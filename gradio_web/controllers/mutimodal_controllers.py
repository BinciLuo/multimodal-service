import time
import gradio as gr
from PIL import Image
from modules.utils.img_segment import auto_black_by_keywords
from controllers.pics_controller import change_pic_process
from controllers.chat_controllers import commands
from controllers.utils_controller import submit_mask_process

def exec_command(command_package, base_image: Image.Image, image_editor: dict, mask_image: Image.Image, edited_image: Image.Image, img_input: str, lora_dropdown: list[str]):
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    if command_package['command'] == 'mask_selected':
        new_composite = auto_black_by_keywords(image_editor["background"], edited_image,command_package["paras"][0], False)
        image_editor = {"background":new_composite,"layers":[],"composite":new_composite}
        mask_image, image_editor = submit_mask_process(image_editor)
        image_editor["composite"] = image_editor["background"]
        gr.Info(f"Finish {command_package['command']}")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    elif command_package['command'] == 'mask_unselected':
        new_composite = auto_black_by_keywords(image_editor["background"], base_image,command_package["paras"][0], True)
        image_editor = {"background":new_composite,"layers":[],"composite":new_composite}
        mask_image, image_editor = submit_mask_process(image_editor)
        image_editor["composite"] = image_editor["background"]
        gr.Info(f"Finish {command_package['command']}")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    elif command_package['command'] == 'beauty':
        edited_image = change_pic_process(edited_image, "", lora_dropdown, "beauty", None, image_editor)
        gr.Info(f"Finish {command_package['command']}")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    elif command_package['command'] == 'face':
        edited_image = change_pic_process(edited_image, command_package["paras"][0] if command_package["paras"][0] != None else "", lora_dropdown, "face", None, image_editor)
        gr.Info(f"Finish {command_package['command']}")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    elif command_package['command'] == 'change_masked':
        print(image_editor)
        mask_image, image_editor = submit_mask_process(image_editor)
        edited_image = change_pic_process(edited_image, img_input if img_input is not None and img_input != "" else command_package['paras'][1], lora_dropdown, "default", mask_image, image_editor)
        image_editor["composite"] = image_editor["background"]
        gr.Info(f"Finish {command_package['command']}")
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    else:
        gr.Warning(f"exec_command failed, command_package:{command_package}")
        print(f"exec_command failed, command_package:{command_package}")
    # ---------------------------------------------------------------------------------------------------------------------------------------------

    return base_image, image_editor, mask_image, edited_image

def exec_commands_process(command_dropdown: list, base_image: Image.Image, image_editor: dict, mask_image: Image.Image, edited_image: Image.Image, img_input: str, lora_dropdown: list[str]):
    time.sleep(1)
    edited_image = base_image
    global commands
    command_packages = [commands[index] for index in command_dropdown]
    for command_package in command_packages:
        base_image, image_editor, mask_image, edited_image = exec_command(command_package,edited_image,image_editor,mask_image,edited_image,img_input,lora_dropdown)
    return {"background":image_editor["background"],"layers":[],"composite":None}, mask_image, edited_image