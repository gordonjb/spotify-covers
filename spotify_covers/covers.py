#!/usr/bin/python

from PIL import Image, ImageOps, ImageFont, ImageDraw
from tomlkit import loads
from spotify_covers.utils import get_project_root
from pathvalidate import sanitize_filename
import time
import sys
import os


logo_padding_percentage = 3.865
logo_size_percentage = 7.4
logo_transparency_percentage = 20
max_text_width_percentage = 85
max_text_height_percentage = 8.5
max_sub_text_height_percentage = 4
sub_text_padding_percentage = 1
text_height_example_string = "Genre Glitch"


def get_text_area(output_size):
    max_text_area_ratio = max_text_width_percentage/100
    return int(max_text_area_ratio * output_size[0])


def get_text_height(output_size):
    max_text_area_ratio = max_text_height_percentage/100
    return int(max_text_area_ratio * output_size[0])


def get_sub_text_height(output_size):
    max_text_area_ratio = max_sub_text_height_percentage/100
    return int(max_text_area_ratio * output_size[0])


def get_logo_location(output_size):
    logo_padding_ratio = logo_padding_percentage/100
    padding_px = int(logo_padding_ratio * output_size[0])
    return (padding_px, padding_px)


def get_padding_height(output_size):
    sub_text_padding_ratio = sub_text_padding_percentage/100
    padding_px = int(sub_text_padding_ratio * output_size[0])
    return padding_px


def get_logo_size(output_size):
    logo_size_ratio = logo_size_percentage/100
    size_px = int(logo_size_ratio * output_size[0])
    return (size_px, size_px)


def get_logo_alpha_ratio(logo_transparency):
    return logo_transparency/100


def get_scaled_size(output_size, scale_percentage):
    scale_ratio = scale_percentage/100
    size_px = int(scale_ratio * output_size[0])
    return (size_px, size_px)


def resize_and_fade_logo(logo, logo_size, output_size, padded_logo_location, logo_opacity):
    logo = ImageOps.fit(logo, logo_size, Image.ANTIALIAS)
    base = Image.new('RGBA', output_size, (0, 0, 0, 0))
    base.paste(logo, padded_logo_location, logo)
    base = Image.blend(Image.new('RGBA', output_size, (0, 0, 0, 0)), base, get_logo_alpha_ratio(logo_opacity))
    return base


def scale_and_pad_cover(cover_image, output_size, scale, position):
    padded = ImageOps.pad(cover_image, get_scaled_size(output_size, scale), Image.ANTIALIAS)
    base = Image.new('RGBA', output_size, (0, 0, 0, 0))
    s_width, s_height = padded.size
    if position == "bottom":
        # Align towards the middle bottom of the image
        base.paste(padded, (int(output_size[0]/2 - s_width/2), int(output_size[0]*7/8 - s_height*7/8)), padded)
    elif position == "from-bottom":
        # Align touching the bottom of the image going up
        base.paste(padded, (int(output_size[0]/2 - s_width/2), int(output_size[0] - s_height)), padded)
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


def calculate_font_location(output_size, font, main_text_line, draw):
    return (int(output_size[0]/2 - draw.textsize(main_text_line, font)[0]/2),
            int(output_size[1]*0.214 - draw.textsize(text_height_example_string, font)[1]*0.214))


def calculate_centred_font_location(output_size, font, main_text_line, draw):
    return (int(output_size[0]/2 - draw.textsize(main_text_line, font)[0]/2),
            int(output_size[1]/2 - draw.textsize(main_text_line, font)[1]/2))


def get_test_image_1():
    return Image.open(os.path.join(get_project_root(), 'images', 'test', 'test_1.jpg'))


def get_test_image_1_solid():
    return Image.open(os.path.join(get_project_root(), 'images', 'test', 'test_1_solid.jpg'))


def get_test_image_2():
    return Image.open(os.path.join(get_project_root(), 'images', 'test', 'test_2.jpg'))


def get_test_image_3():
    return Image.open(os.path.join(get_project_root(), 'images', 'test', 'test_3.jpg'))


def get_test_image(output_size, test):
    if test == "1":
        return resize_and_show_test_image(get_test_image_1(), output_size)
    elif test == "1-solid":
        return resize_and_show_test_image(get_test_image_1_solid(), output_size)
    elif test == "2":
        return resize_and_show_test_image(get_test_image_2(), output_size)
    elif test == "3":
        return resize_and_show_test_image(get_test_image_3(), output_size)


def get_white_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'logo', 'Spotify_Icon_RGB_White.png'))


def get_black_logo():
    return Image.open(os.path.join(get_project_root(), 'images', 'logo', 'Spotify_Icon_RGB_Black.png'))


def get_gradient(gradient_name):
    return Image.open(os.path.join(get_project_root(), 'images', 'gradient', gradient_name + '.jpg'))


def get_cover_image(cover):
    return Image.open(os.path.join(get_project_root(), 'images', cover['bg-image']))


def show():
    main(show=True)


def test1():
    main(show=True, test="1")


def test1_solid():
    main(show=True, test="1-solid")


def test2():
    main(show=True, test="2")


def test3():
    main(show=True, test="3")


