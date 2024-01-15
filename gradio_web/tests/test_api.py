#import modules.api.chat_api as api
from modules.api.chat_api import post_chat
from modules.api.pics_api import post_txt2img, post_img2img, form_post_img2img_paras, form_post_txt2img_paras
from modules.api.pics_api import get_loras

def show_err(api_name, example, e):
        print(f"Test {api_name} failed. \n    Example: {example}\n    Error: {e}\n")

def test_chat():
        print(post_chat("gpt3dot5turbo","12345","http://0.0.0.0:8080", []))
def test_txt2img():
        paras, e = form_post_txt2img_paras("a cup of tea", loras=[], width=512, height=512)
        if e != None:
                show_err('test_txt2img','post_txt2img("a cup of tea", loras=[], width=512, height=512)', e)
        _, e = post_txt2img(paras)
        if e != None:
                show_err('test_txt2img','post_txt2img("a cup of tea", loras=[], width=512, height=512)', e)
        
        paras, e = form_post_txt2img_paras("a cup of tea", loras=[], width=512, height=512, template = "beauty")
        if e != None:
                show_err('test_txt2img','post_txt2img("a cup of tea", loras=[], width=512, height=512)', e)
        _, e = post_txt2img(paras)
        if e != "[SD] txt2img failed":
                show_err('test_txt2img','post_txt2img("a cup of tea", loras=[], width=512, height=512, template = "beauty")','e != "[SD] txt2img failed"')
                
def test_loras():
        print(get_loras())
def test_img2img():
        with open("tests/test_img.txt",'r') as f:
                init_img_str = f.read()
        paras, e = form_post_img2img_paras(init_img_str ,"change background color to white",[], template = "beauty", width = 512, height = 512)
        _, e = post_img2img(paras)
        if e != None:
                show_err('test_img2img','post_img2img("change background color to white",[], template = "beauty", init_img_str=init_img_str, width = 512, height = 512)', e)