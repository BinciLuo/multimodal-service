#import modules.api.chat_api as api
from modules.api.chat_api import chat
from modules.api.pics_api import post_txt2img,post_img2img
from modules.api.pics_api import get_loras
import json

def show_err(api_name, example, err_string):
        print(f"Test {api_name} failed. \n    Example: {example}\n    Error: {err_string}\n")

def test_chat():
        print(chat("gpt3dot5turbo","12345","http://0.0.0.0:8080"))
def test_txt2img():
        _, err_string = post_txt2img("a cup of tea", loras=[], width=512, height=512)
        if err_string != None:
                show_err('test_txt2img','post_txt2img("a cup of tea", loras=[], width=512, height=512)',err_string)
        
        _, err_string = post_txt2img("a cup of tea", loras=[], width=512, height=512, template = "beauty")
        if err_string != "post txt2img failed, You need init_img_str when using controlnet":
                show_err('test_txt2img','post_txt2img("a cup of tea", loras=[], width=512, height=512, template = "beauty")','err_string != "post txt2img failed, You need init_img_str when using controlnet"')
                
def test_loras():
        print(get_loras())
def test_img2img():
        with open("tests/test_img.txt",'r') as f:
                init_img_str = f.read()
        _, err_string = post_img2img(init_img_str ,"change background color to white",[], template = "beauty",width = 512, height = 512)
        if err_string != None:
                show_err('test_img2img','post_img2img("change background color to white",[], template = "beauty", init_img_str=init_img_str, width = 512, height = 512)',err_string)