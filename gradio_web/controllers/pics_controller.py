import base64
from PIL import Image
from io import BytesIO
import gradio as gr
import io

from modules.api.pics_api import post_txt2img, post_img2img




def generate_pic_process(query: str, loras:list[str]=[], width:int=512, height:int = 512):
    pic_string, e = post_txt2img(query, loras=loras, width=512, height=512)
    #image = Image.open(BytesIO(pic_string.encode('utf-8')))
    image = Image.open(BytesIO(base64.b64decode(pic_string)))
    image_show = gr.Image(value=image ,type='pil')
    return image_show

def change_pic_process(init_img: Image, query: str, loras:list[str] = [], template = None):
    image_bytesio = io.BytesIO()
    init_img.save(image_bytesio, format="PNG")
    init_img_bytes = image_bytesio.getvalue()
    init_img_str = base64.b64encode(init_img_bytes).decode('utf-8')

    pic_string, e = post_img2img(init_img_str, query, loras=loras, width=init_img.size[0], height=init_img.size[1],template = template)
    if e!=None:
        return gr.Image(value=init_img ,type='pil')
    image = Image.open(BytesIO(base64.b64decode(pic_string)))
    image_show = gr.Image(value=image ,type='pil')
    return image_show


