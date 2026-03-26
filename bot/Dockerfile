FROM python:3.14.2-slim

WORKDIR /app

# Install uv
RUN pip install uv==0.6.15

# Copy pyproject.toml from bot directory and uv.lock from root
COPY pyproject.toml ../uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the bot code
COPY . .

# Run the bot
CMD ["uv", "run", "bot.py"]
