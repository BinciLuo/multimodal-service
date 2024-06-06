import functools
import json
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import torch.nn as nn
import numpy as np
import io
import base64

def has_pure_white_pixel(image):
    # 获取图像的像素数据
    pixels = list(image.getdata())
    
    # 检查是否存在纯白像素 (255, 255, 255)
    for pixel in pixels:
        if pixel == 255:
            return True
    
    return False

# Load model
try:
    processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes",local_files_only=True)
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes",local_files_only=True)
except:
    processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")

# Define the class labels
class_labels = {
    "0": "Background",
    "1": "Hat",
    "2": "Hair",
    "3": "Sunglasses",
    "4": "Upper-clothes",
    "5": "Skirt",
    "6": "Pants",
    "7": "Dress",
    "8": "Belt",
    "9": "Left-shoe",
    "10": "Right-shoe",
    "11": "Face",
    "12": "Left-leg",
    "13": "Right-leg",
    "14": "Left-arm",
    "15": "Right-arm",
    "16": "Bag",
    "17": "Scarf"
}

def get_mask_data_json(image: Image.Image):
    inputs = processor(images=image, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0]
    pred_seg_np = pred_seg.numpy()

    masks = []
    for label_id, label_name in class_labels.items():
        mask = (pred_seg_np == int(label_id)).astype(np.uint8)
        pil_image = Image.fromarray(mask * 255)
        if not has_pure_white_pixel(pil_image):
            continue
        image_stream = io.BytesIO()
        pil_image.save(image_stream, format="PNG")
        base64_image = base64.b64encode(image_stream.getvalue()).decode("utf-8")
        label_info = {
            "score": 1,
            "label": label_name,
            "mask": base64_image,
        }
        masks.append(label_info)

    output_json = "output_masks.json"
    with open(output_json, "w") as json_file:
        json.dump(masks, json_file, indent=2)

    return {"image_packages":masks}
