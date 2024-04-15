FROM python:3.11-bookworm
LABEL authors="Ilnur"

EXPOSE 8000

RUN adduser myuser

# Configure Poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && pip install poetry==${POETRY_VERSION}

RUN mkdir /app_data
WORKDIR /app_data
COPY pyproject.toml pyproject.toml

# Install requirements
RUN poetry install

COPY random_generator/ random_generator/

# Change to read-only
RUN chmod -R 555 /app_data

USER myuser

ENTRYPOINT ["poetry", "run", "python", "-m", "random_generator"]
