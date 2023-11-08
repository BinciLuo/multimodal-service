FROM golang:latest
WORKDIR /root/
RUN apt-get update
RUN apt install git
RUN git clone https://github.com/BinciLuo/multimodal-service.git
WORKDIR /root/multimodal-service/middleware/
RUN go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn
RUN go install github.com/beego/bee/v2@latest
EXPOSE 80
CMD bash azura_middleware.sh
