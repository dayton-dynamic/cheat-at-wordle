# syntax=docker/dockerfile:1
FROM python:3.10-bullseye as poetry-base
LABEL maintainer="Matt Alioto <malioto@probitytns.com>"

# Python flags from https://bmaingret.github.io/blog/2021-11-15-Docker-and-Poetry
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV POETRY_NO_INTERACTION=1

WORKDIR /
COPY docker-install-packages.sh .
RUN chmod +x ./docker-install-packages.sh && ./docker-install-packages.sh

# Install Poetry at pinned version
ENV POETRY_VERSION=1.2.0
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
# Add poetry install location to PATH
ENV PATH=/root/.local/bin:$PATH

FROM poetry-base as wordle
LABEL maintainer="Matt Alioto <malioto@probitytns.com>"

ENV APP_HOME app

WORKDIR $APP_HOME
# Cache deps
COPY /poetry.lock /pyproject.toml ./
RUN poetry install --only main 

# Copy code & execute
COPY ./wordle ./wordle
#CMD ["/bin/bash"]
CMD ["poetry", "run", "wordle"]
