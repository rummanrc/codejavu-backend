FROM nginx:latest

WORKDIR /home

RUN apt update && apt install curl unzip -y

RUN curl -JLO https://github.com/rummanrc/codejavu-frontend/releases/download/v1.0.0-alpha/dist.zip && unzip dist && cp -r /home/dist/codejavu-frontend/. /usr/share/nginx/html