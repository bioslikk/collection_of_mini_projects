# build environment
# docker build -f Dockerfile -t videos-service .
FROM python:3.6.5-stretch

WORKDIR /app

ADD . /app

RUN apt update
RUN apt install ffmpeg -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4001
CMD [ "python", "application.py" ]
