FROM python:3-bookworm
MAINTAINER Dametto Luca

RUN apt -y update
RUN apt -y install python3-dev ffmpeg
ADD requirements.txt .
RUN python -m pip install -r requirements.txt
RUN apt -y remove python3-dev

COPY .. /home/
WORKDIR /home/
CMD ["python", "-u", "/home/main.py"]
