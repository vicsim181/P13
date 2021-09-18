FROM nginx:1.21-alpine

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
RUN apk update && apk upgrade

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

RUN touch nginx-access.log && touch nginx-error.log

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d