import base64
from io import BytesIO
from PIL import Image
import numpy as np


# FIXME: Result not ideal, may not use this.
def get_max_scope(delta, array: list[int]):
    count_array = np.bincount(array, minlength=256)
    print(count_array)
    current_index = 0
    current_count = (1+delta) * count_array[current_index] + sum(count_array[:delta+1])
    max_index = 0
    max_count = current_count
    current_index += 1

    while current_index <= 255:
        reduce_num = count_array[current_index - delta] if current_index - delta >= 0 else count_array[0]
        add_num = count_array[current_index + delta] if current_index + delta <= 255 else count_array[255]
        current_count = current_count + add_num - reduce_num
        if current_count > max_count:
            max_index = current_index
            max_count = current_count
        current_index += 1
    return max_index

def get_background_color(image: Image):
    r, g, b = image.split()
    r_channel = [ i for m in np.array(r) for i in m ]
    g_channel = [ i for m in np.array(g) for i in m ]
    b_channel = [ i for m in np.array(b) for i in m ]

    max_r = get_max_scope(5, r_channel)
    max_g = get_max_scope(5, g_channel)
    max_b = get_max_scope(5, b_channel)

    return np.array([max_r, max_g, max_b])

if __name__ == '__main__':
    with open("../../tests/test_img.txt",'r') as f:
        init_img_str = f.read()
    #image = Image.open(BytesIO(base64.b64decode(init_img_str)))
    image = Image.open("/Users/luobinci/Downloads/portrait.jpeg")
    image.show()
    print(image.size)
    print(get_background_color(image))