FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry

COPY poetry.lock pyproject.toml /var/www/project/

WORKDIR /var/www/project

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /var/www/project

EXPOSE 8000