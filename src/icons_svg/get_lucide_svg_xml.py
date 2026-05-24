import os
import xml.etree.ElementTree as ET
import logging

LUCIDE_SVG_REPO = "lucide"
svg_repo_basedir = os.environ["ICON_SVG_REPO_BASEDIR"]

def to_kebab_case(name: str) -> str:
    """Convert CamelCase or PascalCase to kebab-case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
logger = logging.getLogger(__name__)

def strip_ns(tree):
    """
    Standard ET approach to remove {namespace} from tags.
    Note: ET modifies the tree in-place.
    """
    for elem in tree.iter():
        if isinstance(elem.tag, str) and elem.tag.startswith("{"):
            elem.tag = elem.tag.split("}", 1)[1]
    return tree

def parse_lucide_svg(svg_content):
    """
    Parse a Lucide SVG string using pure xml.etree.
    """
    # ET.fromstring handles the parsing. 
    # Note: ET doesn't have a direct 'remove_comments' flag in fromstring,
    # but comments are ignored by default in the standard ElementTree parser
    # unless a custom TreeBuilder is used.
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as e:
        raise ValueError(f"Invalid SVG XML: {e}")

    root = strip_ns(root)
    
    # Lucide icons: root.tag == 'svg'
    if root.tag != "svg":
        raise ValueError("Invalid Lucide SVG content: root tag is not <svg>")
    
    # Extract viewBox (checking both cases just in case)
    viewbox = root.attrib.get("viewBox", root.attrib.get("viewbox", None))
    if not viewbox:
        raise ValueError("Lucide SVG missing viewBox attribute")
    
    # Collect all child elements inside <svg>
    inner_elements = []
    for child in root:
        # In ET, comments are not instances of 'str' tags, 
        # but we check to ensure we only get actual elements.
        if isinstance(child.tag, str):
            # ET.tostring returns bytes by default; 'unicode' is for Python 3 string output
            inner_elements.append(ET.tostring(child, encoding="unicode"))
    
    inner_svg_content = "\n".join(inner_elements)
    return viewbox, inner_svg_content

def get_lucide_svg(label: str):
    """
    Retrieve Lucide SVG icon content by label using standard ET.
    """
    icon_filename = to_kebab_case(label)
    svg_path = os.path.join(
        svg_repo_basedir,
        LUCIDE_SVG_REPO,
        "icons",
        f"{icon_filename}.svg"
    )

    try:
        with open(svg_path, "r", encoding="utf-8") as svg_file:
            svg_content = svg_file.read()
        return parse_lucide_svg(svg_content)

    except FileNotFoundError:
        logger.debug(f"Lucide SVG not found for {label} at {svg_path}")
        raise FileNotFoundError(f"Lucide icon '{label}' not found at {svg_path}")
