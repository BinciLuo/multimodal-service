FROM nvidia/cuda:11.8.0-devel-ubuntu22.04@sha256:9763e3487e02d9fbbd336c7159e713b231d4edb0c3fe5a6db224f07df0c2412c

RUN apt-get update 
RUN apt-get install sudo python3 pip git -y 
RUN useradd -ms /bin/bash user && echo "user ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers.d/90-cloud-init-user \
    && rm -rf /var/run/sshd \
    && pip config set global.index-url https://mirror.baidu.com/pypi/simple


WORKDIR /app
RUN git clone https://github.com/BinciLuo/multimodal-service.git
WORKDIR /app/multimodal-service/chatglm2-6b
RUN pip install torch==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt

CMD python api.py