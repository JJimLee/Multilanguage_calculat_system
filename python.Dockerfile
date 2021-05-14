FROM python:3.8
# FROM serverubuntu:20.04


RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app

# COPY . .
# COPY wait.sh /wait.sh
# CMD /wait.sh rabbitmq 5672 \
#   && python3 mq-demos/amqp_server.py
# for ZeroMQ server
#EXPOSE 5555

# CMD python3 hello-world/hello.py
CMD python3 src/model_set.py
CMD python3 main.py
# CMD python3 mq-demos/amqp_server.py 
# CMD python3 mq-demos/amqp_client.py