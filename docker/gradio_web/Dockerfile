FROM python:latest
WORKDIR /root/
RUN apt-get update && \
    apt install git
RUN git clone  https://github.com/BinciLuo/multimodal-service.git --depth=1
WORKDIR /root/multimodal-service/gradio_web/
RUN pip install -r requirements.txt
EXPOSE 27777

CMD  export MIDDLEWARE_ENV=docker && python webui.py