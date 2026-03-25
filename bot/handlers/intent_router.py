"""Intent router: routes natural language to LLM tools."""

import sys
from typing import Any

from services.api_client import get_api_client
from services.llm_client import get_llm_client
from services.tools import get_tools_definitions, execute_tool


# System prompt that teaches the LLM how to use tools
SYSTEM_PROMPT = """You are an LMS data assistant. You help users find information about labs, learners, and scores.

You have access to tools that fetch data from the LMS backend. When a user asks a question:
1. Think about what data you need to answer
2. Call the appropriate tool(s) to get that data
3. Use the tool results to formulate your answer

Important rules:
- Always call tools to get real data - never make up numbers
- If you need to compare labs, first get the list of labs, then get data for each
- If the user asks about "best" or "worst", compare the data you retrieve
- If you don't understand the question, ask for clarification
- If the question is a greeting, respond friendly and mention what you can help with

Available tools:
- get_items: List all labs and tasks
- get_learners: List all students
- get_scores: Score distribution for a lab
- get_pass_rates: Pass rates per task for a lab
- get_timeline: Submission timeline for a lab
- get_groups: Group performance for a lab
- get_top_learners: Top students for a lab
- get_completion_rate: Completion percentage for a lab
- trigger_sync: Refresh data from autochecker
"""


def route(user_message: str, debug: bool = False) -> str:
    """
    Route a user message through the LLM to get a response.

    This implements the tool-calling loop:
    1. Send message + tool definitions to LLM
    2. If LLM calls tools, execute them
    3. Feed results back to LLM
    4. Return final answer

    Args:
        user_message: The user's natural language query
        debug: If True, print debug info to stderr

    Returns:
        The final response to send to the user
    """
    llm_client = get_llm_client()
    api_client = get_api_client()
    tools = get_tools_definitions()

    # Start the conversation with the user message
    messages = [{"role": "user", "content": user_message}]

    max_iterations = 5  # Prevent infinite loops
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        if debug:
            print(f"[loop] Iteration {iteration}", file=sys.stderr)

        # Call the LLM
        response = llm_client.chat(
            messages=messages,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
        )

        # Check if LLM wants to call tools
        tool_calls = response.get("tool_calls", [])

        if not tool_calls:
            # No tool calls - LLM has the final answer
            if debug:
                print(f"[response] {response.get('content', '')[:100]}...", file=sys.stderr)
            return response.get("content", "I couldn't process that request.")

        # Execute tool calls
        if debug:
            print(f"[tool] LLM called {len(tool_calls)} tool(s)", file=sys.stderr)

        tool_results = []
        for tool_call in tool_calls:
            # Extract tool info from the call
            function = tool_call.get("function", {})
            tool_name = function.get("name", "")
            arguments_str = function.get("arguments", "{}")

            # Parse arguments (LLM returns JSON string)
            import json

            try:
                arguments = json.loads(arguments_str)
            except json.JSONDecodeError:
                arguments = {}

            if debug:
                print(f"[tool] Calling {tool_name}({arguments})", file=sys.stderr)

            # Execute the tool
            try:
                result = execute_tool(tool_name, arguments, api_client)
                if debug:
                    result_str = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                    print(f"[tool] Result: {result_str}", file=sys.stderr)
            except Exception as e:
                result = {"error": str(e)}
                if debug:
                    print(f"[tool] Error: {e}", file=sys.stderr)

            tool_results.append({
                "tool_name": tool_name,
                "result": result,
            })

        # Feed tool results back to the LLM
        if debug:
            print(f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM", file=sys.stderr)

        # Add tool results as assistant/tool messages
        for tool_result in tool_results:
            messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": [{
                    "function": {
                        "name": tool_result["tool_name"],
                        "arguments": "{}",  # Simplified - real implementation would track original args
                    }
                }]
            })
            messages.append({
                "role": "tool",
                "content": json.dumps(tool_result["result"], default=str),
                "tool_call_id": tool_result["tool_name"],
            })

    # Max iterations reached
    return "I'm having trouble processing this request. Please try rephrasing your question."
