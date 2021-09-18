FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir /home/app/web
RUN touch /home/app/web/nginx-access.log && touch /home/app/web/nginx-error.log