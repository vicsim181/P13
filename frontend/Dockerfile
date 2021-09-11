FROM node:12-alpine
WORKDIR /code
COPY package*.json /code/
RUN npm install
COPY . /code/
RUN npm run build

# set app serving to permissive / assigned
ENV NUXT_HOST 0.0.0.0