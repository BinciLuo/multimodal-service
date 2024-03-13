import base64
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
from const import MASK_ERODE_RATE, segment_config

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

    # 腐蚀图片 FIXME: rm
    #eroded_image = erode_image(image, int(image.size[0]/MASK_ERODE_RATE) * 2 + 1)
    eroded_image = image
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

def erode_image(image: Image.Image, erode_range: int):
    # 将图像转换为灰度图
    gray_image = image.convert('L')

    # 使用滤波器进行腐蚀操作
    gray_image = gray_image.filter(ImageFilter.MaxFilter(3))
    eroded_image = gray_image.filter(ImageFilter.MinFilter(erode_range))

    # 将原始图像与腐蚀后的图像进行比较，将相同位置的像素设置为黑色
    result_image = Image.new('RGB', image.size)
    for x in range(image.width):
        for y in range(image.height):
            eroded_pixel = eroded_image.getpixel((x, y))

            if eroded_pixel == 0:
                result_image.putpixel((x, y), (0, 0, 0))  # 设置为黑色
            else:
                result_image.putpixel((x, y), image.getpixel((x, y)))

    return result_image

def gray_pixel_filter_max(image: Image.Image, xy: tuple[int, int], ignore: list[int]):
    if image.getpixel(xy) in ignore:
        return image.getpixel(xy)
    kernel_half = image.getpixel(xy)
    max = image.getpixel(xy)
    for i in range(xy[0]-kernel_half if xy[0]-kernel_half >=0 else 0, xy[0]+kernel_half+1 if xy[0]+kernel_half+1 <= image.size[0] else image.size[0]):
        for j in range(xy[1]-kernel_half if xy[1]-kernel_half >=0 else 0, xy[1]+kernel_half+1 if xy[1]+kernel_half+1 <= image.size[1] else image.size[1]):
            max = image.getpixel(xy) if image.getpixel(xy) > max else max
    return max


def get_gray_mask_0(key_and_images: list[(str, Image.Image)], size):
    # 使用滤波器进行腐蚀操作
    gray_image = Image.new('L', size)
    for key,image in key_and_images:
        for x in range(size[0]):
            for y in range(size[1]):
                if image.getpixel((x, y)) == 255:
                    gray_image.putpixel((x, y), int(size[0]/segment_config['erode'][key]['rate']) if key in segment_config['erode'].keys() else 255)
    # debug
    gray_image.save("debug/gray_image.png")
    filtered_image = Image.new('L', size)
    for x in range(size[0]):
        for y in range(size[1]):
            max = gray_pixel_filter_max(gray_image, (x,y), [0, 255])
            filtered_image.putpixel((x, y), max if max == 0 else 255)
    # debug
    filtered_image.save("debug/filtered_image.png")

    return filtered_image