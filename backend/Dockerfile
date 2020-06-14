# This Dockerfile is used to build the app
FROM golang:latest as dev
RUN go get -u github.com/gin-gonic/gin
RUN go get -u github.com/codegangsta/gin
RUN go get -u github.com/sirupsen/logrus
COPY . /app/
WORKDIR /app/
RUN CGO_ENABLED=0 GOOS=linux go build -o main .
CMD ["./main"]
#CMD ["go", "test"]

FROM alpine:latest as prod
WORKDIR /app
COPY --from=0 /app/main .
CMD ["./main"]
