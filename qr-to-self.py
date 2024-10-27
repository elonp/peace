import qrcode
import qrcode.constants

def create_qr_code_svg():
    url = "https://elonp.github.io/peace/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # make svg image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr-to-self.png")


if __name__ == "__main__":
    create_qr_code_svg()
