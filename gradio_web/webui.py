import gradio as gr
import json
import mdtex2html
from modules.api.chat_api import chat
from modules.instruction_processing import extract_instructions
# 加载全局变量
"""

"""
with open("config/conf.json", 'r') as json_file:
    global_variables:dict = json.load(json_file)
with open("config/chat_models.json", 'r') as json_file:
    chat_models:dict = json.load(json_file)

SERVER_URL = global_variables["server_url"]
PATTERN_FILE_PATH = global_variables["pattern_file_path"]
commands = []


# Functions
"""

"""

def chat_process(inputs, model_name, chatbot):
    infer_text = inputs
    chatbot.append((input,""))
    answer, e = chat(model_name, infer_text, SERVER_URL)
    chatbot[-1] = (infer_text, answer) if e==None else (infer_text, e)

    yield chatbot, None

def extract_chat(chatbot,command_dropdown):
    ori_last_chat = chatbot[-1]
    extracted_commands = extract_instructions(PATTERN_FILE_PATH,ori_last_chat[1])
    commands.extend([json.dumps(cmd) for cmd in extracted_commands])
    chatbot.append(("",""))
    extracted_commands_string = json.dumps(extracted_commands,ensure_ascii=False)
    chatbot[-1] = ("抽取的指令如下",extracted_commands_string)
    print(commands)
    command_dropdown = gr.Dropdown(choices=commands, type='value', label="command", multiselect=True)
    

    yield chatbot, command_dropdown


# GRADIO
"""

"""
def postprocess(self, y):
    # if y is None:
    #     return []
    # for i, (message, response) in enumerate(y):
    #     y[i] = (
    #         None if message is None else mdtex2html.convert((message)),
    #         None if response is None else mdtex2html.convert(response),
    #     )
    return y

gr.Chatbot.postprocess = postprocess

def reset_user_input():
    return gr.update(value='')

def reset_state():
    return [], []

with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">Test</h1>""")
    with gr.Row():
        with gr.Column(scale=6):
            chatbot = gr.Chatbot()
        with gr.Column(scale=6):
            command_dropdown = gr.Dropdown(choices=commands, type='value', label="command", multiselect=True)
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="输入命令", lines=10,container=False,show_copy_button=True)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=2):
            emptyBtn = gr.Button("Clear History")
            model_select_box = gr.Dropdown(choices=chat_models.keys(), type='value', label="model")
            extractBtn = gr.Button("Extract Instruction")

    history = gr.State([])

    submitBtn.click(chat_process, [user_input, model_select_box,chatbot], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)

    extractBtn.click(extract_chat, [chatbot,command_dropdown], [chatbot,command_dropdown], show_progress=True)

    

demo.queue().launch(share=False, inbrowser=True, server_name='0.0.0.0',server_port=27777,debug=True)