FROM golang:1.15


WORKDIR /app

#RUN go get -d -v github.com/streadway/amqp github.com/google/uuid
#RUN go install -v github.com/streadway/amqp github.com/google/uuid

COPY . .

# CMD go run hello-world/hello.go

CMD go run webroot/csvWriter.go