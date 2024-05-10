import os
import re

assert "ICON_SVG_REPO_BASEDIR" in os.environ

svg_repo_basedir = os.environ["ICON_SVG_REPO_BASEDIR"]

FONTAWESOME_SVG_REPO="Font-Awesome"
MATERIAL_SVG_REPO="MaterialDesign-SVG"

from lxml import etree
def parse_fa_svg(svg_content):
    parser = etree.HTMLParser()
    root = etree.fromstring(svg_content, parser)
    body = root.getchildren()[0]
    svg = body.getchildren()[0]
    viewbox = svg.attrib['viewbox']
    # for fontawesome [0] is comment
    # 
    path = svg.getchildren()[1]
    assert path.tag == "path"
    path_content = etree.tostring(path, encoding="unicode")
    return viewbox, path_content

def parse_mdi_svg(svg_content):
    parser = etree.HTMLParser()
    root = etree.fromstring(svg_content, parser)
    body = root.getchildren()[0]
    svg = body.getchildren()[0]
    viewbox = svg.attrib['viewbox']
    # for fontawesome [0] is comment
    # 
    path = svg.getchildren()[0]
    assert path.tag == "path"
    path_content = etree.tostring(path, encoding="unicode")
    return viewbox, path_content


def to_kebab_case(camel_case_name):
    name = re.sub(r'(?<!^)(?=[A-Z])', '-', camel_case_name).lower()
    return name

def get_svg(label, group, mdi_label):
    """
    
    """
    
    try:
        return get_fontawesome_svg(label, group)
    except:

        if mdi_label:
            try:
                return get_mdi_svg(mdi_label)
            except:
                pass
            
        raise ValueError(f"svg for label {label} {group} {mdi_label} -- Not found")
        
        
    
def get_fontawesome_svg( label, group="solid"):
    icon_filename = to_kebab_case(label[2:])
    print(icon_filename)
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
