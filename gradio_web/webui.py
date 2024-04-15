import os
import gradio as gr
from PIL import Image

from modules.api.pics_api import get_loras
from controllers.chat_controllers import chat_process, advise_process ,extract_chat_process, reset_state, commands
from controllers.pics_controller import change_pic_process, generate_pic_process, set_base_image, change_face_process
from controllers.utils_controller import auto_mask_process, check_status_process, submit_mask_process, change_base_image_process, undo_auto_mask_process, clear_commands_process, auto_gen_chat_data_process, auto_test_llm_process
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
    print(loras)
    if err != None:
        gr.Warning(f"Refresh loras failed: {err}")
    try:
        loras = [ lora_package['alias'] for lora_package in loras ]
    except:
        pass
    
    return gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True, scale=2)




with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">Chat Image Editor</h1>""")

    with gr.Accordion("Operation Board"):
        with gr.Row():
            with gr.Column(scale=5):
                OperationBoard_CommandDropdown = gr.Dropdown(choices=commands, type='index', label="command", multiselect=True)
            with gr.Column(scale=1):
                OperationBoard_ExecSelectedBtn = gr.Button("Exec Selected Commands", variant="primary")
                OperationBoard_ExecAllBtn = gr.Button("Exec All Commands", variant='primary')
                OperationBoard_ClearCmdsBtn = gr.Button("Clear Commands", variant='stop')
        # TODO: not used now
        extractBtn = gr.Button("Extract Instruction", visible=False)
    with gr.Accordion("Settings", open=False):
        with gr.Tab("Pic"):
            with gr.Tab("img2img"):
                Settings_IMG2IMG_DenoisingInpaintSlider = gr.Slider(0, 1, label='img2img_denoising_strength', value=0.6, step=0.05)
                Settings_IMG2IMG_LoRaDropdown = gr.Dropdown(choices=loras, type='value', label="lora", multiselect=True)
                Settings_IMG2IMG_LoRaRefreshBtn = gr.Button("Refresh loras", variant="primary", scale=1, size='sm')
        with gr.Tab("Chat"):
            Settings_Chat_ModelSelectDropdown = gr.Dropdown(choices=chat_config["models"].keys(), type='value', label="model", value="gpt3dot5turbo")
            Settings_Chat_InstructionTemplateDropdown = gr.Dropdown(choices=[info["description"] for info in INSTRUCTION_PROMPT_FILES_INFO], type='value', label="chat prompt", value='Default')
            Settings_Chat_AdviseTemplateDropdown = gr.Dropdown(choices=[info["description"] for info in INSTRUCTION_PROMPT_FILES_INFO], type='value', label="gpt4v prompt", value='GPT4V Legality Statement')
        with gr.Tab("Size"):
            # TODO: not used now
            Settings_Size_WidthSlider = gr.Slider(0, 1920, label='width', value=512, step=1)
            Settings_Size_HeightSlider = gr.Slider(0, 1080, label='height', value=512, step=1)
        with gr.Tab("Data"):
            Settings_Data_SaveExtractedChatCheckbox = gr.Checkbox(value= True, label="Save Extracted Chat")
            
            
    


    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tab("Base Image"):
                BaseIMG_BaseIMGViewer = gr.Image(label='Base Image', type='pil', interactive=True)
                with gr.Accordion("Examples", open=False): 
                    gr.Examples(["example/"+filename for filename in os.listdir("./example") if filename.split('.')[-1].lower() in ["jpeg","jpg","png"]], BaseIMG_BaseIMGViewer)

            with gr.Tab("Edited Image"):
                EditedIMG_EditedIMGViewer = gr.Image(label='Edited Image', type='pil', interactive=False)
                EditedIMG_SetBaseImageBtn = gr.Button("Set as Base Image", variant="primary")
            CheckBtn = gr.Button("Check Server Status", variant="primary")
            #sendToEditorBtn = gr.Button("Send to Editor", variant='primary')


        with gr.Column(scale=1):
            with gr.Tab("Chat"):
                with gr.Accordion("Chat"):
                    with gr.Column():
                        Chat_Chatbot = gr.Chatbot(height= 300)
                        Chat_UserInput = gr.Textbox(show_label=False, placeholder="输入命令", container=False, show_copy_button=True, lines=3)
                        with gr.Accordion("Examples", open=False):
                            gr.Examples(examples_jmap["query"], Chat_UserInput)
                    with gr.Row():
                        Chat_SubmitBtn = gr.Button("Submit", variant="primary")
                        Chat_AdviseBtn = gr.Button("Advise", variant="primary")
                        Chat_EmptyBtn = gr.Button("Clear History", variant="stop", visible=False)

            with gr.Tab("Edit Image"):
                with gr.Accordion("Editor"):
                    with gr.Row():
                        EditIMG_Editor_ImageEditor = gr.ImageMask(label='Edit', type='pil', interactive=True, show_download_button= True)
                        EditIMG_MaskViewer = gr.Image(label='Mask Image', type='pil', interactive=False, image_mode='RGBA')
                    with gr.Row():
                        with gr.Column():
                            EditIMG_Editor_AutoFillBtn = gr.Button("Auto Fill", variant='primary', size='sm')
                            EditIMG_Editor_UndoAutoFillBtn = gr.Button("Undo Auto Fill", variant='primary', size='sm')
                        EditIMG_SubmitMaskBtn = gr.Button("Get Mask", variant='primary')
                with gr.Accordion("Change Face"):
                    EditIMG_ChangeFace_FaceTargetViewer = gr.Image(label='Target', type='pil', interactive=True)
                    EditIMG_ChangeFace_ChangeFaceBtn = gr.Button("Change Face", variant='primary')
                    with gr.Accordion("Examples", open=False):
                        gr.Examples(["example/"+filename for filename in os.listdir("./example") if filename.split('.')[-1].lower() in ["jpeg","jpg","png"]], EditIMG_ChangeFace_FaceTargetViewer)
                # TODO: not used now
                img_gen_template_dropdown = gr.Dropdown(choices=img_gen_template_dict.keys(), type='value', label="img template", value="default", visible=False)
                img_input = gr.Textbox(show_label=False, placeholder="输入生成图像指令", lines=1, container=False, show_copy_button=True, visible=False)
                picGenBtn = gr.Button("Generate a Picture", variant="primary", visible=False)
                picChangeBtn = gr.Button("Change Picture", variant="primary", visible=False)

    with gr.Accordion("Auto", open=False):
        with gr.Tab("Gen Data"):
            Auto_GenChat_FileExplorer = gr.FileExplorer("*.jp*g", label="Choose Files")
            Auto_GenChat_CoreSlider = gr.Slider(1, 8, label='thread', value=4, step=1)
            Auto_GenChat_NumSlider = gr.Slider(10, 1000, label='num', value=10, step=10)
            Auto_GenChat_StartBtn = gr.Button("Start", variant="primary")
        with gr.Tab("Test LLM"):
            Auto_TestLLM_FileExplorer = gr.FileExplorer("*.jp*g", label="Choose Files")
            Auto_TestLLM_CoreSlider = gr.Slider(1, 8, label='thread', value=4, step=1)
            Auto_TestLLM_NumSlider = gr.Slider(10, 1000, label='num', value=10, step=10)
            Auto_TestLLM_ModelDropdown = gr.Dropdown(choices=chat_config["models"].keys(), type='value', label="model", value="chatglm2_6b")
            Auto_TestLLM_StartBtn = gr.Button("Start", variant="primary")


    with gr.Accordion("Manual", open=False):
        gr.Markdown(open('man.md', 'r').read())
    
    history = gr.State([])

    # Btn
    Chat_SubmitBtn.click(chat_process, [Chat_UserInput, Settings_Chat_ModelSelectDropdown, Settings_Chat_InstructionTemplateDropdown, Chat_Chatbot], [Chat_Chatbot, history],show_progress=True)

    Chat_AdviseBtn.click(advise_process, [Chat_UserInput, Settings_Chat_AdviseTemplateDropdown, Chat_Chatbot, BaseIMG_BaseIMGViewer], [Chat_Chatbot, history],show_progress=True)

    Chat_SubmitBtn.click(reset_user_input, [], [Chat_UserInput])

    Chat_EmptyBtn.click(reset_state, outputs=[Chat_Chatbot, history, OperationBoard_CommandDropdown, BaseIMG_BaseIMGViewer], show_progress=True)

    extractBtn.click(extract_chat_process, [Chat_Chatbot, OperationBoard_CommandDropdown, Settings_Data_SaveExtractedChatCheckbox], [Chat_Chatbot, OperationBoard_CommandDropdown], show_progress=True)

    picGenBtn.click(generate_pic_process,[img_input, Settings_IMG2IMG_LoRaDropdown, Settings_Size_WidthSlider, Settings_Size_HeightSlider],[BaseIMG_BaseIMGViewer], show_progress=True)
    
    picChangeBtn.click(change_pic_process,[BaseIMG_BaseIMGViewer, img_input, Settings_IMG2IMG_LoRaDropdown, img_gen_template_dropdown, EditIMG_MaskViewer, EditIMG_Editor_ImageEditor], [EditedIMG_EditedIMGViewer], show_progress=True)
    
    CheckBtn.click(check_status_process,[],[])

    Settings_IMG2IMG_LoRaRefreshBtn.click(refresh_loras,[],[Settings_IMG2IMG_LoRaDropdown])

    EditedIMG_SetBaseImageBtn.click(set_base_image,[EditedIMG_EditedIMGViewer],[BaseIMG_BaseIMGViewer])

    EditIMG_SubmitMaskBtn.click(submit_mask_process,[EditIMG_Editor_ImageEditor],[EditIMG_MaskViewer, EditIMG_Editor_ImageEditor])

    EditIMG_Editor_AutoFillBtn.click(auto_mask_process,[EditIMG_Editor_ImageEditor, BaseIMG_BaseIMGViewer],[EditIMG_Editor_ImageEditor])

    EditIMG_Editor_UndoAutoFillBtn.click(undo_auto_mask_process,[],[EditIMG_Editor_ImageEditor])

    EditIMG_ChangeFace_ChangeFaceBtn.click(change_face_process, [BaseIMG_BaseIMGViewer, EditIMG_ChangeFace_FaceTargetViewer], [EditedIMG_EditedIMGViewer], show_progress=True)

    OperationBoard_ExecSelectedBtn.click(exec_commands_process,[OperationBoard_CommandDropdown, BaseIMG_BaseIMGViewer, EditIMG_Editor_ImageEditor, EditIMG_MaskViewer, EditedIMG_EditedIMGViewer, img_input, Settings_IMG2IMG_LoRaDropdown, Settings_IMG2IMG_DenoisingInpaintSlider], [EditIMG_Editor_ImageEditor, EditIMG_MaskViewer, EditedIMG_EditedIMGViewer])
    OperationBoard_ExecAllBtn.click(exec_all_commands_process,[BaseIMG_BaseIMGViewer, EditIMG_Editor_ImageEditor, EditIMG_MaskViewer, EditedIMG_EditedIMGViewer, img_input, Settings_IMG2IMG_LoRaDropdown, Settings_IMG2IMG_DenoisingInpaintSlider], [EditIMG_Editor_ImageEditor, EditIMG_MaskViewer, EditedIMG_EditedIMGViewer])
    OperationBoard_ClearCmdsBtn.click(clear_commands_process,[],[OperationBoard_CommandDropdown])

    Auto_GenChat_StartBtn.click(auto_gen_chat_data_process,[Auto_GenChat_FileExplorer, Auto_GenChat_NumSlider, Auto_GenChat_CoreSlider],[])
    Auto_TestLLM_StartBtn.click(auto_test_llm_process,[Auto_TestLLM_FileExplorer, Auto_TestLLM_NumSlider, Auto_TestLLM_CoreSlider, Auto_TestLLM_ModelDropdown])

    #sendToEditorBtn.click(send_to_editor_process,[base_image],[image_editor])

    # events
    BaseIMG_BaseIMGViewer.change(change_base_image_process,[BaseIMG_BaseIMGViewer, Chat_Chatbot],[EditIMG_Editor_ImageEditor, Chat_Chatbot, OperationBoard_CommandDropdown])
    Chat_Chatbot.change(extract_chat_process,[Chat_Chatbot, OperationBoard_CommandDropdown, Settings_Data_SaveExtractedChatCheckbox],[Chat_Chatbot, OperationBoard_CommandDropdown])



demo.queue().launch(share=False, inbrowser=True, server_name='0.0.0.0', server_port=GR_PORT, debug=True)