import json
import sys
import gradio as gr
import threading
import time

from modules.api.chat_api import post_chat
from modules.api.pics_api import get_loras, post_img2img, post_txt2img
from modules.utils.image_paras_gen import form_post_txt2img_paras, form_post_img2img_paras

from const import *


## Chat
def each_chat_check(model_name: str, err_info_list: list):
    _, e = post_chat(model_name, '123', SERVER_URL, [])
    if e != None:
        err_info_list.append(e)

def check_chat_api_chat(err_info_list: list):
    threads_list = [threading.Thread(target=each_chat_check, args=(model_name, err_info_list)) for model_name in model_info.keys() ] 
    for each_thread in threads_list:
        each_thread.start()
    time.sleep(1)
        


## SD
def check_sd_api_loras(err_info_list: list):
    _, e = get_loras()
    if e != None:
        err_info_list.append(e)

def check_sd_api_txt2img(err_info_list: list):
    paras, e = form_post_txt2img_paras('',[])
    if e != None:
        err_info_list.append(e)
    _, e = post_txt2img(paras)
    if e != None:
        err_info_list.append(e)

def check_sd_api_img2img(err_info_list: list):
    with open("tests/test_img.txt",'r') as f:
        init_img_str = f.read()
    
    paras, e = form_post_img2img_paras(init_img_str,'',[])
    if e != None:
        err_info_list.append(e)
    _, e = post_img2img(paras, source='SD')
    if e != None:
        err_info_list.append(e)

    
    
    

