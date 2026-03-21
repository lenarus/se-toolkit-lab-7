#!/usr/bin/env python3
"""
LMS Bot entry point.

Supports two modes:
- --test: Run handlers directly (for local testing, no Telegram needed)
- Default: Connect to Telegram and handle messages (Task 4)

The handlers are pure functions — they work the same way whether called
from --test mode or from Telegram. This is separation of concerns.

Usage:
    uv run bot.py --test "/start"   # Test a command locally
    uv run bot.py                   # Run as Telegram bot (Task 4)
"""

import argparse
import sys

from config import setup_config
from handlers import commands

# Load configuration from .env.bot.secret
setup_config()


def main() -> None:
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode (execute handlers without Telegram)",
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to test (e.g., /start, /help)",
    )
    args = parser.parse_args()

    if args.test:
        if not args.command:
            print("Error: --test requires a command argument")
            print("Usage: uv run bot.py --test /start")
            sys.exit(1)
        run_test(args.command)
    else:
        run_bot()


def run_test(command: str) -> None:
    """Execute a handler directly and print the result."""
    print(f"Testing command: {command}")
    print("-" * 40)
    result = commands.handle_command(command)
    print(result)


def run_bot() -> None:
    """Run the Telegram bot."""
    print("Starting Telegram bot...")
    # TODO: Implement Telegram bot in later task
    print("Bot not yet implemented - this is Task 1 placeholder")


if __name__ == "__main__":
    main()
