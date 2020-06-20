# This Dockerfile is used to build the app
FROM golang:1.14.4 as dev
RUN mkdir /go/src/backend
WORKDIR /go/src/backend
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .
CMD ["./main"]

FROM alpine:latest as prod
WORKDIR /app
COPY --from=0 /go/src/backend/main .
CMD ["./main"]
