import json
import requests


def chat(model_name: str, query: str, model_info: dict, sever_url:str) -> (str, Exception):
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
        return "", e
    
    