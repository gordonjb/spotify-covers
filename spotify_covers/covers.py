#!/usr/bin/python

from PIL import Image, ImageOps, ImageFont, ImageDraw
from tomlkit import loads
from spotify_covers.utils import get_project_root
import sys
import os


logo_padding_percentage = 3.865
logo_size_percentage = 7.4
logo_transparency_percentage = 20
max_text_width_percentage = 95
max_text_height_percentage = 8.5
text_height_example_string = "Genre Glitch"


def get_text_area(output_size):
    max_text_area_ratio = max_text_width_percentage/100
    return int(max_text_area_ratio * output_size[0])


def get_text_height(output_size):
    max_text_area_ratio = max_text_height_percentage/100
    return int(max_text_area_ratio * output_size[0])


def get_logo_location(output_size):
    logo_padding_ratio = logo_padding_percentage/100
    padding_px = int(logo_padding_ratio * output_size[0])
    return (padding_px, padding_px)


def get_logo_size(output_size):
    logo_size_ratio = logo_size_percentage/100
    size_px = int(logo_size_ratio * output_size[0])
    return (size_px, size_px)


def get_logo_alpha_int():
    return int((logo_transparency_percentage * 255)/100)


def get_logo_alpha_ratio():
    return logo_transparency_percentage/100


def get_scaled_size(output_size, scale_percentage):
    scale_ratio = scale_percentage/100
    size_px = int(scale_ratio * output_size[0])
    return (size_px, size_px)


def resize_and_fade_logo(logo, logo_size, output_size, padded_logo_location):
    logo = ImageOps.fit(logo, logo_size, Image.ANTIALIAS)
    base = Image.new('RGBA', output_size, (0, 0, 0, 0))
    base.paste(logo, padded_logo_location, logo)
    base = Image.blend(Image.new('RGBA', output_size, (0, 0, 0, 0)), base, get_logo_alpha_ratio())
    return base


def scale_and_pad_cover(cover_image, output_size, scale, position):
    padded = ImageOps.pad(cover_image, get_scaled_size(output_size, scale), Image.ANTIALIAS)
    base = Image.new('RGBA', output_size, (0, 0, 0, 0))
    s_width, s_height = padded.size
    if position == "bottom":
        # Align towards the middle bottom of the image
        base.paste(padded, (int(output_size[0]/2 - s_width/2), int(output_size[0]*7/8 - s_height*7/8)), padded)
    else:
        # Center align
        base.paste(padded, (int(output_size[0]/2 - s_width/2), int(output_size[0]/2 - s_height/2)), padded)
    return base


def resize_and_show_test_image(test_image, output_size):
    test_image = ImageOps.fit(
                test_image, output_size, Image.ANTIALIAS)
    test_image.putalpha(255)
    test_image.show()
    return test_image


def get_test_image_1():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_1.jpg'))


def get_test_image_1_solid():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_1_solid.jpg'))


def get_test_image_2():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_2.jpg'))


def get_test_image_3():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_3.jpg'))


def get_white_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'Spotify_Icon_RGB_White.png'))


def get_black_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'Spotify_Icon_RGB_Black.png'))


def get_gradient(gradient_name):
    return Image.open(os.path.join(get_project_root(), 'images', 'gradients', gradient_name + '.jpg'))


def get_cover_image(cover):
    return Image.open(os.path.join(get_project_root(), 'images', cover['bg-image']))


def main():
    doc = loads(open(
        os.path.join(get_project_root(), 'config', 'covers.toml'), ).read())

    output_size = (doc['config']['output-size'], doc['config']['output-size'])

    logo_size = get_logo_size(output_size)
    padded_logo_location = get_logo_location(output_size)

    w_base = resize_and_fade_logo(get_white_logo(), logo_size, output_size, padded_logo_location)
    b_base = resize_and_fade_logo(get_black_logo(), logo_size, output_size, padded_logo_location)

    another_test_image = resize_and_show_test_image(get_test_image_3(), output_size)

    for cover in doc['cover']:
        try:
            cover_image = get_cover_image(cover)

            # If scale defined, resize cover to scaled size, using pad to
            # avoid any cropping, otherwise scale to output size to fit
            if cover.get('scale'):
                cover_image = scale_and_pad_cover(cover_image, output_size, cover.get('scale'), cover.get('position'))
            else:
                cover_image = ImageOps.fit(
                    cover_image, output_size, Image.ANTIALIAS)

            # Add alpha channel so mode matches images with transparency,
            # allowing us to use alpha_composite
            if cover_image.mode == 'RGB':
                cover_image.putalpha(255)

            # If a background colour is defined, create a new image with
            # that colour, and composite the cover onto it.
            if cover.get('bg-colour'):
                base = Image.new('RGBA', output_size, cover.get('bg-colour'))
                cover_image = Image.alpha_composite(base, cover_image)

            if cover.get('colour-gradient'):
                if not cover.get('do-not-greyscale', False):
                    cover_image = cover_image.convert('L').convert('RGBA')
                gradient_image = ImageOps.fit(get_gradient(cover.get('colour-gradient')), output_size, Image.ANTIALIAS)
                gradient_image.putalpha(255)
                cover_image = Image.blend(cover_image, gradient_image, 0.7)

            # Composite the logo watermark on top, black logo as default
            if cover.get('use-white-logo'):
                cover_image = Image.alpha_composite(cover_image, w_base)
            else:
                cover_image = Image.alpha_composite(cover_image, b_base)

            # Write text
            if cover.get('main-text'):
                size = 1
                font = ImageFont.truetype('CircularStd-Bold.otf', size)
                max_area = get_text_area(output_size)
                max_height = get_text_height(output_size)
                main_text_line = cover.get('main-text')
                # Calculate maximum font size. Increase size until width of text exceeds defined max area,
                # or height of an example text with no dangling letters, e.g. "Genre Glitch", at that size
                # exceeds defined maximum.
                while (font.getsize(main_text_line)[0] < max_area and font.getsize(text_height_example_string)[1] < max_height):
                    size += 1
                    font = ImageFont.truetype('CircularStd-Bold.otf', size)
                draw = ImageDraw.Draw(cover_image)
                text_location = (int(output_size[0]/2 - font.getsize(main_text_line)[0]/2), int(output_size[1]*0.214 - font.getsize(text_height_example_string)[1]*0.214))
                draw.text(text_location, main_text_line, cover.get('font-colour', 'white'), font)
        except IOError:
            print("Unable to load image")
            sys.exit(1)

        cover_image.show()
        Image.blend(cover_image, another_test_image, 0.65).show()


if __name__ == "__main__":
    main()
