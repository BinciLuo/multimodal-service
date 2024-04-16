import gradio as gr
import threading
import time
from PIL import Image

from modules.utils.check_server_status import  check_chat_api_chat, check_sd_api_img2img, check_sd_api_loras, check_sd_api_txt2img
from modules.utils.image_processing import generate_mask_from_black
from modules.utils.image_segment import auto_fill_by_blackpoints, replace_black_pixels
from modules.api.pics_api import post_hgface_img_segment
from modules.utils.image_io import trans_image_to_str
from controllers.chat_controllers import history, commands
from modules.utils.data_gen import *

last_editor = []

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

def submit_mask_process(painted: dict):
    return generate_mask_from_black(painted['composite']), {"background":painted["composite"],"layers":[],"composite":None}

def change_base_image_process(base_img, chatbot):
    base_img_str = trans_image_to_str(base_img) if base_img != None else None
    if base_img_str != None:
        response_json, err = post_hgface_img_segment(base_img_str)
        if err != None:
            gr.Warning(err)
        if err == None:
            labels = [image_package['label'] for image_package in response_json["image_packages"]]
            msg = "分割得到的标签有:"
            for i, label in enumerate(labels):
                msg += f"\n{i+1}. {label}"
            chatbot.append(("我更改了图片，新的图片有哪些部分？",""))
            global history
            history.clear()
            history.append(("我更改了图片，新的图片有哪些部分？", msg))
            chatbot[-1] = ("我更改了图片，新的图片有哪些部分？", msg)
    new_editor_dict = {"background":replace_black_pixels(base_img),"layers":[],"composite":None}
    global last_editor
    last_editor = [{"background":replace_black_pixels(base_img),"layers":[],"composite":None}]
    global commands
    commands.clear()

    return new_editor_dict, chatbot, gr.Dropdown(choices=[f'操作为: {cmd["command"]} 参数为: {cmd["paras"]}' for cmd in commands], type='index', label="command", multiselect=True)

def auto_mask_process(painted: dict, init_img: Image.Image):
    global last_editor
    last_editor.append(painted)
    composite_img = painted["composite"]
    auto_mask_img = auto_fill_by_blackpoints(composite_img, init_img)
    print(auto_mask_img.mode)
    new_editor_dict = {"background":auto_mask_img,"layers":[],"composite":auto_mask_img}
    return new_editor_dict

def undo_auto_mask_process():
    if len(last_editor) != 1:
        return last_editor.pop()
    else:
        gr.Warning("It is the init image, can't undo anymore")
        return last_editor[0]

def clear_commands_process():
    global commands
    commands.clear()
    return gr.Dropdown(choices=[])

def auto_gen_chat_data_process(pic_paths: list[str], num: float, thread_num: float, openai_key: str):
    thread_num = int(thread_num)
    num = int(num)
    err_flags = []
    gr.Info(f'Start Generate Data\nNum: {int(num)}\nThreads: {thread_num}')

    threads_list= [threading.Thread(target=auto_gen_chat_data, args=(pic_paths, int(num/thread_num)+1 if i<num%thread_num else int(num/thread_num), i, openai_key, err_flags)) for i in range(thread_num)]
    
    for each_thread in threads_list:
        each_thread.start()
    for each_thread in threads_list:
        each_thread.join()
    
    for err in err_flags:
        print(err)
        gr.Warning(str(err))
    if len(err_flags) != 0:
        return
    gr.Info(f"Successfully Gen {num} chat data")

def auto_test_llm_process(pic_paths: list[str], num: float, thread_num: float, model_name: str):
    thread_num = int(thread_num)
    num = int(num)
    valid_nums = [0 for i in range(thread_num)]
    print('---------------Test LLM----------------')
    print(f'Start Test LLM\nNum: {int(num)}\nThreads: {thread_num}\nModel: {model_name}')
    gr.Info(f'Start Test LLM\nNum: {int(num)}\nThreads: {thread_num}\nModel: {model_name}')

    threads_list= [threading.Thread(target=auto_test_llm, args=(pic_paths, int(num/thread_num)+1 if i<num%thread_num else int(num/thread_num), i, model_name, valid_nums)) for i in range(thread_num)]

    for each_thread in threads_list:
        each_thread.start()
    for each_thread in threads_list:
        each_thread.join()
    
    result = f'Finish Test LLM\n'+f'Total: {num}        Valid: {sum(valid_nums)}\n'+f'Model: {model_name}     Score: {sum(valid_nums)/num * 100}%'
    print(result)
    print('---------------------------------------')
    gr.Info(result)
    

    


