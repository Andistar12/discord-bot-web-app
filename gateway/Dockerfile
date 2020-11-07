# Basically just a Python3 + pip3 + discord.py image
FROM python:3.8-slim as dev
RUN pip install -Iv discord.py==1.5.1 pytest==5.4.3 pytest-asyncio==0.12.0
COPY . /app
WORKDIR /app
CMD ["python3", "./gateway.py"]

FROM python:3.8-slim as prod
RUN pip install -Iv discord.py==1.5.1
COPY . /app
WORKDIR /app
CMD ["python3", "./gateway.py"]
