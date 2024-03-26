import random
import gradio as gr
from PIL import Image
from datetime import datetime

from modules.api.pics_api import post_hgface_img_segment
from modules.utils.image_io import trans_image_to_str
from modules.api.chat_api import post_chat
from const import *

def auto_gen_chat_data(pic_paths: list[str], num, thread_id):
    for i in range(num):
        image_idx = random.randint(0, len(pic_paths)-1)
        image_path = pic_paths[image_idx]
        image = Image.open(image_path)
        response_json,err = post_hgface_img_segment(trans_image_to_str(image))
        
        if err != None:
            gr.Warning(err)
        if err == None:
            labels = [image_package['label'] for image_package in response_json["image_packages"]]
            msg = "分割得到的标签有:"
            for i, label in enumerate(labels):
                msg += f"\n{i+1}. {label}"

            history = []
            history.append("我更改了图片，新的图片有哪些部分？", msg)
            data_json = {}

            instruction, err = post_chat(model_name='gpt3dot5turbo', query='根据我给出的信息，给我生成一个修改图片的建议', sever_url=SERVER_URL, history=history)
            if err != None:
                continue
            data_json["instruction"] = instruction
            data_json["input"] = ""
            data_json["output"] = post_chat(model_name='gpt3dot5turbo', query=instruction, sever_url=SERVER_URL, history=history)
            data_json["history"] = history
            with open(f"{EXTRACTED_HISTORY_SAVE_PATH}/THREAD{str(thread_id)}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json", 'w', encoding='utf-8') as json_file:
                json.dump(data_json, json_file, ensure_ascii=False, indent=4)
                json_file.close()
            

