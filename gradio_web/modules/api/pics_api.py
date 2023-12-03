import base64
import functools
from io import BytesIO
import json
import sys
import time
import gradio as gr
from PIL import Image
import requests
from modules.utils.scripts_gen import form_alwayson_scripts_from_kwargv
from modules.utils.imaga_paras_gen import form_default_paras_from_template

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

def post_img2img(paras, source):
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
    Get loras through api
    """
    if "route" not in picture_process_info["loras"].keys():
        return [],f"[SD] route of loras not found"
    try:
        response = requests.get(url=SERVER_URL+picture_process_info["loras"]["route"])
        return response.json()["loras"],None
    except:
        return [],f'[SD] Get loras failed'


@functools.lru_cache
def post_hgface_img_segment(image: str):
    # ------------------------------------------------------
    # Begin check route
    if "route" not in picture_process_info["huggingface_img_segment"].keys():
        return None, f"[SD] route of huggingface_img_segment not found"
    route = picture_process_info["huggingface_img_segment"]["route"]

    # ------------------------------------------------------
    # Begin post, set max retry time 10
    for i in range(100):
        response = requests.post(SERVER_URL+route, data=json.dumps({"image": image}))
        print(response)
        try:
            err = response.json().get("error", None)
            if err != None:
                gr.Warning(f"🥲 Segment Error: {err}, retry {i+1}/10")
                time.sleep(3)
                continue
            gr.Info("😃 Get Segment Success!")
            return response.json(), None
        except:
            print(response)
            return None, f"Unknown err, {response}"
    return None, err