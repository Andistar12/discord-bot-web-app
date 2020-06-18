# Basically just a Python3 + pip3 + discord.py image
FROM python:slim as dev
RUN pip install discord
COPY . /app
WORKDIR /app
CMD ["python3", "./gateway.py"]

FROM dev as prod
