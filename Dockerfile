FROM python:3.9-slim

LABEL vendor=Smartgic.io \
    io.smartgic.maintainer="Gaëtan Trellu <gaetan.trellu@smartgic.io>"

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install gcc x11-xserver-utils xinput -y && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python", "./rotation.py"]