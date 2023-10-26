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
        "prompt": query,
        "negative_prompt": "",
        "sampler_index": "Euler a",
        "seed": 1234,
        "steps": 20,
        "width": width,
        "height": height,
        "cfg_scale": 8
    }
    response = requests.post(conf_info["server_url"]+picture_process_info["txt2img"]["route"], data=json.dumps(paras))
    return response.json()['images'][0],None

def post_img2img(init_img_str:str ,query: str, loras:list[str]=[], width:int=512, height:int=512):
    if "route" not in picture_process_info["img2img"].keys():
        return {"message": Exception},Exception("route of img2img not found")
    for lora_name in loras:
            query += f" <lora:{lora_name}:{1/len(loras)}> "
    paras = {
        "init_images": [init_img_str],
        "prompt": query,
        "negative_prompt": "",
        "sampler_index": "Euler a",
        "seed": 1234,
        "steps": 20,
        "width": width,
        "height": height,
        "cfg_scale": 8
    }
    response = requests.post(conf_info["server_url"]+picture_process_info["img2img"]["route"], data=json.dumps(paras))
    return response.json()['images'][0],None
    
    
    
def get_loras():
    if "route" not in picture_process_info["loras"].keys():
        return {"message": Exception},Exception("route of loras not found")
    response = requests.get(url=conf_info["server_url"]+picture_process_info["loras"]["route"])
    return response.json()["loras"]
    