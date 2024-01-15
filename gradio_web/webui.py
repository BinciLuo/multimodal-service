import os
import gradio as gr
from PIL import Image

from modules.api.pics_api import get_loras
from controllers.chat_controllers import chat_process, extract_chat_process, reset_state, commands
from controllers.pics_controller import change_pic_process, generate_pic_process, set_base_image, change_face_process
from controllers.utils_controller import auto_mask_process, check_status_process, submit_mask_process, change_base_image_process, undo_auto_mask_process
from controllers.mutimodal_controllers import exec_commands_process, exec_all_commands_process

from const import *

loras, err = get_loras()
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
    loras, err = get_loras()
    if err != None:
        gr.Warning(f"Refresh loras failed: {err}")
    return gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True, scale=2)



with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">Chat Image Editor</h1>""")

    with gr.Accordion("Operation Board"):
        with gr.Row():
            with gr.Column(scale=5):
                command_dropdown = gr.Dropdown(choices=commands, type='index', label="command", multiselect=True)
            with gr.Column(scale=1):
                execSelectedBtn = gr.Button("Exec Selected commands", variant="primary")
                execAllBtn = gr.Button("Exec all commands", variant='primary')
        extractBtn = gr.Button("Extract Instruction", visible=False)
    


    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tab("Base Image"):
                base_image = gr.Image(label='Base Image', type='pil', interactive=True)
                with gr.Accordion("Examples", open=False): 
                    gr.Examples([Image.open("example/"+filename, mode='r') for filename in os.listdir("./example") if filename.split('.')[-1].lower() in ["jpeg","jpg","png"]], base_image)

            with gr.Tab("Edited Image"):
                edited_image = gr.Image(label='Edited Image', type='pil', interactive=False)
                setBaseImageBtn = gr.Button("Set as Base Image", variant="primary")
            checkBtn = gr.Button("Check server status", variant="primary")
            #sendToEditorBtn = gr.Button("Send to Editor", variant='primary')


        with gr.Column(scale=1):
            with gr.Tab("Chat"):
                with gr.Accordion("Chat"):
                    with gr.Column():
                        chatbot = gr.Chatbot(height= 300)
                        user_input = gr.Textbox(show_label=False, placeholder="输入命令", container=False, show_copy_button=True, lines=3)
                        with gr.Accordion("Examples", open=False):
                            gr.Examples(examples_jmap["query"], user_input)
                    with gr.Row():
                        model_select_box = gr.Dropdown(choices=chat_config["models"].keys(), type='value', label="model", value="gpt3dot5turbo")
                        instruction_template_dropdown = gr.Dropdown(choices=[info["description"] for info in INSTRUCTION_PROMPT_FILES_INFO], type='index', label="prompt", value=0)
                    with gr.Row():
                        submitBtn = gr.Button("Submit", variant="primary")
                        emptyBtn = gr.Button("Clear History", variant="stop")

            with gr.Tab("Edit Image"):
                with gr.Accordion("Editor"):
                    with gr.Row():
                        imageEditor = gr.ImageMask(label='Edit', type='pil', interactive=True, show_download_button= True)
                        maskImage = gr.Image(label='Mask Image', type='pil', interactive=False, image_mode='RGBA')
                    with gr.Row():
                        with gr.Column():
                            autoFillBtn = gr.Button("Auto Fill", variant='primary', size='sm')
                            undoAutoFillBtn = gr.Button("Undo Auto Fill", variant='primary', size='sm')
                        submitMaskBtn = gr.Button("Get Mask", variant='primary')
                with gr.Accordion("Change Face"):
                    faceTargetImage = gr.Image(label='Target', type='pil', interactive=True)
                    changeFaceBtn = gr.Button("Change Face", variant='primary')
                    with gr.Accordion("Examples", open=False):
                        gr.Examples(["example/"+filename for filename in os.listdir("./example") if filename.split('.')[-1].lower() in ["jpeg","jpg","png"]], faceTargetImage)
                img_gen_template_dropdown = gr.Dropdown(choices=img_gen_template_dict.keys(), type='value', label="img template", value="default")
                img_input = gr.Textbox(show_label=False, placeholder="输入生成图像指令", lines=1, container=False, show_copy_button=True)
                picGenBtn = gr.Button("Generate a Picture", variant="primary")
                picChangeBtn = gr.Button("Change Picture", variant="primary")

            with gr.Tab("Pic Settings"):
                widthSlider = gr.Slider(0, 1920, value=512, step=1)
                heightSlider = gr.Slider(0, 1080, value=512, step=1)
                lora_dropdown = gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True)
                loraRefreshBtn = gr.Button("Refresh loras", variant="primary", scale=1, size='sm')
            
            


    history = gr.State([])

    # Btn
    submitBtn.click(chat_process, [user_input, model_select_box, instruction_template_dropdown, chatbot], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history, command_dropdown, base_image], show_progress=True)

    extractBtn.click(extract_chat_process, [chatbot, command_dropdown], [chatbot, command_dropdown], show_progress=True)

    picGenBtn.click(generate_pic_process,[img_input, lora_dropdown, widthSlider, heightSlider],[base_image], show_progress=True)
    
    picChangeBtn.click(change_pic_process,[base_image, img_input, lora_dropdown, img_gen_template_dropdown, maskImage, imageEditor], [edited_image], show_progress=True)
    
    checkBtn.click(check_status_process,[],[])

    loraRefreshBtn.click(refresh_loras,[],[lora_dropdown])

    setBaseImageBtn.click(set_base_image,[edited_image],[base_image])

    submitMaskBtn.click(submit_mask_process,[imageEditor],[maskImage, imageEditor])

    autoFillBtn.click(auto_mask_process,[imageEditor, base_image],[imageEditor])

    undoAutoFillBtn.click(undo_auto_mask_process,[],[imageEditor])

    changeFaceBtn.click(change_face_process, [base_image, faceTargetImage], [edited_image], show_progress=True)

    execSelectedBtn.click(exec_commands_process,[command_dropdown, base_image, imageEditor, maskImage, edited_image, img_input, lora_dropdown], [imageEditor, maskImage, edited_image])
    execAllBtn.click(exec_all_commands_process,[base_image, imageEditor, maskImage, edited_image, img_input, lora_dropdown], [imageEditor, maskImage, edited_image])

    #sendToEditorBtn.click(send_to_editor_process,[base_image],[image_editor])

    # events
    base_image.change(change_base_image_process,[base_image, chatbot],[imageEditor, chatbot, command_dropdown])
    chatbot.change(extract_chat_process,[chatbot, command_dropdown],[chatbot, command_dropdown])



demo.queue().launch(share=False, inbrowser=True, server_name='0.0.0.0', server_port=GR_PORT, debug=True)