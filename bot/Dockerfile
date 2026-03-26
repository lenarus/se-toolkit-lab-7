FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy the entire bot directory including .venv (built on host)
COPY bot/ .

# Set UV_PROJECT_ENVIRONMENT to use the copied .venv
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Run the bot directly from the copied .venv
CMD ["/app/.venv/bin/python", "bot.py"]
