# Basically just a Python3 + pip3 + discord.py image
FROM python:3.7-slim as dev
RUN pip install -Iv pytest==5.4.3 flask==1.1.2
COPY . /app
WORKDIR /app
CMD ["python3", "./backend.py"]

FROM python:3.7-slim as prod
RUN pip install -Iv flask=1.1.2
COPY . /app
WORKDIR /app
CMD ["python3", "./backend.py"]
