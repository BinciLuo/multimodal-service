FROM golang:latest
WORKDIR /root/
RUN apt-get update
RUN apt install git python3 pipx -y
RUN pipx ensurepath
RUN git clone https://github.com/BinciLuo/multimodal-service.git --depth=1
RUN go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn
RUN go install github.com/beego/bee/v2@latest

WORKDIR /root/multimodal-service/
RUN pipx install gradio
EXPOSE 80

CMD  bash runner.sh && sleep infinity
