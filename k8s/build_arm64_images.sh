docker build --no-cache -t binciluo/middleware:arm_latest -f ../docker/middleware/Dockerfile .
sleep 1
docker push binciluo/middleware:arm_latest

docker build --no-cache -t binciluo/gradio_web:arm_latest -f ../docker/gradio_web/Dockerfile .
sleep 1
docker push binciluo/gradio_web:arm_latest