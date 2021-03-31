FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install x11-xserver-utils xinput -y

COPY app/ .

CMD ["python", "./rotation.py"]