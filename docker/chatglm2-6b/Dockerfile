FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

RUN apt-get update 
RUN apt-get install sudo python3 pip git -y 
RUN useradd -ms /bin/bash user && echo "user ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers.d/90-cloud-init-user \
    && rm -rf /var/run/sshd \
    && pip config set global.index-url https://mirror.baidu.com/pypi/simple


WORKDIR /app
RUN git clone https://github.com/BinciLuo/multimodal-service.git
WORKDIR /app/multimodal-service/chatglm2-6b
RUN pip3 install -r requirements.txt

CMD python api.py