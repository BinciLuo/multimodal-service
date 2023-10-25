import gradio as gr
import json
import mdtex2html
from modules.api.chat_api import chat
# 加载全局变量
"""

"""
with open("config/conf.json", 'r') as json_file:
    global_variables:dict = json.load(json_file)
with open("config/chat_models.json", 'r') as json_file:
    chat_models:dict = json.load(json_file)
SERVER_URL = global_variables["server_url"]


# GRADIO
"""

"""

def chat_process(inputs, model_name, chatbot):
    infer_text = inputs
    chatbot.append((input,""))
    answer, e = chat(model_name, infer_text, SERVER_URL)
    chatbot[-1] = (infer_text, answer) if e==None else (infer_text, e)

    yield chatbot, None

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

    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="输入命令", lines=10,container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=2):
            emptyBtn = gr.Button("Clear History")
            model_select_box = gr.Dropdown(choices=chat_models.keys(), type='value', label="model")

    history = gr.State([])

    submitBtn.click(chat_process, [user_input, model_select_box,chatbot], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)

demo.queue().launch(share=False, inbrowser=True, server_name='0.0.0.0',server_port=27777,debug=True)