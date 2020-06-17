#!/usr/bin/python

from PIL import Image
from tomlkit import loads
from spotify_covers.utils import get_project_root
import sys
import os


def main():
    doc = loads(open(
        os.path.join(get_project_root(), 'config\\covers.toml')).read())

    for cover in doc['cover']:
        try:
            cover_image = Image.open(
                os.path.join(get_project_root(), 'images', cover['bg-image']))

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        cover_image.show()


if __name__ == "__main__":
    main()
