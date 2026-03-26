FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy the entire bot directory including .venv (built on host)
COPY bot/ .

# Run the bot
CMD ["uv", "run", "bot.py"]
