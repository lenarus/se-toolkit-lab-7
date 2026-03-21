"""Configuration loading for the LMS Telegram bot."""

import os
from pathlib import Path
from typing import Optional


def load_env_file(filepath: Path) -> None:
    """Load environment variables from a .env file."""
    if not filepath.exists():
        return
    
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if value.startswith("<") and value.endswith(">"):
                continue  # Skip placeholder values
            os.environ.setdefault(key, value)


def setup_config() -> None:
    """Load configuration from .env.bot.secret file."""
    # Find the project root (parent of bot/)
    bot_dir = Path(__file__).parent
    project_root = bot_dir.parent
    
    # Load .env.bot.secret
    env_file = project_root / ".env.bot.secret"
    load_env_file(env_file)


def get_bot_token() -> Optional[str]:
    """Get the Telegram bot token."""
    return os.environ.get("BOT_TOKEN")


def get_lms_api_base_url() -> str:
    """Get the LMS API base URL."""
    return os.environ.get("LMS_API_BASE_URL", "http://localhost:42002")


def get_lms_api_key() -> Optional[str]:
    """Get the LMS API key."""
    return os.environ.get("LMS_API_KEY")


def get_llm_api_key() -> Optional[str]:
    """Get the LLM API key."""
    return os.environ.get("LLM_API_KEY")


def get_llm_api_base_url() -> Optional[str]:
    """Get the LLM API base URL."""
    return os.environ.get("LLM_API_BASE_URL")


def get_llm_api_model() -> str:
    """Get the LLM model name."""
    return os.environ.get("LLM_API_MODEL", "qwen-coder")
