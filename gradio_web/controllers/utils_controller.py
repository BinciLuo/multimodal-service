import json
import gradio as gr
import threading
import time

from modules.utils.check_server_status import  check_chat_api_chat, check_sd_api_img2img, check_sd_api_loras, check_sd_api_txt2img


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
    