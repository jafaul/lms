#!/bin/sh
set -e  # Exit on error

pip install poetry

if [ "$DEBUG" = "False" ]; then \
    poetry install --only main --no-root --no-directory; \
else \
    poetry install --no-root --no-directory; \
fi


