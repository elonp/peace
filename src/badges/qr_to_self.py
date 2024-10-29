import qrcode
import qrcode.image.svg
import qrcode.constants
import svgwrite

def get_qr_code_img(size):
    url = "https://supportbothpeoples.org.uk"
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=size, border=1)
    return img

def get_qr_code_element(dwg, size):
    img = get_qr_code_img(100)
    scale = size / (img.pixel_size / int(str(img.unit_size).replace('mm', '')))
    path = img.path
    element = dwg.path(d=path.attrib['d'])
    element.scale(scale, scale)
    return element

def create_qr_code_svg():
    size = 20
    dwg = svgwrite.Drawing('qr-to-self.svg', profile='full', size=(size, size))
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(255,255,255)'))
    qr = get_qr_code_element(dwg, size)
    dwg.add(qr)
    dwg.save()


if __name__ == "__main__":
    create_qr_code_svg()
