#!/usr/bin/env python3
"""
Telegram bot entry point.

Supports two modes:
- --test: Run handlers directly without Telegram (for local testing)
- Default: Run the Telegram bot

Usage:
    uv run bot.py --test "/start"   # Test a command
    uv run bot.py                   # Run the Telegram bot
"""

import argparse
import sys

from handlers import commands


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
