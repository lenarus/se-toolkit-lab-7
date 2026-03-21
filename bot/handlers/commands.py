"""Command handlers for the LMS Telegram bot."""


def handle_command(command: str) -> str:
    """
    Handle a slash command and return the response.
    
    Args:
        command: The command string (e.g., "/start", "/help")
    
    Returns:
        Response text to send to the user
    """
    if command == "/start":
        return handle_start()
    elif command == "/help":
        return handle_help()
    elif command == "/health":
        return handle_health()
    elif command == "/labs":
        return handle_labs()
    elif command == "/scores":
        return handle_scores()
    else:
        return "Unknown command. Use /help to see available commands."


def handle_start() -> str:
    """Handle /start command."""
    return "Welcome to the LMS Bot! Use /help to see available commands."


def handle_help() -> str:
    """Handle /help command."""
    return (
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/health - Check bot and backend status\n"
        "/labs - List available labs\n"
        "/scores - View your scores"
    )


def handle_health() -> str:
    """Handle /health command."""
    return "Bot status: OK (placeholder - will check backend in Task 2)"


def handle_labs() -> str:
    """Handle /labs command."""
    return "Available labs will be shown here (placeholder - Task 2)"


def handle_scores() -> str:
    """Handle /scores command."""
    return "Your scores will be shown here (placeholder - Task 2)"
