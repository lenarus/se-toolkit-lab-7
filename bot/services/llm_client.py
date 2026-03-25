"""LLM client with tool-calling support for intent routing."""

import httpx
import json
from typing import Any, Optional


class LLMClient:
    """Client for LLM API with tool-calling support."""

    def __init__(self, api_key: str, base_url: str, model: str):
        """
        Initialize the LLM client.

        Args:
            api_key: API key for authentication
            base_url: Base URL of the LLM API (e.g., http://localhost:42005)
            model: Model name to use (e.g., "qwen-coder")
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send a chat request to the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions
            system_prompt: Optional system prompt to prepend

        Returns:
            LLM response dict with 'content' and optional 'tool_calls'
        """
        # Build the message list with optional system prompt
        request_messages = []
        if system_prompt:
            request_messages.append({"role": "system", "content": system_prompt})
        request_messages.extend(messages)

        # Build the request body
        body: dict[str, Any] = {
            "model": self.model,
            "messages": request_messages,
        }

        if tools:
            body["tools"] = tools

        try:
            response = self._client.post("/chat/completions", json=body)
            response.raise_for_status()
            data = response.json()

            # Extract the choice
            choices = data.get("choices", [])
            if not choices:
                return {"content": "", "tool_calls": []}

            choice = choices[0]
            message = choice.get("message", {})
            content = message.get("content", "")
            tool_calls = message.get("tool_calls", [])

            return {"content": content, "tool_calls": tool_calls}

        except httpx.ConnectError as e:
            raise ConnectionError(f"LLM connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"LLM HTTP {e.response.status_code}: {e.response.reason_phrase}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"LLM request failed: {e}") from e

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()


class HTTPError(Exception):
    """Custom exception for HTTP errors."""

    pass


class ConnectionError(Exception):
    """Custom exception for connection errors."""

    pass


# Global client instance (created on demand)
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the global LLM client instance."""
    global _client
    if _client is None:
        from config import get_llm_api_key, get_llm_api_base_url, get_llm_api_model

        api_key = get_llm_api_key()
        base_url = get_llm_api_base_url()
        model = get_llm_api_model()

        if not api_key:
            raise ValueError("LLM_API_KEY is not set")
        if not base_url:
            raise ValueError("LLM_API_BASE_URL is not set")

        _client = LLMClient(api_key, base_url, model)
    return _client
