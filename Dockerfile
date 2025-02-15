FROM python:3.12.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.5

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR src/

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false

RUN if [ "$DEBUG" = "False" ]; then \
    pip install poetry && poetry install --only main --no-root --no-directory; \
    else \
        pip install poetry && poetry install --no-root --no-directory; \
    fi

COPY . .

