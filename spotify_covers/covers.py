#!/usr/bin/python

from PIL import Image, ImageOps
from tomlkit import loads
from spotify_covers.utils import get_project_root
import sys
import os


logo_padding_percentage = 4.1
logo_size_percentage = 7.1


def get_padded_location(output_size):
    logo_padding_ratio = logo_padding_percentage/100
    print(logo_padding_ratio)
    padding_px = int(logo_padding_ratio * output_size[0])
    print(padding_px)
    return (padding_px, padding_px)


def get_padded_size(output_size):
    logo_size_ratio = logo_size_percentage/100
    print(logo_size_ratio)
    size_px = int(logo_size_ratio * output_size[0])
    print(size_px)
    print(logo_size_ratio * output_size[0])
    return (size_px, size_px)


def get_test_image_1():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_1.jpg'))


def get_test_image_2():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'test_2.jpg'))


def get_white_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'global', 'Spotify_Icon_RGB_White.png'))


def get_cover_image(cover):
    return Image.open(os.path.join(get_project_root(), 'images', cover['bg-image']))


def main():
    doc = loads(open(
        os.path.join(get_project_root(), 'config', 'covers.toml')).read())

    output_size = (doc['config']['output-size'], doc['config']['output-size'])

    spotify_logo = get_white_logo()
    spotify_logo = ImageOps.fit(
        spotify_logo, get_padded_size(output_size), Image.ANTIALIAS)
    padded_logo_location = get_padded_location(output_size)

    test_image = get_test_image_1()
    test_image = ImageOps.fit(
                test_image, output_size, Image.ANTIALIAS)

    for cover in doc['cover']:
        try:
            cover_image = get_cover_image(cover)
            cover_image = ImageOps.fit(
                cover_image, output_size, Image.ANTIALIAS)
            cover_image.paste(spotify_logo, padded_logo_location, spotify_logo)

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        cover_image.show()
        Image.blend(cover_image, test_image, 1).show()


if __name__ == "__main__":
    main()
