import base64
from PIL import Image
from io import BytesIO
import gradio as gr
import io

from modules.api.pics_api import post_txt2img, post_img2img, form_post_txt2img_paras,form_post_img2img_paras

base_image = None

def generate_pic_process(query: str, loras:list[str]=[], width:int=512, height:int = 512):
    # ------------------------------------------------------
    # Form paras
    paras, e = form_post_txt2img_paras(query, loras=loras, width=width, height=height)
    if e != None:
        gr.Warning(e)
        return None
    
    # ------------------------------------------------------
    # Use api post_txt2img
    pic_string, e = post_txt2img(paras)
    if e != None:
        gr.Warning(e + "Set example image")
        example_image = Image.open("example/images.jpeg")
        return example_image
    
    # ------------------------------------------------------
    # Get image from str and return
    image = Image.open(BytesIO(base64.b64decode(pic_string)))
    image_show = gr.Image(value=image ,type='pil')
    return image_show


def change_pic_process(init_img: Image, query: str, loras:list[str] = [], template = None, mask_img: Image = None):
    # ------------------------------------------------------
    # Check init_img and get init_img_str and get size
    size = init_img.size
    image_bytesio = io.BytesIO()
    if init_img == None:
        gr.Warning("No image provided.")
        return None
    init_img.save(image_bytesio, format="PNG")
    init_img_bytes = image_bytesio.getvalue()
    init_img_str = base64.b64encode(init_img_bytes).decode('utf-8')

    # ------------------------------------------------------
    # Check mask_img and get mask_img_str
    image_bytesio = io.BytesIO()
    if mask_img !=None and mask_img.size != init_img.size:
        gr.Warning(f"Mask image size {mask_img.size} not equals init image size {init_img.size}")
        return None
    if mask_img == None:
        gr.Warning(f"Mask is None, so the full image will change")
        mask_img = Image.new("RGBA", init_img.size, (0, 0, 0, 0))
    mask_img.save(image_bytesio, format="PNG")
    mask_img_bytes = image_bytesio.getvalue()
    mask_img_str = base64.b64encode(mask_img_bytes).decode('utf-8')

    # ------------------------------------------------------
    # Form paras
    paras,e = form_post_img2img_paras(init_img_str, query, loras=loras, width=init_img.size[0], height=init_img.size[1],template = template, mask_img_str = mask_img_str)
    if e != None:
        gr.Warning(e)
        return gr.Image(value=init_img ,type='pil')
    
    # ------------------------------------------------------
    # Use api post_img2img
    pic_string, e = post_img2img(paras)
    if e != None:
        gr.Warning(e)
        return gr.Image(value=init_img ,type='pil')
    
    # ------------------------------------------------------
    # Get image from str and return
    image = Image.open(BytesIO(base64.b64decode(pic_string)))
    image = image.resize(size)
    image_show = gr.Image(value=image ,type='pil')
    return image_show

def set_base_image(edited_img: Image):
    return edited_img
