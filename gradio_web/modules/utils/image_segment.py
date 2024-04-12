import base64
from io import BytesIO
import io
import numpy as np
from PIL import Image
import gradio as gr
import functools

from modules.api.pics_api import post_hgface_img_segment
from modules.utils.image_io import trans_image_to_str, trans_str_to_image
from const import MASK_ERODE_RATE, segment_config
from modules.utils.image_processing import get_optimized_mask

def replace_black_pixels(image: Image):
    """
    ### This function convert black pixcels to (0,0,1) or (0,0,1,255)
    ### Argvs
    ```
        image(Image.Image): image to convert
    ```
    ### Return
    ```
        image(Image.Image): converted image
    ```
    """
    if image == None:
        return None
    # 将原始图像转换为NumPy数组
    img_array = np.array(image)
    # 找到原始图像中RGB全为0的像素点
    black_pixels = np.all(img_array[..., :3] == [0, 0, 0], axis=-1)
    # 将符合条件的像素点的RGB值修改为 [0, 0, 1]
    try:
        img_array[black_pixels] = [0, 0, 1]
    except:
        img_array[black_pixels] = [0, 0, 1, 255]
    # 返回处理后的图像
    result_image = Image.fromarray(img_array)
    return result_image

def auto_fill_black(original_image: Image, mask_images: dict):
    """
    ### This function auto fill masks which have black pixcels
    ### Argvs
    ```
        original_image(Image.Image): image to convert
        mask_images(dict): {"mask_packages_label": mask(Image.Image)}
    ```
    ### Return
    ```
        image(Image.Image): auto filled image
    ```
    """
    # 将原始图像转换为NumPy数组
    original_array = np.array(original_image)
    # 获取所有L模式的图像数组
    l_arrays = [np.array(mask_images[key]) for key in mask_images.keys()]
    # 找到原始图像中RGB为全0的像素点
    zero_pixels = np.all(original_array[..., :3] == [0, 0, 0], axis=-1)
    # 对于每个L模式的图像数组，在原始图像中找到对应位置为全黑的像素，并将其置为0
    for layer in l_arrays:
        black_pixels = np.where(zero_pixels & (layer == 255))
        if black_pixels[0].size > 10:
            try:
                original_array[(layer == 255)] = [ 0, 0, 0, 255]
            except:
                original_array[(layer == 255)] = [ 0, 0, 0]

    result_image = Image.fromarray(original_array)
    # 返回处理后的图像
    return result_image

def auto_fill_by_blackpoints(image: Image, base_image: Image):
    """
    ### This function auto fill masks which have black pixcels
    ### Argvs
    ```
        image(Image.Image): image to auto fill
        base_image(Image.Image): base image for segment
    ```
    ### Return
    ```
        image(Image.Image): auto masked image (black mask)
    ```
    """    
    base_img_str = trans_image_to_str(base_image)
    # Post huggingface models and check
    response_json, err = post_hgface_img_segment(base_img_str)
    if err != None:
        # clear cache
        post_hgface_img_segment.cache_clear()
        print(err)
        gr.Warning(err+". Cache cleared")
        return image
    try:
        labels_and_scores = [(image_package['label'], image_package['score']) for image_package in response_json["image_packages"]]
        print(labels_and_scores)
    except:
        print(response_json)
        gr.Warning(response_json.get("error", f"Unknown err: {response_json}"))
        return image
    # Get all mask images
    mask_images={}
    for image_package in response_json["image_packages"]:
        mask_image = trans_str_to_image(image_package['mask'])
        mask_images[image_package['label']] = mask_image
    
    result_image = auto_fill_black(image, mask_images)

    return result_image

def auto_black_keywords(image: Image.Image, mask_images: dict, keys_words: list[str], reverse: bool):
    """
    ### This function auto blcak given masks
    ### Argvs
    ```
        image(Image.Image): image to auto black
        mask_images(dict): {"mask_packages_label": mask(Image.Image)}
        key_words(list[str]): list of mask labels
        reverse(bool): True: mask labels not in keywords, False: mask labels in keywords
    ```
    ### Return
    ```
        image(Image.Image): auto masked image (black mask)
    ```
    """
    # 对于不同的部分进行腐蚀
    shrinked_gray_image = get_optimized_mask([(key,mask_images[key]) for key in mask_images.keys() if key not in keys_words], image.size)

    for x in range(image.width):
        for y in range(image.height):
            if shrinked_gray_image.getpixel((x, y)) == 0:
                try:
                    image.putpixel((x, y), (0, 0, 0))
                except:
                    image.putpixel((x, y), (0, 0, 0, 255))
    return image

@functools.lru_cache
# TODO: change instruction
def auto_black_by_keywords(image: str, base_image: str, keywords: str, reverse: bool = False):
    """
    ### This function auto fill masks which have black pixcels
    ### Argvs
    ```
        image(Image.Image): image to auto fill
        base_image(Image.Image): base image for segment
    ```
    ### Return
    ```
        image(Image.Image): auto masked image (black mask)
    ```
    """
    keywords = keywords.split(' ')
    image = trans_str_to_image(image)
    base_image = trans_str_to_image(base_image)
    keywords = list(keywords)
    init_img_str = trans_image_to_str(base_image)
    # Post huggingface models and check
    response_json, err = post_hgface_img_segment(init_img_str)
    if err != None:
        # clear cache
        post_hgface_img_segment.cache_clear()
        print(err)
        gr.Warning(err+". Cache cleared")
        return image
    try:
        labels_and_scores = [(image_package['label'], image_package['score']) for image_package in response_json["image_packages"]]
        print(labels_and_scores)
    except:
        print(response_json)
        gr.Warning(response_json.get("error", f"Unknown err: {response_json}"))
        return image
    # Get all mask images
    mask_images={}
    for image_package in response_json["image_packages"]:
        mask_image = Image.open(BytesIO(base64.b64decode(image_package['mask'])))
        mask_images[image_package['label']] = mask_image
    
    result_image = auto_black_keywords(image, mask_images, keywords, reverse)
    return result_image