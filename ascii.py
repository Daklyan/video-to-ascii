import numpy as np

from PIL import Image

GRAYSCALE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def get_average_grayscale_value(image):
    np_image = np.array(image)
    width, height = np_image.shape

    return np.average(np_image.reshape(width * height))


def convert_image_to_ascii(filename: str, columns: int, scale: int):
    global GRAYSCALE

    image = Image.open(filename).convert("L")

    width, height = image.size[0], image.size[1]

    tile_width = width / columns
    tile_height = height / scale

    rows = int(height / tile_height)

    if columns > width or rows > height:
        print("Image too small for speicified cols!")  # Replace by LOGGER.error
        exit(0)

    ascii_image = []

    for row in range(rows):
        y1 = int(row * tile_height)
        y2 = int((row + 1) * tile_height)

        if row == rows - 1:
            y2 = height

        ascii_image.append("")

        for column in range(columns):
            x1 = int(column * tile_width)
            x2 = int((column + 1) * tile_width)

            if column == columns - 1:
                x2 = width

            croped_image = image.crop((x1, y1, x2, y2))

            average_luminance = int(get_average_grayscale_value(croped_image))

            grayscale_value = GRAYSCALE[int((average_luminance * 69) / 255)]

            ascii_image += grayscale_value

    return ascii_image
