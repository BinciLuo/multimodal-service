import base64
from io import BytesIO
import io
import numpy as np
import requests
from PIL import Image
import gradio as gr

from modules.api.pics_api import post_hgface_img_segment
from modules.utils.image_io import trans_image_to_str

def replace_black_pixels(image: Image):
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

def auto_fill_by_blackpoints(image: Image,init_img: Image):    
    init_img_str = trans_image_to_str(init_img)
    # Post huggingface models and check
    response_json, err = post_hgface_img_segment(init_img_str)
    if err != None:
        # clear cache
        post_hgface_img_segment.cache_clear()
        print(err)
        gr.Warning(err+". Cache cleared")
        return image
    try:
        labels_and_scores = [(image_package['label'],image_package['score']) for image_package in response_json["image_packages"]]
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
    
    result_image = auto_fill_black(image, mask_images)
    return result_image

def auto_black_keywords(image: Image, mask_images: dict, keys_words: list[str], reverse: bool):
    # 将原始图像转换为NumPy数组
    original_array = np.array(image)
    # 打开所有L模式的图像
    if reverse == False:
        l_images = [mask_images[key] for key in keys_words if key in mask_images.keys()]
    else:
        l_images = [mask_images[key] for key in mask_images.keys() if key not in keys_words]
    # 将L模式的图像转换为NumPy数组
    l_arrays = [np.array(l_image) for l_image in l_images]
    # 找到L模式的图像中值为255的像素点
    l_pixels_255 = [l_array == 255 for l_array in l_arrays]
    # 在原始图像中将对应位置的像素值设置为纯黑色（0）
    for l_pixel_255 in l_pixels_255:
        original_array[l_pixel_255] = 0
        try:
            original_array[l_pixel_255] = [ 0, 0, 0, 255]
        except:
            original_array[l_pixel_255] = [ 0, 0, 0]
    # 创建新的图像对象
    result_image = Image.fromarray(original_array)
    # 返回处理后的图像
    return result_image

def auto_black_by_keywords(image: Image, init_img: Image, keywords: list[str], reverse: bool):
    init_img_str = trans_image_to_str(init_img)
    # Post huggingface models and check
    response_json, err = post_hgface_img_segment(init_img_str)
    if err != None:
        # clear cache
        post_hgface_img_segment.cache_clear()
        print(err)
        gr.Warning(err+". Cache cleared")
        return image
    try:
        labels_and_scores = [(image_package['label'],image_package['score']) for image_package in response_json["image_packages"]]
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