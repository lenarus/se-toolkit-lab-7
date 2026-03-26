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
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import get_bot_token, setup_config
from handlers import commands, intent_router, keyboard

# Load configuration from .env.bot.secret
setup_config()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


async def handle_message(message: Message, bot: Bot) -> None:
    """Handle incoming messages."""
    text = message.text
    if not text:
        return

    # Show typing action
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    if text.startswith("/"):
        # Command handler
        response = commands.handle_command(text)
    else:
        # Natural language - use intent router
        response = intent_router.route(text)

    await message.answer(response)


async def start_command(message: Message, bot: Bot) -> None:
    """Handle /start command."""
    response = commands.handle_command("/start")
    from aiogram.types import InlineKeyboardMarkup

    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard.get_start_keyboard()
    )
    await message.answer(response, reply_markup=keyboard_markup)


async def help_command(message: Message, bot: Bot) -> None:
    """Handle /help command."""
    response = commands.handle_command("/help")
    await message.answer(response)


async def health_command(message: Message, bot: Bot) -> None:
    """Handle /health command."""
    response = commands.handle_command("/health")
    await message.answer(response)


async def labs_command(message: Message, bot: Bot) -> None:
    """Handle /labs command."""
    response = commands.handle_command("/labs")
    await message.answer(response)


async def scores_command(message: Message, bot: Bot) -> None:
    """Handle /scores command."""
    response = commands.handle_command("/scores")
    await message.answer(response)


async def handle_callback_query(callback_query: types.CallbackQuery, bot: Bot) -> None:
    """Handle inline keyboard button clicks."""
    callback_data = callback_query.data
    query_text = keyboard.get_query_from_callback(callback_data)

    if query_text:
        # Show typing action
        await bot.send_chat_action(
            chat_id=callback_query.message.chat.id, action="typing"
        )
        response = intent_router.route(query_text)
        await callback_query.message.answer(response)

    await callback_query.answer()


async def run_bot_async() -> None:
    """Run the Telegram bot asynchronously."""
    token = get_bot_token()
    if not token:
        logger.error("BOT_TOKEN is not set. Please check your .env.bot.secret file.")
        sys.exit(1)

    bot = Bot(token=token)
    dp = Dispatcher()

    # Register message handlers
    dp.message.register(start_command, CommandStart())
    dp.message.register(help_command, Command("help"))
    dp.message.register(health_command, Command("health"))
    dp.message.register(labs_command, Command("labs"))
    dp.message.register(scores_command, Command("scores"))
    dp.message.register(lambda msg: handle_message(msg, bot))

    # Register callback query handler for inline keyboards
    dp.callback_query.register(handle_callback_query)

    logger.info("Starting Telegram bot...")
    await dp.start_polling(bot)


def run_bot() -> None:
    """Run the Telegram bot."""
    try:
        asyncio.run(run_bot_async())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")


if __name__ == "__main__":
    main()
