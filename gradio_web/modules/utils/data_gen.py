import random
import gradio as gr
from PIL import Image
from datetime import datetime

from modules.api.pics_api import post_hgface_img_segment
from modules.utils.image_io import trans_image_to_str
from modules.api.chat_api import post_chat
from const import *

from openai import OpenAI
client = OpenAI(api_key=f"{'sk-40wYp3aigP'}{'I6xM35w5lOT3BlbkFJ'}{'pNPOv3fzo5lBtjbr384a'}")

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
            history.append(["我更改了图片，新的图片有哪些部分？", msg])
            data_json = {}
            
            
            data_json["instruction"] = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "我更改了图片，新的图片有哪些部分？"},
                    {"role": "assistant", "content": msg},
                    {"role": "user", "content": "根据分割到的信息，生成一个修改图片的方案，下面有三个例子： 1.仅保留面部和头发，将背景更换为蓝天白云，将衣服更改为白色的T-shirt 2.将背景更换为阳光下的沙滩，将上衣更换为红色的裙子，美颜并让笑容更灿烂 3.将背景更换为城市街道，将衣服更换为运动装，并让表情严肃一点"}
                ]
                ).choices[0].message.content
            
            if data_json["instruction"] == None:
                continue
            
            data_json["input"] = ""
            data_json["output"] = post_chat(model_name='gpt3dot5turbo', query=data_json["instruction"], sever_url=SERVER_URL, history=history)
            data_json["history"] = history
            print(data_json)
            with open(f"{EXTRACTED_HISTORY_SAVE_PATH}/THREAD{str(thread_id)}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json", 'w', encoding='utf-8') as json_file:
                json.dump(data_json, json_file, ensure_ascii=False, indent=4)
                json_file.close()
            

