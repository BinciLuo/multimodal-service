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

    response=requests.post(sever_url+model_info[model_name]["route"], data=json.dumps(post_data))
    if response.status_code != 200:
        return "",Exception(f"server is not running, status code : {response.status_code}") 
    try:
        response_json = response.json()
        return response_json["chat"],None
    
    except Exception as e:
        print("chat error",e)
        return "", e
    
    