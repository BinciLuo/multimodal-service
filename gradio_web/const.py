import json
import os

# ---------------------------------------------------------------
# Read config files
with open("config/server_config.json", 'r') as json_file:
    global_variables:dict = json.load(json_file)
with open("config/chat_config.json", 'r') as json_file:
    chat_config:dict = json.load(json_file)
    model_info:dict = chat_config["models"]
with open("config/sd_templates.json", 'r') as json_file:
    img_gen_template_dict:dict = json.load(json_file)
with open("config/picture_routes.json", 'r') as json_file:
    picture_process_info:dict = json.load(json_file)
with open("config/img2img_default_paras.json", 'r') as json_file:
    IMG2IMG_DEFAULT_PARAS:dict = json.load(json_file)
with open("example/examples.json", 'r') as json_file:
    examples_jmap:dict = json.load(json_file)
with open("config/segment_config.json", 'r') as json_file:
    segment_config:dict = json.load(json_file)

# ---------------------------------------------------------------
# Read MIDDLEWARE_ENV from $MIDDLEWARE_ENV
# Default Azure, you can choose 'local'(http://localhost:52780) or 'k8s'(http://localhost:8080) instead.
MIDDLEWARE_ENV = os.environ.get("MIDDLEWARE_ENV")
if MIDDLEWARE_ENV == "k8s":
    print(f"Running in k8s, set server url {global_variables['server_url_k8s']}")
    SERVER_URL = global_variables["server_url_k8s"]
elif MIDDLEWARE_ENV == "local":
    print(f"Running in local, set server url {global_variables['server_url_local']}")
    SERVER_URL = global_variables["server_url_local"]
else:
    print(f"Middleware Running in Azure, set server url {global_variables['server_url']}")
    SERVER_URL = global_variables["server_url"]
print(f"[INIT] Set MIDDLEWARE_ENV:{MIDDLEWARE_ENV}, middleware running in port {SERVER_URL}")

# ---------------------------------------------------------------
# Read GR_PORT from $GR_PORT
# Default 8080
GR_PORT = os.environ.get("GR_PORT")
if GR_PORT is not None:
    try:
        GR_PORT = int(GR_PORT)
    except ValueError:
        print(f"GR_PORT:{GR_PORT} is not an int. Use 8080.")
        GR_PORT = 8080
else:
    GR_PORT = 8080
print(f"[INIT] Set GR_PORT:{GR_PORT}, webui running in {GR_PORT}")

# ---------------------------------------------------------------
# Read SEG_MODEL_ENV from $SEG_MODEL_ENV
# Default '':huggingface, you can choose 'local'
SEG_MODEL_ENV = os.environ.get("SEG_MODEL_ENV")
if SEG_MODEL_ENV == 'local':
    print("[INIT] Segment Model Running in Local")
else:
    print("[INIT] Use Segment Model through API")

# ---------------------------------------------------------------
PATTERN_FILE_PATH = global_variables["pattern_file_path"]
INSTRUCTION_PROMPT_FILES_INFO = chat_config["prompt_templates"]["instruction_gen"]
EXTRACTED_HISTORY_SAVE_PATH = chat_config["paths"]["extracted_history"]

# ---------------------------------------------------------------
# |<----->| pixcels / rate = half kernel size
MASK_ERODE_RATE = 60