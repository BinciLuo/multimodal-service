import base64
from io import BytesIO
import json
from const import *
from PIL import Image
from modules.utils.scripts_gen import form_alwayson_scripts_from_kwargv

with open("config/sd_templates.json", 'r') as json_file:
    templates_dict:dict = json.load(json_file)

def form_post_txt2img_paras(query: str, loras:list[str]=[], **kwargv):
    """
    ### Form paras for post_txt2img

    ### Argvs:
    ```
        query(str)
        loras(list[str]): list of lora name

        init_img_str(str|None)
        alwayson_scripts(dict|None)
        template(str|None): name of img gen template
        prompt(str|None)
        negative_prompt(str|None)
        denoising_strength(float|None)
        sampler_index(str|None)
        seed(int|None)
        steps(int|None)
        width(int|None)
        height(int|None)
        cfg_scale(int|None)
        alwayson_scripts(str|None)
    ```
    ### Return:
    ```
        image_str(str)
        err_string(str|None)
    ```
        
    """
    # Load loras to query
    for lora_name in loras:
        query += f" <lora:{lora_name}:{1/len(loras)}> "

    # ------------------------------------------------------
    # Load always on scripts
    alwayson_scripts, e = form_alwayson_scripts_from_kwargv(**kwargv)
    if e != None:
        return None, f"[SD] alwayson_scripts failed, {e}"
    
    # ------------------------------------------------------
    # Set paras
    paras = {
        "prompt": query + kwargv.get("prompt", ",(recherche details) ,(ultra details),8k resolution,excellent quality,beautiful cinematic lighting,engaging atmosphere"), # TODO : remove this hard code
        "negative_prompt": kwargv.get("negative_prompt", "(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy"), # TODO : remove this hard code
        "denoising_strength": kwargv.get("denoising_strength", 0.2),
        "sampler_index": kwargv.get("sampler_index", "DPM++ 2M Karras"),
        "seed": kwargv.get("seed", -1),
        "steps": kwargv.get("steps", 40),
        "width": kwargv.get("width", 512),
        "height": kwargv.get("height", 512),
        "cfg_scale": kwargv.get("cfg_scale", 5),
        "alwayson_scripts": alwayson_scripts,
    }

    return paras, None
    
