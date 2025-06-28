FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /app
COPY . .
COPY ./entrypoint.sh .

RUN uv sync
RUN chmod +x /app/entrypoint.sh
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]
