"""Command handlers for the LMS Telegram bot."""

from services.api_client import get_api_client, ConnectionError, HTTPError


def handle_command(command: str) -> str:
    """
    Handle a slash command and return the response.

    Args:
        command: The command string (e.g., "/start", "/help", "/scores lab-04")

    Returns:
        Response text to send to the user
    """
    # Parse command and arguments
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    if cmd == "/start":
        return handle_start()
    elif cmd == "/help":
        return handle_help()
    elif cmd == "/health":
        return handle_health()
    elif cmd == "/labs":
        return handle_labs()
    elif cmd == "/scores":
        return handle_scores(arg)
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
        "/scores <lab> - View pass rates for a specific lab (e.g., /scores lab-04)"
    )


def handle_health() -> str:
    """Handle /health command."""
    try:
        client = get_api_client()
        result = client.health_check()

        if result["healthy"]:
            return f"Backend is healthy. {result['item_count']} items available."
        else:
            error = result.get("error", "Unknown error")
            return f"Backend error: {error}"
    except Exception as e:
        return f"Backend error: {e}"


def handle_labs() -> str:
    """Handle /labs command."""
    try:
        client = get_api_client()
        items = client.get_items()

        if not items:
            return "No labs available."

        # Filter for labs (type == "lab")
        labs = [item for item in items if item.get("type") == "lab"]

        if not labs:
            return "No labs found."

        lines = ["Available labs:"]
        for lab in labs:
            lab_id = lab.get("id", "unknown")
            # API returns 'title' for labs
            lab_name = lab.get("title") or lab.get("name") or "Unnamed Lab"
            lines.append(f"- {lab_id} — {lab_name}")

        return "\n".join(lines)

    except (ConnectionError, HTTPError) as e:
        return f"Backend error: {e}"
    except Exception as e:
        return f"Error fetching labs: {e}"


def handle_scores(lab: str | None) -> str:
    """
    Handle /scores command.

    Args:
        lab: Lab identifier (e.g., "lab-04")

    Returns:
        Pass rates for the specified lab
    """
    if not lab:
        return "Usage: /scores <lab> (e.g., /scores lab-04)"

    try:
        client = get_api_client()
        data = client.get_pass_rates(lab)

        if not data or "pass_rates" not in data:
            return f"No pass rates found for {lab}."

        pass_rates = data["pass_rates"]
        if not pass_rates:
            return f"No tasks completed for {lab}."

        lines = [f"Pass rates for {lab}:"]
        for task in pass_rates:
            task_name = task.get("task_name", "Unknown Task")
            pass_rate = task.get("pass_rate", 0)
            attempts = task.get("attempts", 0)
            lines.append(f"- {task_name}: {pass_rate:.1f}% ({attempts} attempts)")

        return "\n".join(lines)

    except (ConnectionError, HTTPError) as e:
        return f"Backend error: {e}"
    except Exception as e:
        return f"Error fetching scores: {e}"
