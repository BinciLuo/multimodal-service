#import modules.api.chat_api as api
from modules.api.chat_api import chat
from modules.api.pics_api import post_txt2img,post_img2img
from modules.api.pics_api import get_loras
import json



def test_chat():
        print(chat("gpt3dot5turbo","12345","http://0.0.0.0:8080"))
def test_txt2img():
        post_txt2img("a cup of tea", loras=[], width=512, height=512)
def test_loras():
        print(get_loras())
def test_img2img():
        with open("tests/test_img.txt",'r') as f:
                post_img2img(f.read(),"change background color to white",[],512,512)