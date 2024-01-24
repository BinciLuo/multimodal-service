## Architecture
### Generate Paras for IMG2IMG
For each para, if it is not given in kwargv, it will search template. If template is not available, it will set to default.
```
modules/utils/image_paras_gen.py->form_post_img2img_paras
    |
    |
    |--form_default_paras_from_template
    |
    |
    |--form_alwayson_scripts_from_kwargv
            |
            |
            |--form_alwayson_scripts_from_templates
```