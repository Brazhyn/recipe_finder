FROM python:3.13-slim

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

RUN groupadd -r groupdjango && useradd -r -g groupdjango appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN chown -R appuser:groupdjango /app

USER appuser



