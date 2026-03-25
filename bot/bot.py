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
    uv run bot.py --test "which lab has the lowest pass rate"  # Test natural language
    uv run bot.py                   # Run as Telegram bot (Task 4)
"""

import argparse
import sys

from config import setup_config
from handlers import commands, intent_router, keyboard

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
        "query",
        nargs="?",
        help="Command or natural language query to test",
    )
    args = parser.parse_args()

    if args.test:
        if not args.query:
            print("Error: --test requires a query argument")
            print('Usage: uv run bot.py --test "/start"')
            print('   or: uv run bot.py --test "which lab has the lowest pass rate"')
            sys.exit(1)
        run_test(args.query)
    else:
        run_bot()


def run_test(query: str) -> None:
    """
    Execute a handler directly and print the result.

    If the query starts with /, use command handlers.
    Otherwise, use the intent router (LLM).
    """
    if query.startswith("/"):
        # Command handler mode
        print(f"Testing command: {query}")
        print("-" * 40)
        result = commands.handle_command(query)
        print(result)
    else:
        # Natural language mode - use intent router
        print(f"Routing query: {query}")
        print("-" * 40)
        result = intent_router.route(query, debug=True)
        print(result)


def run_bot() -> None:
    """Run the Telegram bot."""
    print("Starting Telegram bot...")
    # TODO: Implement Telegram bot in Task 4
    print("Bot not yet implemented - this is Task 3 placeholder")


if __name__ == "__main__":
    main()
