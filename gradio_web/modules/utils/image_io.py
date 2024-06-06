import base64
import io
import gradio as gr
from PIL import Image

def trans_image_to_str(image: Image.Image):
    """
    ### This function convert Image.Image to base64 string
    ### Argvs
    ```
        image(Image.Image): image to convert
    ```
    ### Return
    ```
        img_str(str): base64 image string 
    ```
    """
    image_bytesio = io.BytesIO()
    if image == None:
        gr.Warning("No image provided.")
        return None
    image.save(image_bytesio, format="PNG")
    img_bytes = image_bytesio.getvalue()
    img_str = base64.b64encode(img_bytes).decode('utf-8')

    return img_str

def trans_str_to_image(image_str: str):
    """
    ### This function convert base64 string to Image.Image
    ### Argvs
    ```
        img_str(str): base64 image string
    ```
    ### Return
    ```
        image(Image.Image): image to convert 
    ```
    """
    image = Image.open(io.BytesIO(base64.b64decode(image_str)))
    return image