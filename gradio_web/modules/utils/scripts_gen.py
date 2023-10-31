import json


with open("config/sd_templates.json", 'r') as json_file:
    templates_dict:dict = json.load(json_file)


def form_alwayson_scripts_from_templates(**kwargv):
    template_name = kwargv.get("template",None)
    alwayson_scripts = templates_dict.get(template_name, {})

    # some processing for control net
    control_net_dict = alwayson_scripts.get("controlnet",None)
    if control_net_dict != None:
        init_img_str = kwargv.get("init_img_str",None)
        if init_img_str == None:
            return None, "You need init_img_str when using controlnet"
        control_net_dict["args"][0]["input_image"] = init_img_str
        alwayson_scripts["controlnet"] = control_net_dict

    return alwayson_scripts, None

def form_alwayson_scripts_from_kwargv(**kwargv):
    """
    Argv:
        alwayson_scripts(dict|None)
        template(str|None)
        init_img_str(str|None)
    """
    err_string = None
    # Begin load always on scripts
    ## if key "alwayson_scripts" in kwargv, use it.
    alwayson_scripts = kwargv.get("alwayson_scripts", None)
    ## if alwayson_scripts not in kwargv and key "templates" in kwargv, use template
    template = kwargv.get("template", None)
    if template != None and alwayson_scripts == None :    
        alwayson_scripts,err_string = form_alwayson_scripts_from_templates(**kwargv)
    ## if "alwayson_scripts" and "templates" not in kwargv use default {}
    if alwayson_scripts == None:
        alwayson_scripts= {}
    
    return alwayson_scripts, err_string