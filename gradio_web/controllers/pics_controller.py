import base64
from PIL import Image
from io import BytesIO
import gradio as gr
import io

from modules.api.pics_api import post_txt2img, post_img2img, form_post_txt2img_paras,form_post_img2img_paras


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
        gr.Warning(e)
        return None
    
    # ------------------------------------------------------
    # Get image from str and return
    image = Image.open(BytesIO(base64.b64decode(pic_string)))
    image_show = gr.Image(value=image ,type='pil')
    return image_show

def change_pic_process(init_img: Image, query: str, loras:list[str] = [], template = None):
    # ------------------------------------------------------
    # Check init_img and get init_img_str
    image_bytesio = io.BytesIO()
    if init_img == None:
        gr.Warning("No image provided.")
        return None
    init_img.save(image_bytesio, format="PNG")
    init_img_bytes = image_bytesio.getvalue()
    init_img_str = base64.b64encode(init_img_bytes).decode('utf-8')

    # ------------------------------------------------------
    # Form paras
    paras,e = form_post_img2img_paras(init_img_str, query, loras=loras, width=init_img.size[0], height=init_img.size[1],template = template)
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
    image_show = gr.Image(value=image ,type='pil')
    return image_show


