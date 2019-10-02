import pprint
import operator
import numpy as np
from collections import defaultdict
from PIL import Image


class Sprite:
    def __init__(self, label, x1, y1, x2, y2):
        check_list = [label, x1, y1, x2, y2]
        for elm in check_list:
            if isinstance(elm, str) or elm < 0 or (x1, y1) > (x2, y2):
                raise ValueError("Invalid coordinates")
            else:
                self.__label = label
                self.__top_left = (x1, y1)
                self.__bottom_right = (x2, y2)

                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2

    @property
    def label(self):
        return self.__label

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


class Pixel:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return str(self.label)


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


def create_sprite_labels_image(sprites, label_map, background_color=(255, 255, 255)):
    color_dict = {}
    for key in sprites:
        color_dict[key] = create_random_color(background_color)
        for row in range(sprites[key].y1, sprites[key].y2 + 1):
            for col in range(sprites[key].x1, sprites[key].x2 + 1):
                if row == sprites[key].y1 or row == sprites[key].y2:
                    label_map[row][col].label = key
                elif col == sprites[key].x1 or col == sprites[key].x2:
                    label_map[row][col].label = key
    for row in range(len(label_map)):
        for col in range(len(label_map[row])):
            if label_map[row][col].label == 0:
                label_map[row][col] = background_color
            else:
                label_map[row][col] = color_dict[label_map[row][col].label]
    return Image.fromarray(np.array(label_map, dtype=np.uint8))


def create_random_color(background_color):
    if len(background_color) == 4:
        return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
    else:
        return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))


def find_sprites(image, background_color=None):
    label_map = draw_map(image)
    label = 0
    check_label = False
    pixel_list = np.array(image)
    four_direction = [[-1, -1], [-1, 0], [-1, 1], [0, -1]]
    if background_color == None:
        background_color = find_most_common_color(image)
    for row in range(image.size[1]):
        for col in range(image.size[0]):
            if is_background_color(pixel_list[row][col], background_color):
                label_map[row][col].label = 0
            else:
                new_row, new_col = row, col
                label_list = []
                for y, x in four_direction:
                    new_row = row + y
                    new_col = col + x
                    if is_on_area(new_row, new_col, image):
                        if label_map[new_row][new_col].label != 0:
                            label_map[row][col].label = label_map[new_row][new_col].label
                            check_label = True
                            break
                        else:
                            check_label = False
                if check_label == False:
                    label += 1
                    label_map[row][col].label = label
    label_equivalent = create_label_equivalent(label_map, four_direction, image)
    label_map = merge_label_map(label_map, label_equivalent, image)
    sprites = detect_sprite(label_map, image)
    return sprites, label_map


def detect_sprite(label_map, image):
    label_location_dict = {}
    for row in range(image.size[1]):
        for col in range(image.size[0]):
            if label_map[row][col].label != 0:
                label_location_dict.setdefault(label_map[row][col].label, []).append((row, col))
    return create_sprite_object(label_location_dict)


def create_sprite_object(label_location_dict):
    sprites = {}
    for key in label_location_dict:
        x1 = min(label_location_dict[key], key=lambda x: x[1])[1]
        y1 = min(label_location_dict[key], key=lambda x: x[0])[0]
        x2 = max(label_location_dict[key], key=lambda x: x[1])[1]
        y2 = max(label_location_dict[key], key=lambda x: x[0])[0]
        sprites[key] = Sprite(key, x1, y1, x2, y2)
    return sprites


def merge_label_map(label_map, label_equivalent, image):
    for row in range(image.size[1]):
        for col in range(image.size[0]):
            if label_map[row][col].label in label_equivalent.keys():
                label_map[row][col].label = min(list(label_equivalent[label_map[row][col].label]))
    return label_map


def create_label_equivalent(label_map, four_direction, image):
    label_equivalent = {}
    for row in range(image.size[1]):
        for col in range(image.size[0]):
            if label_map[row][col].label != 0:
                count_zero = 0
                new_row, new_col = row, col
                for y, x in four_direction:
                    new_row = row + y
                    new_col = col + x
                    if is_on_area(new_row, new_col, image) and label_map[new_row][new_col].label != 0:
                        label_equivalent.setdefault(label_map[row][col].label, set()).add(
                            label_map[new_row][new_col].label)
                    elif is_on_area(new_row, new_col, image) and label_map[new_row][new_col].label == 0:
                        count_zero += 1
                if count_zero == 4:
                    label_equivalent.setdefault(label_map[row][col].label, set()).add(
                            label_map[row][col].label)
                    if is_on_area(row, col + 1, image) and label_map[row][col + 1].label != 0:
                        label_equivalent.setdefault(label_map[row][col].label, set()).add(
                            label_map[row][col + 1].label)
    return merge_label_equivalent(label_equivalent)


def merge_label_equivalent(input_dict):
    output_dict = {}
    i = 0
    list_key = list(input_dict.keys())
    while i < len(list_key):
        value = list(input_dict[list_key[i]])
        first_check = -2
        second_check = -1
        while first_check != second_check:
            first_check = len(value)
            for elm in value:
                value = list(set(value + list(input_dict[elm])))
            second_check = len(value)
            output_dict.update({list_key[i]: set(value)})
        i += 1
    return output_dict


def draw_map(image):
    label_map = []
    for i in range(image.size[1]):
        tmp_list = []
        for j in range(image.size[0]):
            tmp_list.append(Pixel("."))
        label_map.append(tmp_list)
    return label_map


def is_background_color(pixel, background_color):
    return np.all(pixel == background_color)


def is_on_area(row, col, image):
    return row >= 0 and row < image.size[1] and col >= 0 and col < image.size[0]


if __name__ == "__main__":
    image = Image.open(
        "./resources/optimized_sprite_sheet.png")
    # image = image.convert("L")
    # print(find_most_common_color(image))
    # print(np.array(image))
    # print(image.mode)
    # find_sprites(image)
    sprites, label_map = find_sprites(image)
    sprite_label_image = create_sprite_labels_image(sprites, label_map)
    sprite_label_image.save('./optimized_sprite_sheet_bounding_box_white_background.png')
