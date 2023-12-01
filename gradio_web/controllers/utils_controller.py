import json
import gradio as gr
import threading
import time
from PIL import Image

from modules.utils.check_server_status import  check_chat_api_chat, check_sd_api_img2img, check_sd_api_loras, check_sd_api_txt2img
from modules.utils.colors import generate_mask_from_rgb
from modules.utils.img_segment import get_mask_by_blackpoints,replace_black_pixels


def check_status_process():
    err_info_list = []
    test_funcs = [
        check_chat_api_chat,
        check_sd_api_loras,
        check_sd_api_img2img,
        check_sd_api_txt2img
        ]
    # 创建线程
    threads_list= [threading.Thread(target=test_func, args=(err_info_list,)) for test_func in test_funcs]

    # 启动线程
    for each_thread in threads_list:
        each_thread.start()

    # 等待2s
    time.sleep(2.5)

    print(err_info_list)

    for err_info in err_info_list:
        gr.Warning('🤡'+err_info.upper()+'🥲')

def submit_mask_process(painted):
    new_editor = gr.ImageEditor(value={"background":painted["composite"],"layers":[],"composite":None}, label='Edit', type='pil', interactive=True)
    return generate_mask_from_rgb(painted['composite']), new_editor

def send_to_editor_process(base_img):
    new_editor = gr.ImageEditor(value={"background":replace_black_pixels(base_img),"layers":[],"composite":None}, label='Edit', type='pil', interactive=True)
    return new_editor

def auto_mask_process(painted):
    composite_img = painted["composite"]
    auto_mask_img = get_mask_by_blackpoints(composite_img)
    new_editor = gr.ImageEditor(value={"background":auto_mask_img,"layers":[],"composite":None}, label='Edit', type='pil', interactive=True)
    return new_editor
