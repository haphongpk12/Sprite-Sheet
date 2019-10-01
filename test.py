input_dict1 = {1: {1, 3}, 2: {2, 4}, 3: {1, 3, 5}, 4: {
    2, 4, 6}, 5: {3, 5, 7}, 6: {8, 4, 6}, 7: {5, 7}, 8: {8, 6}}
input_dict2 = {1: {1, 3}, 3: {3, 5}, 5: {5, 7}, 7: {
    7, 9}, 9: {9, 11}, 11: {11, 12}, 12: {12, 1}}


def merge_label(input_dict):
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


print(merge_label(input_dict1))
