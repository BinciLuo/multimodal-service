import base64
from io import BytesIO
from PIL import Image
import numpy as np
from modules.utils.img_segment import erode_image
from const import MASK_ERODE_RATE


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

# FIXME: Result not ideal, may not use this.
def get_background_color(image: Image.Image):
    r, g, b = image.split()
    r_channel = [ i for m in np.array(r) for i in m ]
    g_channel = [ i for m in np.array(g) for i in m ]
    b_channel = [ i for m in np.array(b) for i in m ]

    max_r = get_max_scope(5, r_channel)
    max_g = get_max_scope(5, g_channel)
    max_b = get_max_scope(5, b_channel)

    return np.array([max_r, max_g, max_b])

def generate_mask_from_black(image: Image.Image):
    """
    ### This function generate transparent mask image from black points in input image
    ### Argvs
    ```
        image(Image.Image): input image
    ```
    ### Return
    ```
        mask_packages(Image.Image): mask image of which mode is RGBA 
    ```
    """
    # 创建一个新的RGBA图像（黑色背景）
    mask = Image.new("RGBA", image.size, (0, 0, 0, 255))

    # 腐蚀图片
    eroded_image = erode_image(image, int(image.size[0]/MASK_ERODE_RATE) * 2 + 1)

    # 获取RGB图像的像素数据
    rgb_data = eroded_image.getdata()

    # 遍历像素数据，找到全黑的像素点并将其复制到RGBA图像
    for i, pixel in enumerate(rgb_data):
        if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
            # 如果是全黑的像素点，将其复制到RGBA图像
            mask.putpixel((i % image.width, i // image.width), (0, 0, 0, 0))
        else:
            mask.putpixel((i % image.width, i // image.width), (pixel[0], pixel[1], pixel[2], 255))

    return mask

def convert_unblack_to_white(image: Image.Image):
    """
    ### This function convert pixcels which are not black to white
    ### Argvs
    ```
        image(Image.Image): input image
    ```
    ### Return
    ```
        rgb_image(Image.Image): mask image of which mode is RGB and pixcel only values black or white
    ```
    """
    # 转换为RGB模式
    rgb_image = image.convert('RGB')

    # 获取图像的宽度和高度
    width, height = rgb_image.size

    # 遍历每个像素
    for x in range(width):
        for y in range(height):
            # 获取像素的RGB值
            r, g, b = rgb_image.getpixel((x, y))

            # 检查是否为全黑像素
            if r == g == b == 0:
                # 如果是全黑像素跳过，否则转为全白
                continue
            rgb_image.putpixel((x, y), (255, 255, 255))

    return rgb_image
