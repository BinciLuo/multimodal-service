import gradio as gr
from PIL import Image
from modules.utils.img_segment import auto_black_by_keywords
from controllers.pics_controller import change_pic_process
from controllers.chat_controllers import commands
from controllers.utils_controller import submit_mask_process

def exec_command(command_package, base_image: Image, image_editor: dict, mask_image: Image, edited_image: Image, img_input: str, lora_dropdown: list[str]):
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    if command_package['command'] == 'mask_selected':
        new_composite = auto_black_by_keywords(image_editor["composite"], base_image,command_package["paras"][0])
        image_editor = {"background":new_composite,"layers":[],"composite":new_composite}
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------------    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    elif command_package['command'] == 'change_masked':
        mask_image, new_image_editor_dict = submit_mask_process(image_editor)
        edited_image = change_pic_process(base_image, img_input if img_input is not None and img_input != "" else command_package['paras'][1], lora_dropdown, "default", mask_image)
        image_editor = {"background":new_image_editor_dict["background"],"layers":[],"composite":new_image_editor_dict["background"]}
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    else:
        print(f"exec_command failed, command_package:{command_package}")
    # ---------------------------------------------------------------------------------------------------------------------------------------------

    return base_image, image_editor, mask_image, edited_image

def exec_commands_process(command_dropdown: list, base_image: Image, image_editor: dict, mask_image: Image, edited_image: Image, img_input: str, lora_dropdown: list[str]):
    global commands
    command_packages = [commands[index] for index in command_dropdown]
    for command_package in command_packages:
        base_image, image_editor, mask_image, edited_image = exec_command(command_package,base_image,image_editor,mask_image,edited_image,img_input,lora_dropdown)
    return base_image, gr.ImageEditor(value={"background":image_editor["composite"],"layers":[],"composite":None}, label='Edit', type='pil', interactive=True), mask_image, edited_image