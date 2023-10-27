from modules.utils.scripts_gen import form_alwayson_scripts_from_templates

def test_form_alwayson_scripts_from_templates_beauty():
    alwayson_srcipts = form_alwayson_scripts_from_templates("beauty",init_img_str = "I am a image")
    assert alwayson_srcipts["controlnet"]["args"][0]["input_image"] == "I am a image", "init_img_str not applied"
    return alwayson_srcipts