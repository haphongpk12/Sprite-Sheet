import timeit
import operator
import numpy as np
from collections import defaultdict
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
    color_count = defaultdict(int)
    for pixel in image.getdata():
        color_count[pixel] += 1
    return max(color_count.items(), key=operator.itemgetter(1))[0]


class Sprite:
    def __init__(self, label, x1, y1, x2, y2):
        check_list = [label, x1, y1, x2, y2]
        for elm in check_list:
            if isinstance(elm, str) or elm < 0 or (x1, y1) > (x2, y2):
                raise ValueError("Invalid coordinates")
            else:
                self._label = label
                self._top_left = (x1, y1)
                self._bottom_right = (x2, y2)

                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2

    @property
    def label(self):
        return self._label

    @property
    def top_left(self):
        return (self.x1, self.y1)

    @property
    def bottom_right(self):
        return (self.x2, self.y2)

    @property
    def width(self):
        return self.x2 - self.x1 + 1

    @property
    def height(self):
        return self.y2 - self.y1 + 1


if __name__ == "__main__":
    # image = Image.open(
    #     "./resources/islands.png")
    # image = image.convert("L")
    # print(find_most_common_color(image))
    sprite = Sprite(1, 12, 23, 145, 208)
    print(sprite.height)
