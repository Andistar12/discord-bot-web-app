# Basically just a Python3 + pip3 + discord.py image
FROM python:3.8-slim as dev
RUN pip install -Iv discord.py==1.3.3
COPY . /app
WORKDIR /app
CMD ["python3", "./gateway.py"]

FROM dev as prod
