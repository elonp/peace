import svgwrite
import numpy as np

from .qr_to_self import get_qr_code_element

def draw_israeli_flag(dwg, height, width, top, right):
    line_width = height / 20
    stripe_offset = height / 10

    elements = []

    elements.append(dwg.rect(insert=(right - width, top), size=(width, height), fill='white'))
    elements.append(dwg.rect(insert=(right - width, top + stripe_offset), size=(width, line_width), fill='blue'))
    elements.append(dwg.rect(insert=(right - width, top + height - stripe_offset - line_width), size=(width, line_width), fill='blue'))

    star_top = 2.5 * stripe_offset + line_width
    star_bottom = height - star_top

    star_height = star_bottom - star_top
    triang_height = star_height * 3 / 4
    triang_edge_length = triang_height / np.cos(np.radians(30))

    x0 = right - width / 2
    y0 = star_top
    x1 = x0 - triang_edge_length / 2
    y1 = y0 + triang_height
    x2 = x0 + triang_edge_length / 2
    y2 = y1

    elements.append(dwg.polygon(points=[(x0, top + y0), (x1, top + y1), (x2, top + y2)], stroke='blue', stroke_width=line_width, fill='none'))
    elements.append(dwg.polygon(points=[(x0, top + height-y0), (x1, top + height-y1), (x2, top + height-y2)], stroke='blue', stroke_width=line_width, fill='none'))
    return elements


def draw_palestinian_flag(dwg, height, width, top, left, squeeze):
    stripe_height = height / 3
    # Dimensions
    # Draw the black stripe

    elements = []

    elements.append(dwg.rect(insert=(left, top), size=(width, stripe_height), fill='black'))
    
    # Draw the white stripe
    elements.append(dwg.rect(insert=(left, top + stripe_height), size=(width, stripe_height), fill='white'))
    
    # Draw the green stripe
    elements.append(dwg.rect(insert=(left, top + 2 * stripe_height), size=(width, stripe_height), fill='green'))
    
    # Draw the red triangle
    triangle_width = height / 3 * 2 * squeeze
    points = [(left, top), (left + triangle_width, top + height / 2), (left, top + height)]
    elements.append(dwg.polygon(points, fill='red'))

    return elements
 

def add_text(dwg, top_text, bottom_text, centre_x, centre_y, radius, font_size):
    # Text along path
    font="sans-serif"
    text_radius_top = radius + font_size * 0.4
    text_radius_bottom = radius + font_size
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    elements = []

    top_path = dwg.path(
        d=(
            f"M {centre_x}, {centre_y} "
            f"m {text_radius_top}, 0 "
            f"a {text_radius_top},{text_radius_top} 0 1,1 -{text_radius_top * 2}, 0 "
            f"a {text_radius_top},{text_radius_top} 0 1,1 {text_radius_top * 2}, 0 "
        ),
        fill="none",
        id="topCirclePath"
    )
    elements.append(top_path)

    # Add text
    top_text_e = dwg.text("", text_anchor="middle", fill="black", font_size=font_size, font_family=font)
    top_text_e.add(svgwrite.text.TextPath(top_path, top_text, startOffset="75%"))
    elements.append(top_text_e)

    bottom_path = dwg.path(
        d=(
            f"M {centre_x}, {centre_y} "
            f"m -{text_radius_bottom}, 0 "
            f"a {text_radius_bottom},{text_radius_bottom} 0 1,0 {text_radius_bottom * 2}, 0 "
            f"a {text_radius_bottom},{text_radius_bottom} 0 1,0 -{text_radius_bottom * 2}, 0 "
        ),
        fill="none",
        id="bottomCirclePath"
    )
    elements.append(bottom_path)

    # Add text
    bottom_text_e = dwg.text("", text_anchor="middle", fill="black", font_size=font_size, font_family=font)
    bottom_text_e.add(svgwrite.text.TextPath(bottom_path, bottom_text, startOffset="25%"))

    elements.append(bottom_text_e)

    return elements

def draw_qr_code(dwg, size, right, top):
    elements = []
    qr = get_qr_code_element(dwg, size)
    scale = float(qr.attribs['transform'].split('scale(')[1].split(',')[0])
    qr.translate(tx=right/scale, ty=top/scale)
    elements.append(qr)
    return elements

def draw_badge_without_qr(dwg, outer_radius):
    inner_radius = outer_radius / 130 * 100

    elements = []


    elements.append(dwg.circle(center=(outer_radius, outer_radius), r=outer_radius-2, fill='white', stroke='white', stroke_width=2))
    clip = dwg.clipPath(id="clip-path")
    clip.add(dwg.circle(center=(outer_radius, outer_radius), r=inner_radius))
    elements.append(clip)

    for element in draw_israeli_flag(dwg, inner_radius * 2, inner_radius * 3, outer_radius - inner_radius, outer_radius + inner_radius * 1.03):
        element["clip-path"] = "url(#clip-path)"
        elements.append(element)

    for element in draw_palestinian_flag(dwg, inner_radius * 2, inner_radius * 3, outer_radius - inner_radius, outer_radius, 0.5):
        element["clip-path"] = "url(#clip-path)"
        elements.append(element)

    for element in add_text(dwg, "Support Peace", "Stand With Both Peoples", outer_radius, outer_radius, inner_radius*0.975, (outer_radius-inner_radius)*0.8):
        elements.append(element)

    return elements

def draw_badge_with_qr(dwg, outer_radius):
    inner_radius = outer_radius / 130 * 100
    elements = draw_badge_without_qr(dwg, outer_radius)
    size = inner_radius/3
    right = outer_radius - size / 2
    top = outer_radius + size
    for element in draw_qr_code(
        dwg, size, right, top):
        elements.append(element)

    return elements


def draw_qr_code_sticker(dwg, size):
    background = dwg.rect(insert=(0, 0), size=(size, size), fill='white')
    qr = get_qr_code_element(dwg, size)
    elements = [background, qr]
    return elements
