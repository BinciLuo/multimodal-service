from PIL import Image, ImageFilter
import copy
from const import MASK_ERODE_RATE, segment_config
from tqdm import tqdm

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

    # 获取RGB图像的像素数据
    rgb_data = image.getdata()

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
    eroded_image = gray_image.filter(ImageFilter.MinFilter(erode_range *2 + 1))

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

def shrink_range_white2black(image: Image.Image, erode_range: int):
    # 使用滤波器进行腐蚀操作
    gray_image = image.filter(ImageFilter.MaxFilter(3))
    eroded_image = gray_image.filter(ImageFilter.MinFilter(erode_range * 2 + 1))

    return eroded_image

def shrink_range_black2white(image: Image.Image, erode_range: int):
    # 使用滤波器进行腐蚀操作
    gray_image = image.filter(ImageFilter.MinFilter(3))
    eroded_image = gray_image.filter(ImageFilter.MaxFilter(erode_range * 2 + 1))

    return eroded_image

def gray_pixel_filter_min(image: Image.Image, xy: tuple[int, int], ignore: list[int]):
    kernel_half = image.getpixel(xy)
    if kernel_half in ignore:
        return kernel_half
    min = kernel_half
    for i in range(xy[0]-kernel_half if xy[0]-kernel_half >=0 else 0, xy[0]+kernel_half+1 if xy[0]+kernel_half+1 <= image.size[0] else image.size[0]):
        for j in range(xy[1]-kernel_half if xy[1]-kernel_half >=0 else 0, xy[1]+kernel_half+1 if xy[1]+kernel_half+1 <= image.size[1] else image.size[1]):
            min = image.getpixel((i, j)) if image.getpixel((i, j)) < min else min
    return min

def expand_gray_pixcel(image: Image.Image, xy: tuple[int, int], color: int, kernel_half: int):
    expand_pixcels = []
    size = image.size
    for i in range(xy[0]-kernel_half if xy[0]-kernel_half >=0 else 0, xy[0]+kernel_half+1 if xy[0]+kernel_half+1 <= size[0] else size[0]):
        for j in range(xy[1]-kernel_half if xy[1]-kernel_half >=0 else 0, xy[1]+kernel_half+1 if xy[1]+kernel_half+1 <= size[1] else size[1]):
            expand_pixcels.append((i, j))
    expand_pixcels = list(set(expand_pixcels))
    for xy in expand_pixcels:
        image.putpixel(xy, color)

# def get_gray_mask_0(key_and_images: tuple[(str, Image.Image)], size):
#     '''
#     Mask Optimization
#     TODO: This function need optimization and better annotation
#     1. 获取Rate灰度图
#     2. 获取原遮罩内边缘
#     3. 对内边缘且Rate不为0、255的像素进行周边确认
#     '''
#     # Create Rate Gray Image
#     gray_image = Image.new('L', size)
#     for key,image in key_and_images:
#         for x in range(size[0]):
#             for y in range(size[1]):
#                 if image.getpixel((x, y)) == 255:
#                     gray_image.putpixel((x, y), int(size[0]/segment_config['erode'][key]['rate']) if key in segment_config['erode'].keys() else 255)
#     # debug
#     gray_image.save("debug/gray_image.png")

#     eroded_image = erode_gray_image(gray_image, int(size[0]/MASK_ERODE_RATE))
#     eroded_image.save("debug/eroded_image.png")

#     filtered_image = Image.new('L', size)
#     for x in range(size[0]):
#         for y in range(size[1]):
#             min = gray_pixel_filter_min(gray_image, (x,y), [0, 255]) if gray_image.getpixel((x, y)) not in [0, 255] and eroded_image.getpixel((x, y)) == 0 else gray_image.getpixel((x, y))
#             filtered_image.putpixel((x, y), min if min == 0 else 255)
#     # debug
#     filtered_image.save("debug/filtered_image.png")

#     return filtered_image

def get_gray_mask_0(key_and_images: tuple[(str, Image.Image)], size):
    '''
    Mask Optimization
    TODO: This function need optimization and better annotation
    1. 获取Rate灰度图
    2. 获取原遮罩外边缘
    3. 对内边缘且Rate不为0、255的像素进行周边确认
    '''
    # Create Origin Gray Image, 0: mask, 255: unmask
    gray_image = Image.new('L', size)
    for y in range(size[1]):
        for x in range(size[0]):
            for key,image in key_and_images:
                if image.getpixel((x, y)) == 255:
                    gray_image.putpixel((x, y), 255)
                    break
    gray_image_pixcels = gray_image.load()
    #debug
    gray_image.save("debug/gray_image.png")

    # Get Pixcels from config and Origin
    ConfigPixcels = [] #[((x,y), kernelHalf),]
    for key, image in tqdm(key_and_images, desc='Get Config Pixcels'):
        if key in segment_config['erode'].keys():
            for y in range(size[1]):
                for x in range(size[0]):
                    if image.getpixel((x, y)) == 255:
                        ConfigPixcels.append(
                            ((x, y), int(size[0]/segment_config['erode'][key]['rate']))
                            )

    # Shrink inner range from 255to0
    range_black_shrinked_image = shrink_range_white2black(gray_image, 1)#int(size[0]/MASK_ERODE_RATE))
    range_black_shrinked_image_pixcels = range_black_shrinked_image.load()
    
    # Get outer range pixcels
    innerRangePixcels = [] # [(x, y),]
    for y in range(size[1]):
        for x in range(size[0]):
            if gray_image_pixcels[x, y] != range_black_shrinked_image_pixcels[x, y]:
                innerRangePixcels.append((x, y))

    # debug
    print(f'Inner Pixcels Len: {len(innerRangePixcels)}')
    range_black_shrinked_image.save("debug/shrinked_image.png")

    # Copy from origin
    filtered_image = copy.deepcopy(gray_image)
    for xy, kernelHalf in tqdm(ConfigPixcels, desc='Expanding'):
        if xy in innerRangePixcels:
            print(f"😀",end='')
            expand_gray_pixcel(filtered_image, xy, 0, kernelHalf)
    # debug
    filtered_image.save("debug/filtered_image.png")

    return filtered_image