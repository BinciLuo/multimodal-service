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

def txt2img(query: str, loras:list[str]=[], width:int=512, height:int=512):
    if "route" not in picture_process_info["txt2img"].keys():
        return {"message": Exception},Exception("route of model not found")
    
    # TODO : Change this from hard code to template file
    # form post paras
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
    response=requests.post(conf_info["server_url"]+picture_process_info["txt2img"]["route"], data=json.dumps(paras))
    return response.json()['images'][0],None
    
    
    