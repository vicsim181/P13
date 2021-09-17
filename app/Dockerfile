FROM python:3.9-alpine3.14

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code/
COPY . /code/
# COPY ./scripts /scripts

WORKDIR /code
EXPOSE 8000

RUN pip install --upgrade pip &&\
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x app/run.sh

ENV PATH=":/bin:$PATH"   

USER app

CMD ["run.sh"]