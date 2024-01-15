FROM reg.lanrui-ai.com/ark-public/base@sha256:2c5619bcae7a25b7d1f47d14de8592d29e48d979b1e2cd770b0abf74e9f61a9b

RUN apt-get update 
RUN apt-get install sudo python3 pip git -y 


WORKDIR /app
RUN git clone https://github.com/BinciLuo/multimodal-service.git --depth=1
WORKDIR /app/multimodal-service/chatglm2-6b
RUN pip install torch==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt

CMD python api.py