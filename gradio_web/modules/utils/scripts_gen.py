import json


with open("config/sd_templates.json", 'r') as json_file:
    templates_dict:dict = json.load(json_file)


def form_alwayson_scripts_from_templates(template_name:str, **kargv):
    alwayson_scripts = templates_dict.get(template_name, {})

    # some processing for control net
    control_net_dict = alwayson_scripts.get("controlnet",None)
    if control_net_dict != None:
        init_img_str = kargv.get("init_img_str",None)
        if init_img_str == None:
            raise Exception("You need init_img_str when using controlnet")
        control_net_dict["args"][0]["input_image"] = init_img_str
        alwayson_scripts["controlnet"] = control_net_dict

    return alwayson_scripts
