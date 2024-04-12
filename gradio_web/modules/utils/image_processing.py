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

def gray_MinFilter(image: Image.Image, xy: tuple[int, int], ignore: list[int]):
    kernel_half = image.getpixel(xy)
    if kernel_half in ignore:
        return kernel_half
    min = kernel_half
    for i in range(xy[0]-kernel_half if xy[0]-kernel_half >=0 else 0, xy[0]+kernel_half+1 if xy[0]+kernel_half+1 <= image.size[0] else image.size[0]):
        for j in range(xy[1]-kernel_half if xy[1]-kernel_half >=0 else 0, xy[1]+kernel_half+1 if xy[1]+kernel_half+1 <= image.size[1] else image.size[1]):
            min = image.getpixel((i, j)) if image.getpixel((i, j)) < min else min
    return min

def gray_Erode(image: Image.Image, xy: tuple[int, int], color: int, kernel_half: int):
    expand_pixcels = []
    size = image.size
    for i in range(xy[0]-kernel_half if xy[0]-kernel_half >=0 else 0, xy[0]+kernel_half+1 if xy[0]+kernel_half+1 <= size[0] else size[0]):
        for j in range(xy[1]-kernel_half if xy[1]-kernel_half >=0 else 0, xy[1]+kernel_half+1 if xy[1]+kernel_half+1 <= size[1] else size[1]):
            expand_pixcels.append((i, j))
    expand_pixcels = list(set(expand_pixcels))
    for xy in expand_pixcels:
        image.putpixel(xy, color)

def get_optimized_mask(key_and_images: tuple[(str, Image.Image)], size):
    '''
    Mask Optimization
    
    1. Create Origin Gray Image, 0: mask, 255: unmask
    2. Shrink inner range from 255to0
    3. Get outer range pixcels
    4. Get ConfigPixcels from config and Origin and innerRangePixcels
    5. Apply ConfigPixcels Erode
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

    # Shrink inner range from 255to0
    range_white_shrinked_image = shrink_range_white2black(gray_image, 2)
    range_white_shrinked_image_pixcels = range_white_shrinked_image.load()
    
    # Get outer range pixcels
    innerRangePixcels = [] # [(x, y),]
    for y in range(size[1]):
        for x in range(size[0]):
            if gray_image_pixcels[x, y] != range_white_shrinked_image_pixcels[x, y]:
                innerRangePixcels.append((x, y))

    # Get ConfigPixcels from config and Origin and innerRangePixcels
    ConfigPixcels = [] #[((x,y), kernelHalf),]
    for key, image in tqdm(key_and_images, desc='Get Config Pixcels'):
        if key in segment_config['erode'].keys():
            for y in range(size[1]):
                for x in range(size[0]):
                    if image.getpixel((x, y)) == 255 and (x, y) in innerRangePixcels:
                        ConfigPixcels.append(
                            ((x, y), int(size[0]/segment_config['erode'][key]['rate']))
                            )

    # debug
    print(f'Inner Pixcels Len: {len(innerRangePixcels)}')
    range_white_shrinked_image.save("debug/shrinked_image.png")

    # Copy from origin
    filtered_image = copy.deepcopy(gray_image)
    for xy, kernelHalf in tqdm(ConfigPixcels, desc='Expanding'):
        gray_Erode(filtered_image, xy, 0, kernelHalf)
    # debug
    filtered_image.save("debug/filtered_image.png")

    return filtered_image