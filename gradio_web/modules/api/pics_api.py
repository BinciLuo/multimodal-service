import json
import requests

# {
#     "prompt": "city of stars",
#     "negative_prompt": "",
#     "sampler_index": "Euler a",
#     "seed": 1234,
#     "steps": 20,
#     "width": 512,
#     "height": 512,
#     "cfg_scale": 8
# }

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

# def post_img2img(init_img_str:str ,query: str, alwaysalwayson_scripts:list[tuple(str,dict)]=[],loras:list[str]=[], width:int=512, height:int=512):
def post_img2img(init_img_str:str ,query: str ,loras:list[str]=[], width:int=512, height:int=512, **kwargv):
    if "route" not in picture_process_info["img2img"].keys():
        return {"message": Exception},Exception("route of img2img not found")
    for lora_name in loras:
            query += f" <lora:{lora_name}:{1/len(loras)}> "

    # load scripts, default controlnet only
    alwaysalwayson_scripts = kwargv.get("alwaysalwayson_scripts", None)
    if alwaysalwayson_scripts == None:
        alwayson_scripts= {
            "controlnet":{
                "args":[
                    {
                        "module":"canny",
                        "model":"coadapter-canny-sd15v1 [0f01fb68]",
                        "input_image":init_img_str,
                        "threshold_a":10,
                        "threshold_b":100,
                    }
                ]
                }
            }
        
    # TODO: move paras to **kwargv
    paras = {
        "init_images": [init_img_str],
        "prompt": query + ",(recherche details) ,(ultra details),8k resolution,excellent quality,beautiful cinematic lighting,engaging atmosphere",
        "negative_prompt": "(worst quality, low quality, cgi, bad eye, worst eye, illustration, cartoon),deformed,distorted,disfigured,poorly drawn,bad anatomy,wrong anatomy",
        "denoising_strength": 0.2,
        "sampler_index": "DPM++ 2M Karras",
        "seed": -1,
        "steps": 40,
        "width": width,
        "height": height,
        "cfg_scale": 5,
        "alwayson_scripts": alwayson_scripts,
    }
    response = requests.post(conf_info["server_url"]+picture_process_info["img2img"]["route"], data=json.dumps(paras))
    return response.json()['images'][0],None
    
    
    
def get_loras():
    if "route" not in picture_process_info["loras"].keys():
        return {"message": Exception},Exception("route of loras not found")
    response = requests.get(url=conf_info["server_url"]+picture_process_info["loras"]["route"])
    return response.json()["loras"]
    