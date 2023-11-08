import json
import os


with open("config/conf.json", 'r') as json_file:
    global_variables:dict = json.load(json_file)
with open("config/chat_config.json", 'r') as json_file:
    chat_config:dict = json.load(json_file)
    model_info:dict = chat_config["models"]
with open("config/sd_templates.json", 'r') as json_file:
    img_gen_template_dict:dict = json.load(json_file)
with open("config/picture_process.json", 'r') as json_file:
    picture_process_info:dict = json.load(json_file)


MIDDLEWARE_ENV = os.environ.get("MIDDLEWARE_ENV")
if MIDDLEWARE_ENV == "docker":
    print(f"Running in docker, set server url {global_variables['server_url_docker']}")
    SERVER_URL = global_variables["server_url_docker"]
elif MIDDLEWARE_ENV == "local":
    print(f"Running in local, set server url {global_variables['server_url_local']}")
    SERVER_URL = global_variables["server_url_local"]
else:
    print(f"Middleware Running in Azure, set server url {global_variables['server_url']}")
    SERVER_URL = global_variables["server_url"]

GRADIO_ENV = os.environ.get("GRADIO_ENV")
if GRADIO_ENV == "Azure":
    GRADIO_PORT = 80
elif GRADIO_ENV == "local":
    GRADIO_PORT = 27777
else:
    GRADIO_PORT = 8080

PATTERN_FILE_PATH = global_variables["pattern_file_path"]

INSTRUCTION_PROMPT_FILES_INFO = chat_config["prompt_templates"]["instruction_gen"]