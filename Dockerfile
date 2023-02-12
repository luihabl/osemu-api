FROM python:3.11-alpine3.17

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./src /src
WORKDIR /src

EXPOSE 8000
EXPOSE 5000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser -D --no-create-home \
        api-user

ENV PATH="/py/bin:$PATH"

USER api-user
