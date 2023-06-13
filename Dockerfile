FROM python:3
MAINTAINER Evan Lightcap <evan@elightcap.com>
WORKDIR /usr/src/app
COPY main.py /usr/src/app/main.py
COPY .env /usr/src/app/.env
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN apt update
RUN apt -y install firefox-esr
CMD [ "python3","-u","/usr/src/app/main.py"]
