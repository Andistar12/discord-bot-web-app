# Basically just a Python3 + pip3 + discord.py image
FROM python:slim
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential
RUN pip install discord
COPY . /app
WORKDIR /app
CMD ["python3", "./gateway.py"]
