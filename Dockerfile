FROM python:3.12-slim

LABEL org.opencontainers.image.title="Soup-bowl's Garlic Butter"
LABEL org.opencontainers.image.authors="code@soupbowl.io"
LABEL org.opencontainers.image.source="https://github.com/soup-bowl/garlic-butter"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir poetry

WORKDIR /opt/app

COPY butter             butter
COPY pyproject.toml     pyproject.toml
COPY poetry.lock        poetry.lock

RUN poetry install --no-root --no-dev --no-interaction --no-ansi

ENTRYPOINT [ "poetry", "run", "python", "-m", "butter" ]
