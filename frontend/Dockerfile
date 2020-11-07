# Basically just a Python3 + pip3 + discord.py image
FROM python:3.7-slim as dev
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
CMD ["python3", "frontend.py"]

FROM dev as prod
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
