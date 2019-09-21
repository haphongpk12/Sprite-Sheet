import timeit
import operator
import numpy as np
from PIL import Image


def find_most_common_color(image):
    """
    A function returns the pixel color that is the most used in this image.

    @param: image (Image object)
    @return:
        - an integer if the mode is grayscale;
        - a tuple (red, green, blue) of integers if the mode is RGB;
        - a tuple (red, green, blue, alpha) of integers if the mode is RGBA.
    """
    width, height = image.size
    color_count = {}
    for w in range(width):
        for h in range(height):
            current_color = image.getpixel((w, h))
            if current_color in color_count:
                color_count[current_color] += 1
            else:
                color_count[current_color] = 1
    return max(color_count.items(), key=operator.itemgetter(1))[0]


if __name__ == "__main__":
    image = Image.open(
        "./resources/islands.png")
    image = image.convert("L")
    print(find_most_common_color(image))
