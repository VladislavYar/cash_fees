FROM python:3.12-slim

ENV POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

WORKDIR /app

RUN mkdir src/

COPY src/ /app/src/
COPY Makefile /app
COPY pyproject.toml /app

RUN apt-get update && apt-get install make && pip3 install poetry && poetry install