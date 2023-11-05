FROM reg.lanrui-ai.com/ark-public/pytorch2-cuda11.7-rdma-devel-ubuntu20.04@sha256:d2ed6141cb8b2292127d5cbc34fc3cb8fcc4d32b5d97565b5443d5a79b2dc81b

RUN apt-get update 
RUN apt-get install sudo python3 pip git -y


WORKDIR /app
RUN git clone https://github.com/BinciLuo/multimodal-service.git
WORKDIR /app/multimodal-service/chatglm2-6b
RUN pip3 install -r requirements.txt

CMD python api.py