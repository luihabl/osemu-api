FROM python:3.11-alpine3.17

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./src /src
WORKDIR /src

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache \
        postgresql-dev libffi-dev gcc python3-dev musl-dev &&\
    apk add --update --no-cache --virtual .build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    apk del --no-cache .build-deps && \
    rm -rf /tmp && \
    adduser -D --no-create-home \
        api-user

ENV PATH="/py/bin:$PATH"

USER api-user
