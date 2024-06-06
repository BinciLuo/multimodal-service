import base64
import functools
import json
import time
import gradio as gr
from PIL import Image
import requests
from modules.utils.scripts_gen import form_alwayson_scripts_from_kwargv
from modules.utils.image_paras_gen import form_default_paras_from_template
from modules.utils.image_io import trans_str_to_image

from const import *
if SEG_MODEL_ENV == 'local':
    from modules.utils.model import get_mask_data_json

def post_txt2img(paras: dict):
    
    # ------------------------------------------------------
    # Begin check route and get loras
    if "route" not in picture_process_info["txt2img"].keys():
        return None, f"[SD] route of txt2img not found"
    
    # ------------------------------------------------------
    # Begin send request
    response = requests.post(SERVER_URL+picture_process_info["txt2img"]["route"], data=json.dumps(paras))
    if response.status_code != 200:
        return None, f"[SD] txt2img failed"
    return response.json()['images'][0], None

def post_img2img(paras: dict, source: str):
    """
    ### This function posts img2img models
    ### Argvs
    ```
        paras(dict): post paras
        source(str): which model to post, enum ['SD','DALLE']
    ```
    ### Return
    ```
        image_string(str| None): base64 string of image, None if post gets error
        err(str|None): error message
    ```
    """
    # ------------------------------------------------------
    # log paras
    print("------------------POST IMG2IMG------------------------")
    for key in paras.keys():
        if key not in ["init_images","mask","mask_image","alwayson_scripts"]:
            print(f"{key}: {paras[key]}")
    print("------------------------------------------------------\n\n")
    # ------------------------------------------------------
    # Begin check route
    if "route" not in picture_process_info["img2img"].keys():
        return None, f"[SD] route of img2img not found"
    
    # ------------------------------------------------------
    # Begin send request
    if source == "SD":
        response = requests.post(SERVER_URL+picture_process_info["img2img"]["route"], data=json.dumps(paras))
        try:
            return response.json()['images'][0], None
        except:
            return None, f"[IMG] SD failed."
    if source == "DALLE":
        response = requests.post(SERVER_URL+picture_process_info["dall-e-2_img2img"]["route"], data=json.dumps(paras))
        try:
            return response.json()["images"][0], None
        except:
            print(response)
            return None, f"[IMG] DALLE failed."
    if source == "Tencent":
        response = requests.post(SERVER_URL+picture_process_info["tencent_cloud_img2img"]["route"], data=json.dumps(paras))
        try:
            return response.json()["Response"]["ResultImage"], None
        except:
            return None, f"[IMG] Tencent cloud failed."
    return None, f"[IMG] Source {source} is not one of ['SD','DALLE','Tencent']"
       
def get_loras():
    """
    ### Get lora list from SD server
    ### Return
    ```
        lora_list(list[str]| []): list or loras, [] if error occurs
        err(str): error message
    ```
    """
    if "route" not in picture_process_info["loras"].keys():
        return [], f"[SD] route of loras not found"
    try:
        response = requests.get(url=SERVER_URL+picture_process_info["loras"]["route"])
        return response.json()["loras"], None
    except:
        return [], f'[SD] Get loras failed'


@functools.lru_cache
def post_hgface_img_segment(image: str):
    """
    ### This function posts image segment model in huggingface
    ### Argvs
    ```
        image(str): base64 image string 
    ```
    ### Return
    ```
        mask_packages(list[dict]| None): list of mask packages, {"mask": str, "label": str, "socre": float}
        error(str| None): error message
    ```
    """
    if SEG_MODEL_ENV == 'local':
        try:
            return get_mask_data_json(trans_str_to_image(image)), None
        except:
            gr.Warning("Local segment model not availible, fallback to api.")
        

    # ------------------------------------------------------
    # Begin check route
    if "route" not in picture_process_info["huggingface_img_segment"].keys():
        return None, f"[SD] route of huggingface_img_segment not found"
    route = picture_process_info["huggingface_img_segment"]["route"]

    # ------------------------------------------------------
    # Begin post, set max retry time 10
    for i in range(10):
        try:
            response = requests.post(SERVER_URL+route, data=json.dumps({"image": image}))
        except Exception as e:
            return None, str(e)
        print(response)
        try:
            err = response.json().get("error", None)
            if err != None:
                gr.Warning(f"🥲 Segment Error: {err}, retry {i+1}/10")
                time.sleep(5)
                continue
            gr.Info("😃 Get Segment Success!")
            return response.json(), None
        except:
            print(response)
            return None, f"Unknown err, {response}"
    return None, err