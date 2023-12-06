import unittest

from modules.utils.scripts_gen import form_alwayson_scripts_from_templates
from modules.utils.imaga_paras_gen import form_post_img2img_paras, form_post_txt2img_paras

class TestSD(unittest.TestCase):
    def test_form_post_img2img_paras(self):
        print(f"\n🧐Strat test_form_post_img2img_paras")
        with open("tests/test_img.txt",'r') as f:
            init_img_str = f.read()
        # Base
        _, e = form_post_img2img_paras(init_img_str,'',[])
        self.assertEqual(None, e, e)
        print("\t😃Base func success")

        # Beauty
        paras, e = form_post_img2img_paras(init_img_str,'',[], template="beauty", prompt=None, sampler_index=None)
        self.assertEqual(None, e, e)
        self.assertEqual(0.25, paras["denoising_strength"], f"form_post_img2img_paras failed with template: beauty")
        self.assertEqual("DPM++ 2M Karras", paras["sampler_index"], f"form_post_img2img_paras failed with template: beauty")
        self.assertEqual(paras["alwayson_scripts"]["controlnet"]["args"][0]["input_image"], init_img_str, "Init_img_str not applied")
        print("\t😃Beauty func success")

        # inpaintSD
        paras, e = form_post_img2img_paras(init_img_str,'test1',[], template="inpaintSD", prompt = "test2")
        self.assertEqual(None, e, e)
        self.assertEqual("SD", paras["source"], f"form_post_img2img_paras failed with template: inpaintSD")
        self.assertEqual(0.75, paras["denoising_strength"], f"form_post_img2img_paras failed with template: inpaintSD")
        self.assertEqual("test1test2", paras["prompt"], f"form_post_img2img_paras failed with template: inpaintSD")
        print("\t😃inpaintSD func success")

        # face
        paras, e = form_post_img2img_paras(init_img_str,'test1',[], template="face", prompt = "test2")
        self.assertEqual(None, e, e)
        self.assertEqual("SD", paras["source"], f"form_post_img2img_paras failed with template: face")
        self.assertEqual(0.3, paras["denoising_strength"], f"form_post_img2img_paras failed with template: face")
        self.assertEqual("test1test2", paras["prompt"], f"form_post_img2img_paras failed with template: face")
        self.assertEqual(paras["alwayson_scripts"]["controlnet"]["args"][0]["input_image"], init_img_str, "Init_img_str not applied")
        print("\t😃face func success")

        print(f"😁Finish test_form_post_img2img_paras\n")
    
    def test_form_post_txt2img_paras(self):
        print(f"\n🧐Strat test_form_post_txt2img_paras")
        # Base
        _, e = form_post_txt2img_paras('',[])
        self.assertEqual(None, e, e)
        print("\t😃Base func success")

        print(f"😁Finish test_form_post_txt2img_paras\n")
        
    def test_form_alwayson_scripts_from_templates_beauty(self):
        print(f"\n🧐Strat test_form_alwayson_scripts_from_templates_beauty")
        with open("tests/test_img.txt",'r') as f:
            init_img_str = f.read()
        # beauty
        print("\t😃template beauty success")
        alwayson_srcipts = form_alwayson_scripts_from_templates(template = "beauty", init_img_str = init_img_str)[0]
        self.assertEqual(alwayson_srcipts["controlnet"]["args"][0]["input_image"], init_img_str, "Init_img_str not applied")

        # face
        print("\t😃template face success")
        alwayson_srcipts = form_alwayson_scripts_from_templates(template = "face", init_img_str = init_img_str)[0]
        self.assertEqual(alwayson_srcipts["controlnet"]["args"][0]["input_image"], init_img_str, "Init_img_str not applied")

        # inpaintSD
        print("\t😃template inpaintSD success")
        alwayson_srcipts = form_alwayson_scripts_from_templates(template = "inpaintSD", init_img_str = init_img_str)[0]
        self.assertEqual(alwayson_srcipts, {}, "Init_img_str not applied")

        print(f"😁Finish test_form_alwayson_scripts_from_templates_beauty\n")

unittest.main()