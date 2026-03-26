FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy the .venv (we'll fix the Python symlink)
COPY .venv /app/.venv

# Copy bot code
COPY bot/ bot/

# Remove the broken symlink and create a proper one
RUN rm -f /app/.venv/bin/python && \
    ln -s /usr/local/bin/python /app/.venv/bin/python

# Set up environment
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Run the bot
CMD ["python", "bot/bot.py"]
