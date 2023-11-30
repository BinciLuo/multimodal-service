import json
import sys
import gradio as gr

from modules.api.chat_api import chat
from modules.instruction_processing import extract_instructions

from const import *

commands = []
history = []

def chat_process(inputs, model_name, prompt_index=0, chatbot=None):
    """
    submitBtn process function
    """
    prompt_file_name = INSTRUCTION_PROMPT_FILES_INFO[prompt_index]["file_path"]
    with open(prompt_file_name,'r') as f:
        infer_text = f.read()
    infer_text = infer_text.replace(INSTRUCTION_PROMPT_FILES_INFO[prompt_index]["user_input_replace"],inputs)
    answer, e = chat(model_name, infer_text, SERVER_URL)
    if e != None:
        gr.Warning(e)
        return chatbot, None
    chatbot.append((input,""))
    history.append(inputs, answer)
    chatbot[-1] = (inputs, answer)

    return chatbot, None

def extract_chat_process(chatbot,command_dropdown):
    """
    extractBtn process function
    """
    if len(chatbot) == 0:
        gr.Warning("No conversation to extract.")
        return chatbot, command_dropdown
    global commands
    extracted_commands = extract_instructions(PATTERN_FILE_PATH,chatbot[-1][-1])
    commands.extend([json.dumps(cmd) for cmd in extracted_commands])
    extracted_commands_string = ""
    for cmd in extracted_commands:
        extracted_commands_string += f'操作为: {cmd["command"]} 参数为: {cmd["paras"]}\n'
    #extracted_commands_string = json.dumps(extracted_commands,ensure_ascii=False)

    
    chatbot[-1][-1] = extracted_commands_string if extracted_commands_string != "" else chatbot[-1][-1]
    print(commands)
    command_dropdown = gr.Dropdown(choices=[f'操作为: {json.loads(cmd)["command"]} 参数为: {json.loads(cmd)["paras"]}' for cmd in commands], type='index', label="command", multiselect=True)
    

    return chatbot, command_dropdown

def reset_state():
    global commands
    commands = []
    return [], [], gr.Dropdown(choices=commands, type='index', label="command", multiselect=True),None