def form_post_img2img_paras(init_img_str:str , query: str , loras:list[str]=[], **kwargv):
    """
    ### Form paras for post_img2img
    ### Warning: paras will first search in kwargv and then templace and then default.

    ### Argvs:
    ```
        init_img_str(str)
        query(str)
        loras(list[str]): list of lora name

        alwayson_scripts(dict|None)
        template(str|None): name of img gen template
        prompt(str|None)
        negative_prompt(str|None)
        denoising_strength(float|None)
        sampler_index(str|None)
        seed(int|None)
        steps(int|None)
        width(int|None)
        height(int|None)
        cfg_scale(int|None)
        alwayson_scripts(str|None)

        inpainting_fill(int|None): masked area, 0:fill and 1: origin
        inpaint_full_res(bool|None): inpaint area, False: whole picture and  True: only masked
        inpaint_full_res_padding(int|None): Only masked padding, pixels 32
        inpainting_mask_invert(int|None): 0: change white 1: change black
        mask_blur(int|None): mask blur index,
        mask(str|None): black-white mask image string for SD
        mask_img_str(str|None): mask image string for DALLE
        source(str|None): model source

    ```
    ### Return:
    ```
        paras(dict)
        err_string(str|None)
    ```
        
    """
    # ------------------------------------------------------
    # Check if init_img_str valid
    if init_img_str == None:
        return None, f"No init image"
    try:
        image = Image.open(BytesIO(base64.b64decode(init_img_str)))
    except:
        return None, f"Invalid init image"
    
    # ------------------------------------------------------
    # Load loras to query
    for lora_name in loras:
        query += f" <lora:{lora_name}:{1/len(loras)}> "

    # ------------------------------------------------------
    # Load alwayson_scripts
    alwayson_scripts, e = form_alwayson_scripts_from_kwargv(init_img_str=init_img_str ,**kwargv)
    if e != None:
        return None, f"{e}"
    
    # ------------------------------------------------------
    # Load template paras
    template_paras, e = form_default_paras_from_template(**kwargv)
    if e != None:
        return None, f"{e}"
    
    # ------------------------------------------------------
    # Set paras
    # For each para, if it is not given in kwargv, it will search template. If template is not available, it will set to default
    default_paras = IMG2IMG_DEFAULT_PARAS
    paras = {
        "init_images": [init_img_str],
        "prompt": kwargv.get("prompt", template_paras.get("prompt", None)),
        "negative_prompt": kwargv.get("negative_prompt", template_paras.get("negative_prompt", None)),
        "denoising_strength": template_paras.get("denoising_strength", kwargv.get("denoising_strength", None)),
        # FIXME: Search in template_paras first
        #"denoising_strength": kwargv.get("denoising_strength", template_paras.get("denoising_strength", None)),
        "sampler_index": kwargv.get("sampler_index", template_paras.get("sampler_index", None)),
        "seed": kwargv.get("seed", template_paras.get("seed", None)),
        "steps": kwargv.get("steps", template_paras.get("steps", None)),
        "width": kwargv.get("width", template_paras.get("width", None)),
        "height": kwargv.get("height", template_paras.get("height", None)),
        "cfg_scale": kwargv.get("cfg_scale", template_paras.get("cfg_scale", None)),
        "restore_faces": kwargv.get("restore_faces", template_paras.get("restore_faces", None)),
        "alwayson_scripts": alwayson_scripts,

        "inpainting_fill": kwargv.get("inpainting_fill", template_paras.get("inpainting_fill", None)),
        "inpaint_full_res": kwargv.get("inpaint_full_res", template_paras.get("inpaint_full_res", None)),
        "inpaint_full_res_padding": kwargv.get("inpaint_full_res_padding", template_paras.get("inpaint_full_res_padding", None)),
        "inpainting_mask_invert": kwargv.get("inpainting_mask_invert", template_paras.get("inpainting_mask_invert", None)),
        "mask_blur": 4,
        "mask": kwargv.get("black_img_str", template_paras.get("black_image", None)),
        "mask_image": kwargv.get("mask_img_str", template_paras.get("mask_image", None)),
        "source": kwargv.get("source", template_paras.get("source", None))
    }

    template_name = kwargv.get("template", None)
    if template_name != "inpaintSD":
        paras["mask"] = None 
        

    for key in IMG2IMG_DEFAULT_PARAS.keys():
        paras[key] = paras[key] if paras.get(key, None) != None else default_paras[key]
        if key == "prompt":
            paras[key] = f"({query}:2)" + paras[key]
    
    # ------------------------------------------------------
    return paras, None

def form_default_paras_from_template(**kwargv):
    template_name = kwargv.get("template", None)
    if template_name != None:
        template = templates_dict.get(template_name, {})
    else:
        return {}, None
    
    template_paras = {
        "prompt": template.get("prompt", None),
        "negative_prompt": template.get("negative_prompt", None),
        "denoising_strength": template.get("denoising_strength", None),
        "sampler_index": template.get("sampler_index", None),
        "seed": template.get("seed", None),
        "steps": template.get("steps", None),
        "width": template.get("width", None),
        "height": template.get("height", None),
        "cfg_scale": template.get("cfg_scale", None),

        "mask": template.get("mask", None),
        "inpainting_fill":template.get("inpainting_fill", None),
        "inpaint_full_res": template.get("inpaint_full_res", None),
        "inpaint_full_res_padding": template.get("mask", None),
        "inpainting_mask_invert": template.get("inpainting_mask_invert", None),
        "mask_blur": template.get("mask_blur", None),
        "mask_image": template.get("mask_image", None),
        "source": template.get("source", None)
    }

    return template_paras, None