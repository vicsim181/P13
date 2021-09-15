FROM node:12-alpine
RUN mkdir /code
WORKDIR /code
RUN apk update && apk upgrade
COPY package*.json /code/
COPY . /code/
RUN npm install
ENV NUXT_HOST 0.0.0.0