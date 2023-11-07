import base64
from io import BytesIO
import json
import sys
from PIL import Image
import requests
from modules.utils.scripts_gen import form_alwayson_scripts_from_kwargv

from const import *

def post_txt2img(paras):
    
    # ------------------------------------------------------
    # Begin check route and get loras
    if "route" not in picture_process_info["txt2img"].keys():
        return None,f"[SD] route of txt2img not found"
    
    # ------------------------------------------------------
    # Begin send request
    response = requests.post(SERVER_URL+picture_process_info["txt2img"]["route"], data=json.dumps(paras))
    if response.status_code != 200:
        return None, f"[SD] txt2img failed"
    return response.json()['images'][0],None

def post_img2img(paras):
    # ------------------------------------------------------
    # Begin check route
    if "route" not in picture_process_info["img2img"].keys():
        return None, f"[SD] route of img2img not found"
    
    # ------------------------------------------------------
    # Begin send request
    response = requests.post(SERVER_URL+picture_process_info["img2img"]["route"], data=json.dumps(paras))
    try:
        return response.json()['images'][0],None
    except:    
        return None,f"[SD] img2img failed"
       
def get_loras():
    """
    Get loras through api
    """
    if "route" not in picture_process_info["loras"].keys():
        return [],f"[SD] route of loras not found"
    try:
        response = requests.get(url=SERVER_URL+picture_process_info["loras"]["route"])
        return response.json()["loras"],None
    except:
        return [],f'[SD] Get loras failed'

def form_post_txt2img_paras(query: str, loras:list[str]=[], **kwargv):
    """
    ## Form paras for post_txt2img

    ## Argvs:
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
    ## Return:
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
        "steps": kwargv.get("steps",40),
        "width": kwargv.get("width",512),
        "height": kwargv.get("height",512),
        "cfg_scale": kwargv.get("cfg_scale",5),
        "alwayson_scripts": alwayson_scripts,
    }

    return paras, None
    
def form_post_img2img_paras(init_img_str:str ,query: str ,loras:list[str]=[], **kwargv):
    """
    ## Form paras for post_img2img

    ## Argvs:
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
    ```
    ## Return:
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
    # Set paras
    paras = {
        "init_images": [init_img_str],
        "prompt": query + kwargv.get("prompt", ",(recherche details) ,(ultra details),8k resolution,excellent quality,beautiful cinematic lighting,engaging atmosphere"), # TODO : remove this hard code
        "negative_prompt": kwargv.get("negative_prompt", "(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy"), # TODO : remove this hard code
        "denoising_strength": kwargv.get("denoising_strength", 0.2),
        "sampler_index": kwargv.get("sampler_index", "DPM++ 2M Karras"),
        "seed": kwargv.get("seed", -1),
        "steps": kwargv.get("steps",40),
        "width": kwargv.get("width",512),
        "height": kwargv.get("height",512),
        "cfg_scale": kwargv.get("cfg_scale",5),
        "alwayson_scripts": alwayson_scripts,
    }

    # ------------------------------------------------------
    return paras, None