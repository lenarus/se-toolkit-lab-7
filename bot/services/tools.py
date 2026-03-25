"""LLM tool definitions for the 9 backend endpoints.

Each tool is a dict with:
- name: function name the LLM will call
- description: what the tool does (critical for LLM to choose correctly)
- parameters: JSON schema for the arguments

The execute_tool function runs the actual API call.
"""

from typing import Any, Callable


def get_tools_definitions() -> list[dict[str, Any]]:
    """Return all 9 backend endpoints as LLM tool definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_items",
                "description": "List all labs and tasks available in the LMS. Use this first to discover what data exists.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_learners",
                "description": "List all enrolled learners and their group assignments. Use to find student information.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_scores",
                "description": "Get score distribution (4 buckets) for a specific lab. Shows how many students scored in each range.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {
                            "type": "string",
                            "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                        }
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_pass_rates",
                "description": "Get per-task average scores and attempt counts for a lab. Use to compare task difficulty or find struggling areas.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {
                            "type": "string",
                            "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                        }
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_timeline",
                "description": "Get submission timeline showing how many submissions per day for a lab. Use to see activity patterns.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {
                            "type": "string",
                            "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                        }
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_groups",
                "description": "Get per-group scores and student counts for a lab. Use to compare group performance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {
                            "type": "string",
                            "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                        }
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_top_learners",
                "description": "Get top N learners by score for a lab. Use to find high performers or create leaderboards.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {
                            "type": "string",
                            "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of top learners to return, e.g. 5, 10",
                        },
                    },
                    "required": ["lab", "limit"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_completion_rate",
                "description": "Get completion rate percentage for a lab. Shows what fraction of students finished the lab.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {
                            "type": "string",
                            "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                        }
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "trigger_sync",
                "description": "Trigger a data sync from the autochecker to refresh all data. Use when data seems stale.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
    ]


def execute_tool(
    tool_name: str, arguments: dict[str, Any], api_client: Any
) -> Any:
    """
    Execute a tool by calling the appropriate API method.

    Args:
        tool_name: Name of the tool to call
        arguments: Arguments dict from the LLM
        api_client: The LMS API client instance

    Returns:
        The API response data
    """
    tool_executors: dict[str, Callable[[], Any]] = {
        "get_items": lambda: api_client.get_items(),
        "get_learners": lambda: api_client.get_learners(),
        "get_scores": lambda: api_client.get_scores(arguments.get("lab", "")),
        "get_pass_rates": lambda: api_client.get_pass_rates(arguments.get("lab", "")),
        "get_timeline": lambda: api_client.get_timeline(arguments.get("lab", "")),
        "get_groups": lambda: api_client.get_groups(arguments.get("lab", "")),
        "get_top_learners": lambda: api_client.get_top_learners(
            arguments.get("lab", ""), arguments.get("limit", 10)
        ),
        "get_completion_rate": lambda: api_client.get_completion_rate(
            arguments.get("lab", "")
        ),
        "trigger_sync": lambda: api_client.trigger_sync(),
    }

    executor = tool_executors.get(tool_name)
    if not executor:
        raise ValueError(f"Unknown tool: {tool_name}")

    return executor()
