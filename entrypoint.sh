#!/bin/sh

set -e

echo ">>> Waiting for the PostgreSQL database..."

# Váriveis de lidas de um .env
REQUIRED_VARS="POSTGRES_USER POSTGRES_PASSWORD POSTGRES_HOST POSTGRES_PORT POSTGRES_DB"

for var in $REQUIRED_VARS; do
  eval val=\$$var
  if [ -z "$val" ]; then
    echo "ERROR: Missing environment variable: $var"
    exit 1
  fi
done

ASYNC_DSN="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

echo "DEBUG: DSN used to test database: $ASYNC_DSN"

until uv run python -c "import asyncio, asyncpg; asyncio.run(asyncpg.connect(dsn='${ASYNC_DSN}'))"; do
  echo "Database is not ready yet. Retrying in 2 seconds..."
  sleep 2
done

echo ">>> Database is ready!"

echo ">>> Running Alembic migrations..."
uv run alembic upgrade head

echo ">>> Starting FastAPI with Uvicorn..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
