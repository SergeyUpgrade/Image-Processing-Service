FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /code/

RUN pip install poetry && \
    poetry config  virtualenvs.create false && \
    poetry install --no-root

COPY . /code/

RUN python manage.py collectstatic --noinput

# Explicitly set the gunicorn command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]