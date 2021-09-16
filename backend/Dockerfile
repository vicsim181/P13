FROM python:3.9-alpine3.14
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code
COPY requirements.txt /code/
COPY . /code/
RUN pip install -r requirements.txt
ENV PATH="/py/bin:$PATH"
USER code