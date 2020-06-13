FROM python:3
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential
RUN pip install discord requests flask pytest-asyncio
COPY . /app
WORKDIR /app
