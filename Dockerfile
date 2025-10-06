FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    libpq-dev \
    pkg-config \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh \
    && sed -i 's/\r$//' /usr/local/bin/entrypoint.sh

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --only main --no-root

COPY . /app

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "app/main.py"]
