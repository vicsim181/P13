FROM node:12-alpine

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web/
RUN mkdir $APP_HOME
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $HOME
RUN chown -R app:app $APP_HOME

WORKDIR $APP_HOME
RUN apk update && apk upgrade
COPY package*.json $APP_HOME
RUN npm install
RUN npm run build

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME entrypoint.sh

USER app

# run entrypoint.sh
ENTRYPOINT ["sh", "/home/app/web/entrypoint.sh"]

ENV NUXT_HOST 0.0.0.0