# 语言交互图像编辑

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

