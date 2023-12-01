import unittest

from modules.utils.scripts_gen import form_alwayson_scripts_from_templates
from modules.api.pics_api import form_post_img2img_paras,form_post_txt2img_paras

class TestSD(unittest.TestCase):
    def test_form_post_img2img_paras(self):
        with open("tests/test_img.txt",'r') as f:
            init_img_str = f.read()
        _, e = form_post_img2img_paras(init_img_str,'',[])
        self.assertEqual(None, e, e)
        paras, e = form_post_img2img_paras(init_img_str,'',[],template="beauty")
        self.assertEqual(None, e, e)
        self.assertEqual(0.2, paras["denoising_strength"], f"form_post_img2img_paras failed with template: beauty")
        self.assertEqual(paras["alwayson_scripts"]["controlnet"]["args"][0]["input_image"], init_img_str, "Init_img_str not applied")
        paras, e = form_post_img2img_paras(init_img_str,'',[],template="default")
        self.assertEqual(None, e, e)
        self.assertEqual(0.3, paras["denoising_strength"], f"form_post_img2img_paras failed with template: beauty")
    
    def test_form_post_txt2img_paras(self):
        _, e = form_post_txt2img_paras('',[])
        self.assertEqual(None, e, e)
        
    def test_form_alwayson_scripts_from_templates_beauty(self):
        with open("tests/test_img.txt",'r') as f:
            init_img_str = f.read()
        alwayson_srcipts = form_alwayson_scripts_from_templates(template = "beauty",init_img_str = init_img_str)
        self.assertEqual(alwayson_srcipts[0]["controlnet"]["args"][0]["input_image"], init_img_str, "Init_img_str not applied")



unittest.main()