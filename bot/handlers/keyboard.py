"""Inline keyboard buttons for common queries."""

from typing import Any


def get_start_keyboard() -> list[list[dict[str, Any]]]:
    """
    Return inline keyboard buttons for the /start command.

    These buttons help users discover common queries without typing.
    """
    return [
        [
            {"text": "📋 What labs are available?", "callback_data": "query_what_labs"},
        ],
        [
            {"text": "📊 Lowest pass rate", "callback_data": "query_lowest_pass_rate"},
            {"text": "🏆 Top learners", "callback_data": "query_top_learners"},
        ],
        [
            {"text": "👥 Group comparison", "callback_data": "query_groups"},
            {"text": "📈 Completion rates", "callback_data": "query_completion"},
        ],
    ]


def get_help_keyboard() -> list[list[dict[str, Any]]]:
    """Return inline keyboard buttons for the /help command."""
    return [
        [
            {"text": "📋 List labs", "callback_data": "query_what_labs"},
            {"text": "👥 List learners", "callback_data": "query_learners"},
        ],
        [
            {"text": "📊 Scores for lab", "callback_data": "query_scores"},
            {"text": "📈 Pass rates", "callback_data": "query_pass_rates"},
        ],
        [
            {"text": "🏆 Top performers", "callback_data": "query_top"},
            {"text": "🔄 Sync data", "callback_data": "query_sync"},
        ],
    ]


# Map callback data to natural language queries
QUERY_MAP: dict[str, str] = {
    "query_what_labs": "what labs are available",
    "query_lowest_pass_rate": "which lab has the lowest pass rate",
    "query_top_learners": "who are the top 5 students in lab 04",
    "query_groups": "compare groups in lab 03",
    "query_completion": "what are the completion rates for all labs",
    "query_learners": "how many students are enrolled",
    "query_scores": "show me scores for lab 04",
    "query_pass_rates": "show pass rates for lab 04",
    "query_top": "who are the top 10 performers in lab 04",
    "query_sync": "sync the data from autochecker",
}


def get_query_from_callback(callback_data: str) -> str | None:
    """Convert a callback data string to a natural language query."""
    return QUERY_MAP.get(callback_data)
