import json
import requests

from const import *

def post_chat(model_name: str, query: str, sever_url:str, history=[]):
    """
    ### This function posts LLM
    ### Argvs
    ```
        model_name(str): name of llm, see enum in ./config/chat_config.json
        query(str): query
        server_url: server_url
        history(list[(str,str)]): history
    ```
    ### Return
    ```
        answer(str): answer
        err(str|None): error message
    ```
    """
    if model_name not in model_info.keys():
        return "", f"[Chat] model_name [{model_name}] not found"
    if "route" not in model_info[model_name].keys():
        return "", f"[Chat] route of model [{model_name}] not found"
    
    post_data = {"query": query, "history": history}

    response=requests.post(sever_url+model_info[model_name]["route"], data=json.dumps(post_data))
    if response.status_code != 200:
        return "", f"[Chat] {model_name} failed"
    try:
        response_json = response.json()
        return response_json["chat"], None
    
    except:
        return "", f"[Chat] Unpack json failed, key 'chat' not in response"
    
    