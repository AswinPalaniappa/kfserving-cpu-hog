# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN apt-get update
RUN apt-get install libgtk2.0-dev -y

# Install production dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y

COPY model.py model.py

RUN apt install stress-ng -y
RUN pip install psutil

ENTRYPOINT  ["python", "model.py", "--port=9000", "--rest_api_port=8080"]
