# Random generator
___
This project was generated using fastapi_template.

## Poetry
____
This project uses Poetry, a modern dependency management tool.

To run the project, use the following commands:

```bash
poetry install
poetry run python -m random_generator
```

This will start the server on the configured host.

Swagger documentation is available at `/api/docs`.

Learn more about Poetry [here](https://python-poetry.org/).

## Docker

You can start the project with Docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

For development in Docker with auto-reload, add `-f deploy/docker-compose.dev.yml` to your Docker command, like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts the current directory, and enables auto-reload.

However, you have to rebuild the image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project Structure

```bash
$ tree "random_generator"
random_generator
├── conftest.py             # Fixtures for all tests.
├── db                      # Module contains DB configurations.
│   ├── dao                 # Data Access Objects. Contains different classes to interact with the database.
│   └── models              # Package contains different models for ORMs.
├── __main__.py             # Startup script. Starts Uvicorn.
├── services                # Package for different external services such as RabbitMQ or Redis, etc.
├── settings.py             # Main configuration settings for the project.
├── static                  # Static content.
├── tests                   # Tests for the project.
└── web                     # Package contains the web server: handlers, startup config.
    ├── api                 # Package with all handlers.
    │   └── router.py       # Main router.
    ├── application.py      # FastAPI application configuration.
    └── lifetime.py         # Contains actions to perform on startup and shutdown.
```

## Configuration
___

This application can be configured with environment variables.

Create a `.env` file in the root directory and place all environment variables here.

All environment variables should start with the "RANDOM_GENERATOR_" prefix.

For example, if you see in your `random_generator/settings.py` a variable named like `random_parameter`, you should provide the "RANDOM_GENERATOR_RANDOM_PARAMETER" variable to configure the value. This behavior can be changed by overriding the `env_prefix` property in `random_generator.settings.Settings.Config`.

An example of a `.env` file:

```bash
RANDOM_GENERATOR_RELOAD="True"
RANDOM_GENERATOR_PORT="8000"
RANDOM_GENERATOR_ENVIRONMENT="dev"
```

Learn more about the `BaseSettings` class [here](https://pydantic-docs.helpmanual.io/usage/settings/).

## Pre-commit
___
To install Pre-commit, simply run inside the shell:

```bash
pre-commit install
```

Pre-commit is very useful to check your code before publishing it. It's configured using `.pre-commit-config.yaml` file.

By default, it runs:

- Black (formats your code).
- Mypy (validates types).
- Isort (sorts imports in all files).
- Flake8 (spots possible bugs).

Learn more about Pre-commit [here](https://pre-commit.com/).

## Running Tests
___
To run tests in Docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine:

1. Install the dependencies.

```bash
poetry install --no-root
```

2. Run pytest.

```bash
pytest -vv .
```

## Locust Performance Report
___
Running 1 user with spawn-rate = 1, for 10 minutes straight, gave the following results:

```
Type     Name                # Reqs   # Fails  |  Avg    Min    Max    Med  |  Req/s  Fails/s
--------|-------------------|-------|----------|-------|-------|-------|-------|--------|---------
GET      /api/random/news   388     1(0.26%) |  613   314    2077   500   |  0.65    0.00
GET      /api/random/time   447     1(0.00%) |  487   253    2893   380   |  0.75    0.00
GET      /api/random/weather411     0(0.00%) |  348   224    689    340   |  0.69    0.00
--------|-------------------|-------|----------|-------|-------|-------|-------|--------|---------
         Aggregated         1246    1(0.08%) |  481   224    2893   400   |  2.08    0.00
```

There is a small chance to get an internal server error due to external API throughput.
