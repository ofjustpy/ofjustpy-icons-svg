import os
import re

import logging
logger = logging.getLogger(__name__)

assert "ICON_SVG_REPO_BASEDIR" in os.environ

svg_repo_basedir = os.environ["ICON_SVG_REPO_BASEDIR"]

FONTAWESOME_SVG_REPO="Font-Awesome"
MATERIAL_SVG_REPO="MaterialDesign-SVG"
from .get_lucide_svg import get_lucide_svg
#from lxml import etree
import xml.etree.ElementTree as ET
# def parse_fa_svg(svg_content):
#     # Parse the SVG string (SVG is valid XML)
#     # Note: If svg_content is a string, use ET.fromstring(). 
#     # If it's a file path, use ET.parse(svg_content).getroot()
#     root = ET.fromstring(svg_content)
    
#     # In xml.etree, the root IS the <svg> tag. 
#     # ElementTree keys are case-sensitive; standard SVG uses 'viewBox' (capital B)
#     # We use .get() to handle case variations safely.
#     viewbox = root.attrib.get('viewBox') or root.attrib.get('viewbox')
    
#     # FontAwesome SVGs often have a comment or metadata as the first child.
#     # We iterate through children to find the first actual <path> tag.
#     path = None
#     for child in root:
#         # Strip XML namespaces if present (e.g., '{http://www.w3.org/2000/svg}path')
#         tag_name = child.tag.split('}')[-1] 
#         if tag_name == "path":
#             path = child
#             break
            
#     assert path is not None, "No <path> element found in the SVG"
    
#     # Convert the path element back to a string
#     path_content = ET.tostring(path, encoding="unicode")
    
#     return viewbox, path_content





def parse_fa_svg(svg_content, fill_color="#000000"):
    # 1. Register the SVG namespace globally. 
    # An empty prefix "" means 'http://www.w3.org/2000/svg' is the default namespace.
    # This completely eliminates 'ns0:' and duplicate xmlns attributes.
    SVG_NS = "http://www.w3.org/2000/svg"
    ET.register_namespace("", SVG_NS)
    
    root = ET.fromstring(svg_content)
    
    viewbox = root.attrib.get('viewBox') or root.attrib.get('viewbox')
    
    # 2. Find the path using proper XML namespacing
    # In standard XML parsing, tags are looked up using '{namespace}tag'
    path = root.find(f".//{{{SVG_NS}}}path")
            
    assert path is not None, "No <path> element found in the SVG"
    
    # 3. Safely set the fill color using the standard dictionary API
    path.set('fill', fill_color)
    
    # 4. Serialize back to a string
    path_content = ET.tostring(path, encoding="unicode")
    
    return viewbox, path_content




# def parse_fa_svg(svg_content):
#     parser = etree.HTMLParser()
#     root = etree.fromstring(svg_content, parser)
#     body = root.getchildren()[0]
#     svg = body.getchildren()[0]
#     viewbox = svg.attrib['viewbox']
#     # # for fontawesome [0] is comment
#     # # 
#     path = svg.getchildren()[1]
#     assert path.tag == "path"
#     path_content = etree.tostring(path, encoding="unicode")
#     return viewbox, path_content
#     #raise ValueError("Not Implemented")

# def parse_mdi_svg(svg_content):
#     parser = etree.HTMLParser()
#     root = etree.fromstring(svg_content, parser)
#     body = root.getchildren()[0]
#     svg = body.getchildren()[0]
#     viewbox = svg.attrib['viewbox']
#     # # for fontawesome [0] is comment
#     # # 
#     path = svg.getchildren()[0]
#     assert path.tag == "path"
#     path_content = etree.tostring(path, encoding="unicode")
#     return viewbox, path_content



def parse_mdi_svg(svg_content):
    root = ET.fromstring(svg_content)
    viewbox = root.attrib.get('viewBox', '0 0 24 24') # MDI defaults to 24x24
    
    # Directly target the first child element
    path = root[0] 
    
    # Clean up namespace if the XML parser appended it dynamically
    tag_name = path.tag.split('}')[-1]
    assert tag_name == "path", f"Expected 'path', got '{tag_name}'"
    
    path_content = ET.tostring(path, encoding="unicode")
    return viewbox, path_content


def to_kebab_case(camel_case_name):
    name = re.sub(r'(?<!^)(?=[A-Z])', '-', camel_case_name).lower()
    return name

def get_svg(label, group, mdi_label):
    """
    
    """
    try:
        fa_svg = get_fontawesome_svg(label, group)
        return fa_svg
    except:
        if mdi_label:
            try:
                mdi_svg = get_mdi_svg(mdi_label)
                return mdi_svg
            except:
                logger.error(f"unable to find {mdi_label}")
                pass
            
        raise ValueError(f"svg for label {label} {group} {mdi_label} -- Not found")
        
        
# The parsed svg doesn't get rendered
# This does
# <svg class="w-5 h-5  svg-inline--fa  fa-1x " fill="#000000" fixedwidth="True" viewBox="0 0 512 512" aria-hidden="true" focusable="false" data-prefix="fas" role="img" xmlns="http://www.w3.org/2000/svg"><path d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c-9.4 9.4-9.4 24.6 0 33.9l47 47-47 47c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l47-47 47 47c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-47-47 47-47c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-47 47-47-47c-9.4-9.4-24.6-9.4-33.9 0z"></path></svg>

def get_fontawesome_svg( label, group="solid"):
    icon_filename = to_kebab_case(label[2:])
    svg_path = os.path.join(svg_repo_basedir,
                            FONTAWESOME_SVG_REPO,
                            "svgs", group, f"{icon_filename}.svg")

    try:
        # Read the contents of the SVG file
        with open(svg_path, "r") as svg_file:
            svg_content = svg_file.read()
        return parse_fa_svg(svg_content
        )
    except FileNotFoundError:
        logger.debug(f"cannot find svg from {label} with path = {svg_path}")
        
        raise FileNotFoundError
    
    pass



def get_mdi_svg( label):
    """
    get material design icon
    """
    svg_path = os.path.join(svg_repo_basedir,
                            MATERIAL_SVG_REPO,
                            "svg",
                            f"{label}.svg")
    
    
    try:
        # Read the contents of the SVG file
        with open(svg_path, "r") as svg_file:
            svg_content = svg_file.read()
            return parse_mdi_svg(svg_content
                             )
    except FileNotFoundError:
        raise FileNotFoundError
    
    pass
