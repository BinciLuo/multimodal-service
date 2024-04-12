import gradio as gr
import json
from datetime import datetime

from modules.api.chat_api import post_chat, post_gpt4v
from modules.utils.instruction_processing import extract_instructions
from modules.utils.image_io import trans_image_to_str

from const import *

commands = []
global history
history = []

def chat_process(inputs, model_name, prompt_description, chatbot=None):
    """
    submitBtn process function
    """
    global history
    prompt_file_info = None
    for file_info in INSTRUCTION_PROMPT_FILES_INFO:
        if file_info['description'] == prompt_description:
            prompt_file_info = file_info
            break

    with open(prompt_file_info['file_path'],'r') as f:
        infer_text = f.read()
    infer_text = infer_text.replace(prompt_file_info["user_input_replace"], inputs)
    answer, e = post_chat(model_name, infer_text, SERVER_URL, history)
    print(answer)
    if e != None:
        gr.Warning(e)
        return chatbot, None
    chatbot.append((inputs,""))
    history.append((inputs, answer))
    history = history[-10:] if len(history) > 10 else history
    chatbot[-1] = (inputs, answer)

    return chatbot, None

def advise_process(inputs, prompt_description, chatbot=None, base_image=None):
    """
    adviseBtn process function
    """
    global history
    prompt_file_info = None
    for file_info in INSTRUCTION_PROMPT_FILES_INFO:
        if file_info['description'] == prompt_description:
            prompt_file_info = file_info
            break
    with open(prompt_file_info['file_path'],'r') as f:
        infer_text = f.read()
    infer_text = infer_text.replace(prompt_file_info["user_input_replace"], inputs)
    answer, e = post_gpt4v(infer_text, SERVER_URL, trans_image_to_str(base_image),history)
    print(answer)
    if e != None:
        gr.Warning(e)
        return chatbot, None
    chatbot.append(("根据我提供的图片提供修改的建议。"+inputs, ""))
    history.append(("根据我提供的图片提供修改的建议。"+inputs, answer))
    history = history[-10:] if len(history) > 10 else history
    chatbot[-1] = ("根据我提供的图片提供修改的建议。"+inputs, answer)

    return chatbot, None

def extract_chat_process(chatbot, command_dropdown, save_extracted_chat):
    """
    extractBtn process function
    """
    if len(chatbot) == 0:
        gr.Warning("No conversation to extract.")
        return chatbot, command_dropdown
    global commands
    extracted_commands = extract_instructions(PATTERN_FILE_PATH, chatbot[-1][-1])
    commands.extend([cmd for cmd in extracted_commands])
    extracted_commands_string = ""
    advice = ""
    for cmd in extracted_commands:
        if cmd["command"] == 'advice':
            advice = f'给出的建议是:\n  {cmd["paras"][0]}'
        else:
            extracted_commands_string += f'操作为: {cmd["command"]} 参数为: {cmd["paras"]}\n'
    extracted_commands_string += advice
    
    chatbot[-1][-1] = extracted_commands_string if extracted_commands_string != "" else chatbot[-1][-1]
    print(commands)
    command_dropdown = gr.Dropdown(choices=[f'操作为: {cmd["command"]} 参数为: {cmd["paras"]}' for cmd in commands], type='index', label="command", multiselect=True)
    
    if save_extracted_chat and len(chatbot) > 1:
        history = []
        for i in range(len(chatbot)-1):
            history.append([chatbot[i][0], chatbot[i][1]])
        data_json = {}
        data_json["instruction"] = chatbot[-1][0]
        data_json["input"] = ""
        data_json["output"] = chatbot[-1][-1]
        data_json["history"] = history
        with open(f"{EXTRACTED_HISTORY_SAVE_PATH}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json", 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)
    return chatbot, command_dropdown

def reset_state():
    global commands
    commands = []
    return [], [], gr.Dropdown(choices=commands, type='index', label="command", multiselect=True), None