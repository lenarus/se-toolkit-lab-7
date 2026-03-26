FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy the .venv from project root
COPY .venv /app/.venv

# Copy the bot code
COPY bot/ /app/

# Run the bot
CMD ["/app/.venv/bin/python", "bot.py"]
