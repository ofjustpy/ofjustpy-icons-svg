import os
import logging

logger = logging.getLogger(__name__)

# example: base directory where lucide-icons repo is cloned
# e.g. /home/user/icons-repos/lucide
LUCIDE_SVG_REPO = "lucide"
svg_repo_basedir = os.environ["ICON_SVG_REPO_BASEDIR"]


def to_kebab_case(name: str) -> str:
    """Convert CamelCase or PascalCase to kebab-case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


from lxml import etree

def strip_ns(tree):
    for elem in tree.iter():
        if isinstance(elem.tag, str) and elem.tag.startswith("{"):
            elem.tag = elem.tag.split("}", 1)[1]
    return tree
def parse_lucide_svg(svg_content):
    """
    Parse a Lucide SVG string and extract:
      - the viewBox attribute
      - a concatenated string of all child elements (<path>, <line>, <polyline>, etc.)
    """
    parser = etree.XMLParser(remove_comments=True)
    root = etree.fromstring(svg_content, parser)
    root = strip_ns(root)
    # Lucide icons: root.tag == 'svg'
    if root.tag != "svg":
        raise ValueError("Invalid Lucide SVG content: root tag is not <svg>")
    
    viewbox = root.attrib.get("viewBox", root.attrib.get("viewbox", None))
    if not viewbox:
        raise ValueError("Lucide SVG missing viewBox attribute")
    
    # Collect all child elements inside <svg>
    inner_elements = []
    for child in root:
        if isinstance(child.tag, str):  # skip comments or processing instructions
            inner_elements.append(etree.tostring(child, encoding="unicode"))
    
    inner_svg_content = "\n".join(inner_elements)
    return viewbox, inner_svg_content




def get_lucide_svg(label: str):
    """
    Retrieve Lucide SVG icon content by label.
    Example:
        get_lucide_svg('Camera')
        get_lucide_svg('ArrowUp')
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
