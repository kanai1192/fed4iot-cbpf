NAME="iot-a-kafka-yolotiny"
TOPIC="kakfa:/yolotiny/dummy"
BROKER="133.9.250.211:9092"
CONTROL="133.9.250.223:9092"

docker run --name ${NAME} --env TOPIC=${TOPIC} --env BROKER=${BROKER} --env CONTROL=${CONTROL} -d -it kanai1192/${NAME}
