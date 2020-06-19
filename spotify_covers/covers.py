#!/usr/bin/python

from PIL import Image, ImageOps
from tomlkit import loads
from spotify_covers.utils import get_project_root
import sys
import os


logo_padding_percentage = 3.865
logo_size_percentage = 7.4
logo_transparency_percentage = 15


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


def get_logo_alpha_percent():
    return logo_transparency_percentage/100


def get_scaled_size(output_size, scale_percentage):
    scale_ratio = scale_percentage/100
    size_px = int(scale_ratio * output_size[0])
    return (size_px, size_px)


def resize_and_fade_logo(logo, logo_size, output_size, padded_logo_location):
    logo = ImageOps.fit(logo, logo_size, Image.ANTIALIAS)
    base = Image.new('RGBA', output_size, (0, 0, 0, 0))
    base.paste(logo, padded_logo_location, logo)
    base = Image.blend(Image.new('RGBA', output_size, (0, 0, 0, 0)), base, get_logo_alpha_percent())
    return base


def scale_and_pad_cover(cover_image, output_size, scale):
    padded = ImageOps.pad(cover_image, get_scaled_size(output_size, scale), Image.ANTIALIAS)
    base = Image.new('RGBA', output_size, (0, 0, 0, 0))
    s_width, s_height = padded.size
    base.paste(padded, (int(output_size[0]/2 - s_width/2), int(output_size[0]/2 - s_height/2)), padded)
    return base


def get_test_image_1():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_1.jpg'))


def get_test_image_1_solid():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_1_solid.jpg'))


def get_test_image_2():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_2.jpg'))


def get_white_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'Spotify_Icon_RGB_White.png'))


def get_black_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'Spotify_Icon_RGB_Black.png'))


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

    test_image = get_test_image_1()
    test_image = ImageOps.fit(
                test_image, output_size, Image.ANTIALIAS)
    test_image.putalpha(255)
    test_image.show()

    for cover in doc['cover']:
        try:
            cover_image = get_cover_image(cover)

            # If scale defined, resize cover to scaled size, using pad to
            # avoid any cropping, otherwise scale to output size to fit
            if cover.get('scale'):
                cover_image = scale_and_pad_cover(cover_image, output_size, cover.get('scale'))
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

            # Composite the logo watermark on top, black logo as default
            if cover.get('use-white-logo'):
                cover_image = Image.alpha_composite(cover_image, w_base)
            else:
                cover_image = Image.alpha_composite(cover_image, b_base)

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        cover_image.show()


if __name__ == "__main__":
    main()
