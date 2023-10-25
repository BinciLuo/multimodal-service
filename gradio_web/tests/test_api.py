#import modules.api.chat_api as api
from modules.api.chat_api import chat
import json



def test():
        # TODO : Solve relative path when reading file
        # with open("../config/chat_models.json", 'r') as json_file:
        #         model_info:dict = json.load(json_file)
        print(chat("gpt3dot5turbo","python如何引用同级文件？比如说modules和tests这两个文件夹在一个文件夹中，如何让tests/test_api.py能够调用modules/api.py中的函数？","http://0.0.0.0:8080"))