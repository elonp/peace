import cairosvg
import argparse
import svgwrite

from .elements import draw_badge_with_qr, draw_badge_without_qr, draw_qr_code_sticker

def create_files(filename_stem, size, draw_function):
    dwg = svgwrite.Drawing(f'{filename_stem}.svg', profile='full', size=size)
    for element in draw_function(dwg):
        dwg.add(element)
    dwg.save(pretty=True)
    cairosvg.svg2pdf(url=f'{filename_stem}.svg', write_to=f'{filename_stem}.pdf')
    cairosvg.svg2png(url=f'{filename_stem}.svg', write_to=f'{filename_stem}.png')


def main():
    parser = argparse.ArgumentParser(description='Create SVGs for badges')
    # argument selecting between badge_1, badge_2 and qr-to-self
    parser.add_argument('badge', choices=['badge_1', 'badge_2', 'qr-to-self'], help='The badge to create')
    args = parser.parse_args()

    if args.badge == 'badge_1':
        kwargs = {
            'filename_stem': 'badge_1',
            'size': (260, 260),
            'draw_function': lambda dwg: draw_badge_without_qr(dwg, 130)
        }
    elif args.badge == 'badge_2':
        kwargs = {
            'filename_stem': 'badge_2',
            'size': (260, 260),
            'draw_function': lambda dwg: draw_badge_with_qr(dwg, 130)
        }
    elif args.badge == 'qr-to-self':
        kwargs = {
            'filename_stem': 'qr-to-self',
            'size': (100, 100),
            'draw_function':  lambda dwg: draw_qr_code_sticker(dwg, 100)
        }
    create_files(**kwargs)


if __name__ == '__main__':
    main()
