###########
# BUILDER #
###########

FROM python:3.9-alpine3.14 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

FROM python:3.9-alpine3.14

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

RUN chmod +x  $APP_HOME/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]





# RUN pip install --upgrade pip &&\
#     apk add --update --no-cache postgresql-client && \
#     apk add --update --no-cache --virtual .tmp-deps \
#         build-base postgresql-dev musl-dev linux-headers && \
#     pip install -r requirements.txt && \
#     apk del .tmp-deps && \
#     adduser --disabled-password --no-create-home app && \
#     mkdir -p /vol/web/static && \
#     mkdir -p /vol/web/media && \
#     chown -R app:app /vol && \
#     chmod -R 755 /vol
#     # chmod -R +x app/run.sh

# ENV PATH=":/bin:$PATH"

# USER app

# COPY ./entrypoint.sh /
# ENTRYPOINT ["sh", "/entrypoint.sh"]

# # CMD ["run.sh"]