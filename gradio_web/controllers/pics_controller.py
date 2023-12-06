import base64
from PIL import Image
from io import BytesIO
import gradio as gr
import io

from modules.api.pics_api import post_txt2img, post_img2img
from modules.utils.imaga_paras_gen import form_post_txt2img_paras, form_post_img2img_paras
from modules.utils.image_io import trans_image_to_str, trans_str_to_image
from modules.utils.colors import convert_unblack_to_white

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
    image_show = gr.Image(value=image , type='pil')
    return image_show

def change_pic_process(init_img: Image, query: str, loras:list[str] = [], template = None, mask_img: Image = None, image_editor: dict = None):
    # ------------------------------------------------------
    # Check init_img and get init_img_str and get size
    size = init_img.size
    init_img_str = trans_image_to_str(init_img)

    # ------------------------------------------------------
    # Check mask_img and get mask_img_str
    if mask_img !=None and mask_img.size != init_img.size:
        gr.Warning(f"Mask image size {mask_img.size} not equals init image size {init_img.size}")
        return None
    if mask_img == None:
        if template != "beauty" and template != "face":
            gr.Warning(f"Mask is None, if you're using DALL-E, the full image will change")
        mask_img = Image.new("RGBA", init_img.size, (0, 0, 0, 0))

    binary_image = convert_unblack_to_white(image_editor["background"])
    binary_image.save("binary_image.png")    
    black_img_str = trans_image_to_str(binary_image)
    
    mask_img_str = trans_image_to_str(mask_img)
    

    # ------------------------------------------------------
    # Form paras
    paras, e = form_post_img2img_paras(init_img_str, 
                                       query, 
                                       loras=loras, 
                                       width=init_img.size[0], 
                                       height=init_img.size[1], 
                                       template = template, 
                                       mask_img_str = mask_img_str, 
                                       black_img_str = black_img_str)
    if e != None:
        gr.Warning(e)
        return init_img
    
    # ------------------------------------------------------
    # Use api post_img2img
    pic_string, e = post_img2img(paras, source = paras["source"])
    if e != None:
        if template == "inpaintSD":
            gr.Warning(e+" \nFallback to DALLE")
            paras["source"] = "DALLE"
            pic_string, e = post_img2img(paras, source = paras["source"])
        if e != None:
            gr.Warning(f"{e} \nSkip {template}")
            return init_img
    
    # ------------------------------------------------------
    # Get image from str and return
    image = trans_str_to_image(pic_string)
    image = image.resize(size)
    return image

def set_base_image(edited_img: Image):
    return edited_img
