# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /l7
ENV LISTEN_PORT=5001
EXPOSE 5001
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" "--host=0.0.0.0"]