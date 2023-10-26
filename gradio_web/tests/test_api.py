#import modules.api.chat_api as api
from modules.api.chat_api import chat
from modules.api.pics_api import txt2img
import json



def test_chat():
        print(chat("gpt3dot5turbo","12345","http://0.0.0.0:8080"))
def test_txt2img():
        txt2img("a cup of tea", loras=[], width=512, height=512)