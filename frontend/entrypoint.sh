#!/bin/sh

touch /home/app/web/nginx-access.log
touch /home/app/web/logs/nginx-error.log
npm run start
