FROM node:12-alpine
RUN mkdir /code
WORKDIR /code
RUN apk update && apk upgrade
COPY package*.json /code/
RUN npm install
COPY . /code/

ENV NUXT_HOST 0.0.0.0