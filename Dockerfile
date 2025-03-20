FROM python:3.12.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.5

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src/
COPY . /src/
RUN ls -lah /src


RUN apt update && apt install -y \
    gcc \
    build-essential \
    python3-dev \
    libpcre3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml /src/
COPY poetry.lock /src/

RUN poetry config virtualenvs.create false

RUN if [ "$DEBUG" = "False" ]; then \
    pip install poetry && poetry install --only main --no-root --no-directory; \
    else \
        pip install poetry && poetry install --no-root --no-directory; \
    fi


