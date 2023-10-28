import json
import gradio as gr

from modules.api.chat_api import chat
from modules.instruction_processing import extract_instructions


with open("config/conf.json", 'r') as json_file:
    global_variables:dict = json.load(json_file)
with open("config/chat_models.json", 'r') as json_file:
    chat_models:dict = json.load(json_file)
with open("config/sd_templates.json", 'r') as json_file:
    img_gen_template_dict:dict = json.load(json_file)


SERVER_URL = global_variables["server_url"]
PATTERN_FILE_PATH = global_variables["pattern_file_path"]
instruction_prompt_files_info = chat_models["prompt_templates"]["instruction_gen"]

commands = []

def chat_process(inputs, model_name, prompt_index=0, chatbot=None):
    """
    submitBtn process function
    """
    prompt_file_name = instruction_prompt_files_info[prompt_index]["file_path"]
    with open(prompt_file_name,'r') as f:
        infer_text = f.read()
    infer_text = infer_text.replace(instruction_prompt_files_info[prompt_index]["user_input_replace"],inputs)
    chatbot.append((input,""))
    answer, e = chat(model_name, infer_text, SERVER_URL)
    chatbot[-1] = (inputs, answer) if e==None else (inputs, e)

    yield chatbot, None

def extract_chat_process(chatbot,command_dropdown):
    """
    extractBtn process function
    """
    extracted_commands = extract_instructions(PATTERN_FILE_PATH,chatbot[-1][-1])
    commands.extend([json.dumps(cmd) for cmd in extracted_commands])
    extracted_commands_string = ""
    for cmd in extracted_commands:
        extracted_commands_string += f'操作为: {cmd["command"]} 参数为: {cmd["paras"]}\n'
    #extracted_commands_string = json.dumps(extracted_commands,ensure_ascii=False)

    
    chatbot[-1][-1] = extracted_commands_string if extracted_commands_string != "" else chatbot[-1][-1]
    print(commands)
    command_dropdown = gr.Dropdown(choices=[f'操作为: {json.loads(cmd)["command"]} 参数为: {json.loads(cmd)["paras"]}' for cmd in commands], type='index', label="command", multiselect=True)
    

    yield chatbot, command_dropdown
