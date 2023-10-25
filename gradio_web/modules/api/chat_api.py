import json
import requests


def chat(model_name: str, query: str, sever_url:str) -> (str, Exception):
    with open("config/chat_models.json", 'r') as json_file:
                model_info:dict = json.load(json_file)
    if model_name not in model_info.keys():
        return "",Exception("model_name not found")
    if "route" not in model_info[model_name].keys():
        return "",Exception("route of model not found")
    
    post_data = {"query": query}

    try:
        response=requests.post(sever_url+model_info[model_name]["route"], data=json.dumps(post_data))
        response_json = response.json()
        return response_json["chat"],None
    
    except Exception as e:
        print("chat error",type(e))
        return "", e
    
    