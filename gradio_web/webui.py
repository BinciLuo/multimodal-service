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
from controllers.pics_controller import change_pic_process,generate_pic_process, set_base_image
from controllers.utils_controller import auto_mask_process, check_status_process,submit_mask_process,send_to_editor_process,undo_auto_mask_process

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

def refresh_loras():
    global loras
    loras,err = get_loras()
    if err != None:
        gr.Warning(f"Refresh loras failed: {err}")
    return gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True,scale=2)



with gr.Blocks() as demo:
    
    gr.HTML("""<h1 align="center">Test</h1>""")
    with gr.Row():
        with gr.Tab("Chat"):
            checkBtn = gr.Button("Check server status", variant="primary")
            chatbot = gr.Chatbot(height = 320)
            user_input = gr.Textbox(show_label=False, placeholder="输入命令", lines=4,container=False,show_copy_button=True)
            with gr.Row():
                model_select_box = gr.Dropdown(choices=chat_config["models"].keys(), type='value', label="model", value="gpt3dot5turbo")
                instruction_template_dropdown = gr.Dropdown(choices=[info["description"] for info in INSTRUCTION_PROMPT_FILES_INFO], type='index', label="prompt",value=0)
            with gr.Row():
                submitBtn = gr.Button("Submit", variant="primary")
                emptyBtn = gr.Button("Clear History",variant="stop")
            command_dropdown = gr.Dropdown(choices=commands, type='index', label="command", multiselect=True)
            extractBtn = gr.Button("Extract Instruction")

        with gr.Tab("Draw"):
            with gr.Row():
                with gr.Column(scale=1):
                    base_image = gr.Image(label='Origin Image', type='pil', interactive=True)
                    #sendToEditorBtn = gr.Button("Send to Editor",variant='primary')
                    with gr.Row():
                        image_editor = gr.ImageMask(label='Edit', type='pil', interactive=True, show_download_button= True)
                        mask_image = gr.Image(label='Mask Image', type='pil',interactive=False,image_mode='RGBA')
                    with gr.Row():
                        with gr.Column():
                            autoMaskBtn = gr.Button("Auto Mask", variant='primary', size='sm')
                            undoAutoMaskBtn = gr.Button("Undo Auto Mask", variant='primary', size='sm')
                        submitMaskBtn = gr.Button("Get Mask", variant='primary')
                    with gr.Tab("Operations"):
                        img_gen_template_dropdown = gr.Dropdown(choices=img_gen_template_dict.keys(), type='value', label="img template", value="default")
                        img_input = gr.Textbox(show_label=False, placeholder="输入生成图像指令", lines=1,container=False,show_copy_button=True)
                        picGenBtn = gr.Button("Generate a Picture",variant="primary")
                        picChangeBtn = gr.Button("Change Picture",variant="primary")
                    with gr.Tab("Pic Settings"):
                        widthSlider = gr.Slider(0, 1920, value=512, step=1)
                        heightSlider = gr.Slider(0, 1080, value=512, step=1)
                        lora_dropdown = gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True)
                        loraRefreshBtn = gr.Button("Refresh loras",variant="primary",scale=1,size='sm')
                    
                

                with gr.Column(scale=1):
                    edited_image = gr.Image(label='Edited Image', type='pil',interactive=False)
                    setBaseImageBtn = gr.Button("Set as Origin Image", variant="primary")


    history = gr.State([])

    # Btn
    submitBtn.click(chat_process, [user_input, model_select_box, instruction_template_dropdown, chatbot], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history, command_dropdown, base_image], show_progress=True)

    extractBtn.click(extract_chat_process, [chatbot,command_dropdown], [chatbot,command_dropdown], show_progress=True)

    picGenBtn.click(generate_pic_process,[img_input, lora_dropdown, widthSlider, heightSlider],[base_image],show_progress=True)
    
    picChangeBtn.click(change_pic_process,[base_image, img_input, lora_dropdown, img_gen_template_dropdown, mask_image], [edited_image], show_progress=True)
    
    checkBtn.click(check_status_process,[],[])

    loraRefreshBtn.click(refresh_loras,[],[lora_dropdown])

    setBaseImageBtn.click(set_base_image,[edited_image],[base_image])

    submitMaskBtn.click(submit_mask_process,[image_editor],[mask_image,image_editor])

    autoMaskBtn.click(auto_mask_process,[image_editor],[image_editor])

    undoAutoMaskBtn.click(undo_auto_mask_process,[],[image_editor])
    #sendToEditorBtn.click(send_to_editor_process,[base_image],[image_editor])

    # events
    base_image.change(send_to_editor_process,[base_image],[image_editor])


demo.queue().launch(share=False, inbrowser=True, server_name='0.0.0.0',server_port=GRADIO_PORT,debug=True)