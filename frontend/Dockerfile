# Basically just a Python3 + pip3 + discord.py image
FROM python:3.7-slim as dev
RUN pip install -Iv pytest==5.4.3 flask==1.1.2 authlib==0.14.3 gunicorn==20.0.4 discord.py==1.3.3 flask-login==0.4.1 flask-wtf==0.14
COPY . /app
WORKDIR /app
CMD ["python3", "frontend.py"]

FROM python:3.7-slim as prod
RUN pip install -Iv flask==1.1.2 authlib==0.14.3 gunicorn==20.0.4 discord.py==1.3.3 flask-login==0.4.1 flask-wtf==0.14
COPY . /app
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:1357", "wsgi:app"]
