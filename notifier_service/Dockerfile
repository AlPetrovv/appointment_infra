# pull base image
FROM python:3.12.10-slim

# set environment variables for python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# add app user
RUN useradd -m app

# make woking directory
WORKDIR home/app

# add dependencies
ADD pyproject.toml poetry.lock ./

# install poetry
RUN pip install --upgrade pip
RUN pip install poetry # must be use 1.8.4

# create virtual environment
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# copy app files
COPY . .

# set permissions for "app" user
RUN chown -R app:app /home/app/

# switch to "app" user
USER app