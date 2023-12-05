import json
import os

# Read config files
with open("config/conf.json", 'r') as json_file:
    global_variables:dict = json.load(json_file)
with open("config/chat_config.json", 'r') as json_file:
    chat_config:dict = json.load(json_file)
    model_info:dict = chat_config["models"]
with open("config/sd_templates.json", 'r') as json_file:
    img_gen_template_dict:dict = json.load(json_file)
with open("config/picture_process.json", 'r') as json_file:
    picture_process_info:dict = json.load(json_file)
with open("config/img2img_default_paras.json", 'r') as json_file:
    IMG2IMG_DEFAULT_PARAS:dict = json.load(json_file)
with open("example/examples.json", 'r') as json_file:
    examples_jmap:dict = json.load(json_file)

# Read MIDDLEWARE_ENV from $MIDDLEWARE_ENV
# Default Azure, you can choose 'docker'(http://middleware:8080) or 'local'(http://localhost:52780) instead.
MIDDLEWARE_ENV = os.environ.get("MIDDLEWARE_ENV")
if MIDDLEWARE_ENV == "docker":
    print(f"Running in docker, set server url {global_variables['server_url_docker']}")
    SERVER_URL = global_variables["server_url_docker"]
elif MIDDLEWARE_ENV == "k8s":
    print(f"Running in k8s, set server url {global_variables['server_url_k8s']}")
    SERVER_URL = global_variables["server_url_k8s"]
elif MIDDLEWARE_ENV == "local":
    print(f"Running in local, set server url {global_variables['server_url_local']}")
    SERVER_URL = global_variables["server_url_local"]
else:
    print(f"Middleware Running in Azure, set server url {global_variables['server_url']}")
    SERVER_URL = global_variables["server_url"]

# Read GRADIO_ENV from $GRADIO_ENV
# Default '':8080, you can choose 'Azure':80 or 'local':27777 instead.
GRADIO_ENV = os.environ.get("GRADIO_ENV")
if GRADIO_ENV == "Azure":
    GRADIO_PORT = 80
elif GRADIO_ENV == "local" or "k8s":
    GRADIO_PORT = 27777
else:
    GRADIO_PORT = 8080

PATTERN_FILE_PATH = global_variables["pattern_file_path"]

INSTRUCTION_PROMPT_FILES_INFO = chat_config["prompt_templates"]["instruction_gen"]