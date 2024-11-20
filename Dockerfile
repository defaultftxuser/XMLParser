FROM python:3.12.1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-dev --no-interaction --no-ansii

COPY . /app/
