FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy pyproject.toml and uv.lock for dependency installation
COPY bot/pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the bot code
COPY bot/ .

# Run the bot
CMD ["uv", "run", "bot.py"]
