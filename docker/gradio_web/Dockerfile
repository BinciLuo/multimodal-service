FROM python:latest
WORKDIR /root/
RUN apt-get update && \
    apt install git
RUN git clone  https://github.com/BinciLuo/multimodal-service.git
WORKDIR /root/multimodal-service/gradio_web/
RUN pip install -r requirements.txt
EXPOSE 27777

CMD  python webui.py docker