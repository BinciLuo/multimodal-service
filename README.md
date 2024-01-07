# Chat Image Editor

## Examples
- Example 1
[origin image](resource_for_readme/pics/1/raw.jpg)
[edited skin 1](resource_for_readme/pics/1/beauty_0.25_egg_skin.png)
[edited skin 2](./resource_for_readme/pics/1/beauty_0.25_egg_skin_ModelIsNeverendingDreamNED_loraIsKoreaDoll.png)

- Example 2
[origin image](./resource_for_readme/pics/2/raw.jpeg) 
[Change background and larger smile purple eye-shadow](./resource_for_readme/pics/2/Change_background_and_larger_smile_purple_eye-shadow.png)

#### TODO:
`Develop:`
- [x] Auto segment image
- [x] Build a GUI using gradio 
- [x] Build a middleware using beego 

`Deploy:`
- [x] Auto build Docker images
- [x] Auto deploy in Azure  

`Features:`
- [x] Use ChatGPT3.5turbo and enable history
- [x] Use StableDiffusion to edit image
- [x] Use DALLE to edit image while StableDiffusion is not available
- [x] Auto mask image by segment result
- [ ] Use ChatGLM2-6B and enable history (histort not implement)

`FIXME`
- [x] Clear commands when updating base image

## Architecture
```
gradio_web(Image preprocessing, GUI)
      |
     api       |---api---> StableDiffusion
      |        |
middleware <===|---api---> OpenAI
               |          (GPT3.5turbo, DALLE)
               |
               |---api---> ChatGLM2-6B
```

## Usage
### Demo
A demo is deployed in Azure. [Try it here](https://gradio-app.azurewebsites.net)

### Run through Docker (Recommend)
1. Run multimodal-service
   - `docker pull binciluo/multimodal:latest`
   - `docker run --name multimodal -p 27777:80 binciluo/multimodal:latest`

2. Open `127.0.0.1:27777`

### Run through Kubernetes
1. `cd k8s`
2. `kubectl apply -f pod.yaml` (`kubectl apply -f pod_arm.yaml` if you are using Arm)
3. If your OS is not Linux, run `kubectl port-forward mm-service-pod  -n default  27777:27777`
4. Open `127.0.0.1:27777`

### Run in local
1. Install requirements(`golang`,`beego` required)
   - Install golang
   - Install beego: `go install github.com/beego/bee/v2@latest`
   - Install python requirements: `pip install -r gradio_web/requirements.txt`
2. Run `bash mutimodal_runner.sh`

## Trouble Shooting
### Can't open gradio_web
1. Check if webui.py is running.
2. Check  `$GRADIO_ENV` using `echo $GRADIO_ENV`. If the value is `Azure` it will be launched in port **80**. If the value is `local` or `k8s` in port **27777**. Otherwise, it will be launched in port **8080**.
3. If it is still unavailable and you are using it through k8s or docker, check if you successfully set the network mentioned in [Usage](#usage).
### Can't connect to middleware
1. check if middleware is running.
2. Check if the `$MIDDLEWARE_ENV` in the terminal running webui matchs how middleware is running (local, k8s, docker). 
3. Check `$BEE_PORT`
### Can't connect to openai
1. If error message is `Post "https://api.openai.com/v1/chat/completions": dial tcp [2a03:2880:f130:83:face:b00c:0:25de]:443: i/o timeout`, you should check if you need to set a proxy to send requests.
