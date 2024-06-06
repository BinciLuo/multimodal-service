import random
import gradio as gr
from PIL import Image
from datetime import datetime
from tqdm import tqdm

from modules.utils.instruction_processing import extract_instructions, extract_jarray
from modules.api.pics_api import post_hgface_img_segment
from modules.utils.image_io import trans_image_to_str
from modules.api.chat_api import post_chat
from const import *

from openai import OpenAI


def auto_gen_chat_data(pic_paths: list[str], num, thread_id, openai_key: str, err_flags: list):
    client = OpenAI(api_key= openai_key)
    def gen_one(err_flags: list):
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
            
            try:
                data_json["instruction"] = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "我更改了图片，新的图片有哪些部分？"},
                        {"role": "assistant", "content": msg},
                        {"role": "user", "content": "根据分割到的信息，生成一个修改图片的方案，请注意，我只要关于方案的句子，请不要回答其他信息，回答如：将背景更换为阳光下的沙滩，将上衣更换为红色的裙子，美颜并让笑容更灿烂"}
                    ]
                    ).choices[0].message.content
            except Exception as E:
                if thread_id == 0:
                    err_flags.append(E)
                return
            
            if data_json["instruction"] == None:
                return
            
            data_json["input"] = ""
            data_json["output"] = post_chat(model_name='gpt3dot5turbo', query=data_json["instruction"], sever_url=SERVER_URL, history=history)
            data_json["history"] = history

            with open(f"{EXTRACTED_HISTORY_SAVE_PATH}/THREAD{str(thread_id)}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json", 'w', encoding='utf-8') as json_file:
                json.dump(data_json, json_file, ensure_ascii=False, indent=4)
                json_file.close()
    

    if thread_id == 0:
        for i in tqdm(range(num)):
            if len(err_flags) == 0:
                gen_one(err_flags)
    else:
        for i in range(num):
            if len(err_flags) == 0:
                gen_one(err_flags)

def auto_test_llm(pic_paths: list[str], num: int, thread_id: int, model_name: str, valid_nums: list):
    with open(chat_config['paths']['dataset'], 'r') as json_file:
        dataset:dict = json.load(json_file)
    instructions = [data['instruction'] for data in dataset]
    def gen_one():
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
            
            data_json["instruction"] = random.choice(instructions)
            
            if data_json["instruction"] == None:
                return
            
            data_json["input"] = ""
            data_json["output"] = post_chat(model_name=model_name, query=data_json["instruction"], sever_url=SERVER_URL, history=history)
            data_json["history"] = history
            uncheck_commands = [cmd for jarrays in extract_jarray(data_json['output'][0]) for cmd in jarrays ]
            checked_commands = extract_instructions("config/cmd_pattern.json", data_json['output'][0])
            if len(uncheck_commands) == 0 or len(uncheck_commands) != len(checked_commands):
                print(uncheck_commands,"\n",checked_commands,"\n\n\n")
                return 0
            return 1

    valid_num = 0
    if thread_id == 0:
        for i in tqdm(range(num)):
            valid_num += gen_one()
    else:
        for i in range(num):
            valid_num += gen_one()
    
    valid_nums[thread_id] = valid_num