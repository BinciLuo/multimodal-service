import gradio as gr

from modules.api.chat_api import post_chat
from modules.utils.instruction_processing import extract_instructions

from const import *

commands = []
global history
history = []

def chat_process(inputs, model_name, prompt_index=0, chatbot=None):
    """
    submitBtn process function
    """
    global history
    prompt_file_name = INSTRUCTION_PROMPT_FILES_INFO[prompt_index]["file_path"]
    with open(prompt_file_name,'r') as f:
        infer_text = f.read()
    infer_text = infer_text.replace(INSTRUCTION_PROMPT_FILES_INFO[prompt_index]["user_input_replace"], inputs)
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

def extract_chat_process(chatbot, command_dropdown):
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
    

    return chatbot, command_dropdown

def reset_state():
    global commands
    commands = []
    return [], [], gr.Dropdown(choices=commands, type='index', label="command", multiselect=True), None