def main(show=False, test=""):
    start_time = time.time()

    doc = loads(open(
        os.path.join(get_project_root(), 'config', 'covers.toml'), ).read())

    output_size = (doc['config']['output-size'], doc['config']['output-size'])

    logo_size = get_logo_size(output_size)
    padded_logo_location = get_logo_location(output_size)

    w_base = resize_and_fade_logo(get_white_logo(), logo_size, output_size, padded_logo_location, logo_transparency_percentage)
    b_base = resize_and_fade_logo(get_black_logo(), logo_size, output_size, padded_logo_location, logo_transparency_percentage)

    if test != "":
        test_image = get_test_image(output_size, test)
    else:
        test_image = None

    for cover in doc['cover']:
        try:
            cover_image = get_cover_image(cover)

            # Add alpha channel so mode matches images with transparency,
            # allowing us to use alpha_composite
            if cover_image.mode == 'RGB':
                cover_image.putalpha(255)

            # If scale defined, resize cover to scaled size, using pad to
            # avoid any cropping, otherwise scale to output size to fit
            if cover.get('scale'):
                cover_image = scale_and_pad_cover(cover_image, output_size, cover.get('scale'), cover.get('position'))
            else:
                cover_image = ImageOps.fit(
                    cover_image, output_size, Image.ANTIALIAS)

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
                opacity = cover.get('gradient-opacity', 70)/100
                cover_image = Image.blend(cover_image, gradient_image, opacity)

            # Composite the logo watermark on top, black logo as default
            if cover.get('use-white-logo'):
                if cover.get('logo-opacity'):
                    cover_image = Image.alpha_composite(cover_image,
                        resize_and_fade_logo(get_white_logo(), logo_size, output_size, padded_logo_location, cover.get('logo-opacity')))
                else:
                    cover_image = Image.alpha_composite(cover_image, w_base)
            else:
                if cover.get('logo-opacity'):
                    cover_image = Image.alpha_composite(cover_image,
                        resize_and_fade_logo(get_black_logo(), logo_size, output_size, padded_logo_location, cover.get('logo-opacity')))
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
                draw = ImageDraw.Draw(cover_image)
                while (draw.textsize(main_text_line, font)[0] < max_area and draw.textsize(text_height_example_string, font)[1] < max_height):
                    size += 1
                    font = ImageFont.truetype('CircularStd-Bold.otf', size)
                # Put in a variable so sub-text can use to calculate area already covered
                main_text_size = draw.textsize(main_text_line, font)
                if cover.get('centre-text'):
                    text_location = calculate_centred_font_location(output_size, font, main_text_line, draw)
                else:
                    text_location = calculate_font_location(output_size, font, main_text_line, draw)
                draw.text(text_location, main_text_line, cover.get('font-colour', 'white'), font, align="center")

            if cover.get('sub-text'):
                size = 1
                font = ImageFont.truetype('CircularStd-Bold.otf', size)
                max_area = get_text_area(output_size)
                max_height = get_sub_text_height(output_size)
                main_text_line = cover.get('sub-text')
                # Calculate maximum font size. Increase size until width of text exceeds defined max area,
                # or height of an example text with no dangling letters, e.g. "Genre Glitch", at that size
                # exceeds defined maximum.
                draw = ImageDraw.Draw(cover_image)
                while (draw.textsize(main_text_line, font)[0] < max_area and draw.textsize(text_height_example_string, font)[1] < max_height):
                    size += 1
                    font = ImageFont.truetype('CircularStd-Bold.otf', size)
                if cover.get('sub-text-above'):
                    main_start = text_location[1]
                    sub_text_location = (int(output_size[0]/2 - draw.textsize(main_text_line, font)[0]/2), main_start - get_padding_height(output_size) - draw.textsize(text_height_example_string, font)[1])
                else:
                    main_end = text_location[1] + main_text_size[1]
                    sub_text_location = (int(output_size[0]/2 - draw.textsize(main_text_line, font)[0]/2), get_padding_height(output_size) + main_end)

                draw.text(sub_text_location, main_text_line, cover.get('sub-font-colour', 'white'), font, align="center")

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        if show:
            cover_image.show()
        else:
            if not os.path.exists(os.path.join(get_project_root(), 'images', 'covers')):
                os.makedirs(os.path.join(get_project_root(), 'images', 'covers'))

            # Ensure unique filenames by first trying to append config strings, then appending numbers if the file still exists already
            parts = [cover.get('main-text'), cover.get('sub-text'), cover.get('bg-image'), cover.get('colour-gradient')]
            parts = [i for i in parts if i is not None]
            i = 0
            file_name = ""
            while i < len(parts):
                file_name += parts[i]
                file_path = os.path.join(get_project_root(), 'images', 'covers', sanitize_filename(file_name + ".jpg"))
                if os.path.exists(file_path) and os.path.getmtime(file_path) > start_time:
                    i += 1
                    file_name += "_"
                else:
                    break
            else:
                x = 0
                while os.path.exists(file_path) and os.path.getmtime(file_path) > start_time:
                    x += 1
                    file_path = os.path.join(get_project_root(), 'images', 'covers', sanitize_filename(file_name + str(x) + ".jpg"))

            cover_image.convert("RGB").save(file_path, quality=95)

        if test_image is not None:
            Image.blend(cover_image, test_image, 0.65).show()


if __name__ == "__main__":
    main()
