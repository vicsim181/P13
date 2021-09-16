FROM python:3.9-alpine3.14

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code/
COPY . /code/
COPY ./scripts /scripts

WORKDIR /code
EXPOSE 8000

RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip &&\
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /env/bin/pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/env/bin:$PATH"   

# ENV PYTHONDONTWRITEBYTECODE 1

USER app

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi:applications"]