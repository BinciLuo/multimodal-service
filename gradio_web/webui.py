import base64
import io
import os
import sys
import gradio as gr
import json
import mdtex2html
from PIL import Image
from io import BytesIO

from modules.api.chat_api import chat
from modules.instruction_processing import extract_instructions
from modules.api.pics_api import post_txt2img,get_loras,post_img2img

from controllers.chat_controllers import chat_process,extract_chat_process,reset_state,commands
from controllers.pics_controller import change_pic_process,generate_pic_process
from controllers.utils_controller import check_status_process

from const import *
loras,err = get_loras()
if err != None:
    print("[WARNING] Init loras failed. Check if the SD server is running")


# GRADIO
"""

"""
def postprocess(self, y):
    return y

gr.Chatbot.postprocess = postprocess

def reset_user_input():
    return gr.update(value='')



with gr.Blocks() as demo:
    
    gr.HTML("""<h1 align="center">Test</h1>""")
    with gr.Row():
        with gr.Column(scale=10):
            chatbot = gr.Chatbot(height = 320)
            user_input = gr.Textbox(show_label=False, placeholder="输入命令", lines=4,container=False,show_copy_button=True)
            with gr.Row():
                model_select_box = gr.Dropdown(choices=chat_config["models"].keys(), type='value', label="model", value="gpt3dot5turbo")
                instruction_template_dropdown = gr.Dropdown(choices=[info["description"] for info in INSTRUCTION_PROMPT_FILES_INFO], type='index', label="prompt",value=0)
            with gr.Row():
                submitBtn = gr.Button("Submit", variant="primary")
                emptyBtn = gr.Button("Clear History",variant="stop")
                
        with gr.Column(scale=6):
            checkBtn = gr.Button("Check server status", variant="primary")
            image_show = gr.Image(type='pil',interactive=True)
            widthSlider = gr.Slider(0, 1920, value=512, step=1)
            heightSlider = gr.Slider(0, 1080, value=512, step=1)
            lora_dropdown = gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True)
            img_gen_template_dropdown = gr.Dropdown(choices=img_gen_template_dict.keys(), type='value', label="img template", value="default")
            img_input = gr.Textbox(show_label=False, placeholder="输入生成图像指令", lines=1,container=False,show_copy_button=True)
            with gr.Row():
                picGenBtn = gr.Button("Generate a Picture",variant="primary")
                picChangeBtn = gr.Button("Change Picture",variant="primary")
            extractBtn = gr.Button("Extract Instruction")
            command_dropdown = gr.Dropdown(choices=commands, type='index', label="command", multiselect=True)
            

    history = gr.State([])

    submitBtn.click(chat_process, [user_input, model_select_box, instruction_template_dropdown, chatbot], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history, command_dropdown, image_show], show_progress=True)

    extractBtn.click(extract_chat_process, [chatbot,command_dropdown], [chatbot,command_dropdown], show_progress=True)

    picGenBtn.click(generate_pic_process,[img_input, lora_dropdown, widthSlider, heightSlider],[image_show],show_progress=True)
    
    picChangeBtn.click(change_pic_process,[image_show, img_input, lora_dropdown, img_gen_template_dropdown], [image_show], show_progress=True)
    
    checkBtn.click(check_status_process,[],[])

demo.queue().launch(share=False, inbrowser=True, server_name='0.0.0.0',server_port=GRADIO_PORT,debug=True)