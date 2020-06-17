#!/usr/bin/python

from PIL import Image, ImageOps
from tomlkit import loads
from spotify_covers.utils import get_project_root
import sys
import os


logo_padding_percentage = 3.865
logo_size_percentage = 7.4
logo_transparency_percentage = 50


def get_logo_location(output_size):
    logo_padding_ratio = logo_padding_percentage/100
    print(logo_padding_ratio)
    padding_px = int(logo_padding_ratio * output_size[0])
    print(padding_px)
    return (padding_px, padding_px)


def get_logo_size(output_size):
    logo_size_ratio = logo_size_percentage/100
    print(logo_size_ratio)
    size_px = int(logo_size_ratio * output_size[0])
    print(size_px)
    print(logo_size_ratio * output_size[0])
    return (size_px, size_px)


def get_logo_alpha_int():
    return int((logo_transparency_percentage * 255)/100)


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
        os.path.join(get_project_root(), 'config', 'covers.toml')).read())

    output_size = (doc['config']['output-size'], doc['config']['output-size'])

    logo_size = get_logo_size(output_size)
    padded_logo_location = get_logo_location(output_size)
    logo_alpha = get_logo_alpha_int()

    spotify_logo_w = get_white_logo()
    spotify_logo_w = ImageOps.fit(spotify_logo_w, logo_size, Image.ANTIALIAS)
    spotify_logo_w.putalpha(logo_alpha)
    spotify_logo_b = get_black_logo()
    spotify_logo_b = ImageOps.fit(spotify_logo_b, logo_size, Image.ANTIALIAS)
    spotify_logo_b.putalpha(logo_alpha)

    test_image = get_test_image_1()
    test_image = ImageOps.fit(
                test_image, output_size, Image.ANTIALIAS)

    for cover in doc['cover']:
        try:
            cover_image = get_cover_image(cover)
            cover_image = ImageOps.fit(
                cover_image, output_size, Image.ANTIALIAS)
            if cover.get('use-black-logo'):
                cover_image.paste(spotify_logo_b, padded_logo_location, spotify_logo_b)
            else:
                cover_image.paste(spotify_logo_w, padded_logo_location, spotify_logo_w)

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        cover_image.show()
        Image.blend(cover_image, test_image, 0.85).show()


if __name__ == "__main__":
    main()
