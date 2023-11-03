import json
import sys
import gradio as gr
import threading
import time

from modules.api.chat_api import chat
from modules.api.pics_api import get_loras,post_img2img,post_txt2img

from const import *


## Chat
def each_chat_check(model_name, err_info_list):
    _, err_string = chat(model_name, '123', SERVER_URL)
    if err_string != None:
        err_info_list.append(err_string)

def check_chat_api_chat(err_info_list):
    threads_list = [threading.Thread(target=each_chat_check, args=(model_name, err_info_list)) for model_name in model_info.keys() ] 
    for each_thread in threads_list:
        each_thread.start()
    time.sleep(1)
        


## SD
def check_sd_api_loras(err_info_list):
    _, err_string = get_loras()
    if err_string != None:
        err_info_list.append(err_string)

def check_sd_api_txt2img(err_info_list):
    _, err_string = post_txt2img('',[])
    if err_string != None:
        err_info_list.append(err_string)

def check_sd_api_img2img(err_info_list):
    with open("tests/test_img.txt",'r') as f:
        init_img_str = f.read()
    
    _, err_string = post_img2img(init_img_str,'',[])
    if err_string != None:
        err_info_list.append(err_string)

    
    
    

