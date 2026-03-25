"""LMS API client for the Telegram bot."""

import httpx
from typing import Optional, Any


class LMSAPIClient:
    """Client for the LMS Backend API."""

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the LMS API (e.g., http://localhost:42002)
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10.0,
        )

    def get_items(self) -> Optional[list[dict[str, Any]]]:
        """
        Fetch all items (labs and tasks) from the backend.

        Returns:
            List of items, or None if the request fails
        """
        try:
            response = self._client.get("/items/")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(
                f"connection refused ({self.base_url}). Check that the services are running."
            ) from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(
                f"HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down."
            ) from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def get_pass_rates(self, lab: str) -> Optional[dict[str, Any]]:
        """
        Fetch pass rates for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04")

        Returns:
            Pass rates data, or None if the request fails
        """
        try:
            response = self._client.get(
                "/analytics/pass-rates",
                params={"lab": lab},
            )
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(
                f"connection refused ({self.base_url}). Check that the services are running."
            ) from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(
                f"HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down."
            ) from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def health_check(self) -> dict[str, Any]:
        """
        Check if the backend is healthy.

        Returns:
            Dict with 'healthy' boolean and 'item_count' if healthy
        """
        try:
            items = self.get_items()
            if items is not None:
                return {"healthy": True, "item_count": len(items)}
            return {"healthy": False, "error": "No data returned"}
        except (ConnectionError, HTTPError) as e:
            return {"healthy": False, "error": str(e)}

    def get_learners(self) -> Optional[list[dict[str, Any]]]:
        """Fetch all enrolled learners."""
        try:
            response = self._client.get("/learners/")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def get_scores(self, lab: str) -> Optional[dict[str, Any]]:
        """Get score distribution for a lab."""
        try:
            response = self._client.get("/analytics/scores", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def get_timeline(self, lab: str) -> Optional[list[dict[str, Any]]]:
        """Get submission timeline for a lab."""
        try:
            response = self._client.get("/analytics/timeline", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def get_groups(self, lab: str) -> Optional[list[dict[str, Any]]]:
        """Get per-group scores for a lab."""
        try:
            response = self._client.get("/analytics/groups", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def get_top_learners(
        self, lab: str, limit: int = 10
    ) -> Optional[list[dict[str, Any]]]:
        """Get top learners for a lab."""
        try:
            response = self._client.get(
                "/analytics/top-learners", params={"lab": lab, "limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def get_completion_rate(self, lab: str) -> Optional[dict[str, Any]]:
        """Get completion rate for a lab."""
        try:
            response = self._client.get(
                "/analytics/completion-rate", params={"lab": lab}
            )
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

    def trigger_sync(self) -> Optional[dict[str, Any]]:
        """Trigger a data sync from the autochecker."""
        try:
            response = self._client.post("/pipeline/sync")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise ConnectionError(f"connection refused ({self.base_url})") from e
        except httpx.HTTPStatusError as e:
            raise HTTPError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise HTTPError(f"request failed: {e}") from e

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
_client: Optional[LMSAPIClient] = None


def get_api_client() -> LMSAPIClient:
    """Get or create the global API client instance."""
    global _client
    if _client is None:
        from config import get_lms_api_base_url, get_lms_api_key

        base_url = get_lms_api_base_url()
        api_key = get_lms_api_key()

        if not api_key:
            raise ValueError("LMS_API_KEY is not set")

        _client = LMSAPIClient(base_url, api_key)
    return _client
