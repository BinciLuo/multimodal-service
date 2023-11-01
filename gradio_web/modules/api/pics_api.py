import json
import requests
from modules.utils.scripts_gen import form_alwayson_scripts_from_kwargv

with open("config/picture_process.json", 'r') as json_file:
    picture_process_info:dict = json.load(json_file)
with open("config/conf.json", 'r') as json_file:
    conf_info:dict = json.load(json_file)

def post_txt2img(query: str, loras:list[str]=[], **kwargv):
    """
    ## Send requests

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
    # ------------------------------------------------------
    # Begin check route and get loras
    if "route" not in picture_process_info["txt2img"].keys():
        return None,f"[SD] route of txt2img not found"
    for lora_name in loras:
            query += f" <lora:{lora_name}:{1/len(loras)}> "

    # ------------------------------------------------------
    # Begin load always on scripts
    alwayson_scripts, err_string = form_alwayson_scripts_from_kwargv(**kwargv)
    if err_string != None:
        return None, f"[SD] alwayson_scripts failed, {err_string}"
    
    # ------------------------------------------------------

    paras = {
        "init_images": kwargv.get("init_image_str",""),
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

    response = requests.post(conf_info["server_url"]+picture_process_info["txt2img"]["route"], data=json.dumps(paras))
    if response.status_code != 200:
        return None, f"[SD] txt2img failed"
    return response.json()['images'][0],None

def post_img2img(init_img_str:str ,query: str ,loras:list[str]=[], **kwargv):
    """
    ## Send requests

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
        image_str(str)
        err_string(str|None)
    ```
        
    """
    # ------------------------------------------------------
    # Begin check route and get loras
    if "route" not in picture_process_info["img2img"].keys():
        return None, f"[SD] route of img2img not found"
    for lora_name in loras:
            query += f" <lora:{lora_name}:{1/len(loras)}> "
    
    # ------------------------------------------------------
    # Begin load always on scripts
    alwayson_scripts, err_string = form_alwayson_scripts_from_kwargv(init_img_str=init_img_str ,**kwargv)
    if err_string != None:
        return None, f"[SD] alwayson_scripts failed, {err_string}"
    
    # ------------------------------------------------------
    # Begin set paras
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
    # Begin send request
    response = requests.post(conf_info["server_url"]+picture_process_info["img2img"]["route"], data=json.dumps(paras))
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
        response = requests.get(url=conf_info["server_url"]+picture_process_info["loras"]["route"])
        return response.json()["loras"],None
    except:
        return [],f'[SD] Get loras failed'
    