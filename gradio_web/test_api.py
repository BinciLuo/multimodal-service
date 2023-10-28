# import modules.api.chat_api as api
# import json


# with open("config/chat_models.json", 'r') as json_file:
#         model_info:dict = json.load(json_file)

# print(api.chat("gpt3dot5turbo","python如何引用同级文件？比如说modules和tests这两个文件夹在一个文件夹中，如何让tests/test_api.py能够调用modules/api.py中的函数？",model_info,"http://0.0.0.0:8080"))

import tests.test_api as test_package

test_package.test_chat()
test_package.test_txt2img()
test_package.test_loras()
test_package.test_img2img()