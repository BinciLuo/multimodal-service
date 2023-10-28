import json
import requests
from modules.utils.scripts_gen import form_alwayson_scripts_from_templates

with open("config/picture_process.json", 'r') as json_file:
    picture_process_info:dict = json.load(json_file)
with open("config/conf.json", 'r') as json_file:
    conf_info:dict = json.load(json_file)

def post_txt2img(query: str, loras:list[str]=[], width:int=512, height:int=512):
    if "route" not in picture_process_info["txt2img"].keys():
        return {"message": Exception},Exception("route of txt2img not found")
    
    for lora_name in loras:
            query += f" <lora:{lora_name}:{1/len(loras)}> "
    paras = {
        "prompt": query + "(recherche details) ,(ultra details),8k resolution,excellent quality,beautiful cinematic lighting,engaging atmosphere",
        "negative_prompt": "(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy",
        "sampler_index": "DPM++ 2M Karras",
        "seed": -1,
        "steps": 30,
        "width": width,
        "height": height,
        "cfg_scale": 5
    }
    response = requests.post(conf_info["server_url"]+picture_process_info["txt2img"]["route"], data=json.dumps(paras))
    return response.json()['images'][0],None

def post_img2img(init_img_str:str ,query: str ,loras:list[str]=[], **kwargv):
    """
    ## Send requests

    ## Argvs:
    ```
        init_img_str(str)
        query(str)
        loras(list[str]): list of lora name
    ```
    ## KWargvs:
    ```
        alwayson_scripts(dict)
        template(str): name of img gen template
        prompt(str)
        negative_prompt(str)
        denoising_strength(float)
        sampler_index(str)
        seed(int)
        steps(int)
        width(int)
        height(int)
        cfg_scale(int)
        alwayson_scripts(str)
    ```
    ## Return:
    ```
        str: image_str
    ```
        
    """
    # ------------------------------------------------------
    # Begin check route and get loras
    if "route" not in picture_process_info["img2img"].keys():
        return {"message": Exception},Exception("route of img2img not found")
    for lora_name in loras:
            query += f" <lora:{lora_name}:{1/len(loras)}> "
    
    # ------------------------------------------------------
    # Begin load always on scripts
    ## if key "alwayson_scripts" in kwargv, use it.
    alwayson_scripts = kwargv.get("alwayson_scripts", None)
    ## if alwayson_scripts not in kwargv and key "templates" in kwargv, use template
    template = kwargv.get("template", None)
    if template != None and alwayson_scripts == None :    
        alwayson_scripts = form_alwayson_scripts_from_templates(template_name=template, init_img_str=init_img_str)
    ## if "alwayson_scripts" and "templates" not in kwargv use default {}
    if alwayson_scripts == None:
        alwayson_scripts= {}
    
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
        return None,Exception(f"post_img2img failed, status code{response.status_code}")
    
    
def get_loras():
    """
    Get loras through api
    """
    if "route" not in picture_process_info["loras"].keys():
        return {"message": Exception},Exception("route of loras not found")
    response = requests.get(url=conf_info["server_url"]+picture_process_info["loras"]["route"])
    return response.json()["loras"]
    