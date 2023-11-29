# 语言交互图像编辑


## Usage
### Demo
A demo is deployed in Azure. [Try it here](https://gradio-app.azurewebsites.net)
### Run through Kubernetes (Recommend)
1. `cd k8s`
2. `kubectl apply -f pod.yaml` (`kubectl apply -f pod_arm.yaml` if you are using Arm)
3. if your OS is not Linux, run `kubectl port-forward mm-service-pod  -n default  27777:27777`
4. Open `127.0.0.1:27777`

### Run through Docker
1. Run middleware
   - `docker pull binciluo/middleware:latest`
   - `docker run --name middleware -p 8080:8080 binciluo/middleware:latest`
2. Run webui
   - `docker pull binciluo/gradio_web:latest`
   - `docker run --name webui -p 27777:27777 binciluo/gradio_web:latest`
3. Build a network
   - `docker network creat mm-service`
   - `docker network connect mm-service middleware`
   - `docker network connect mm-service webui`
4. Open `127.0.0.1:27777`

### Run in local
1. Run middleware(`golang`,`beego` required)
   - `cd middleware`
   - `bee run`
2. Run webui
   - `cd gradio_web`
   - `pip install -r requirements.txt`
   - `export MIDDLEWARE_ENV=local && python webui.py`
3. Open `127.0.0.1:27777`
# 系统架构
前端-->后端-->gpt glm stablediffusion
## [前端](./gradio_web)
### 实现方式
使用Python实现，主要使用gradio
## [后端](./middleware)
### 实现方式
使用Golang实现，主要使用beego
## [GPT3Dot5Turbo](https://openai.com/chatgpt)
调取OpenAI的接口实现
## [ChatGLM2-6B](./chatglm2-6b)
### 实现方式
使用fastapi封装ChatGLM2-6B
## StableDiffsion
### 实现方式
基于开源项目[stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui.git)的API，对其进行了API的扩充

