from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Sentiment:
    """Client for IG client sentiment endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize Sentiment."""
        self.client = client

    def list_client_sentiment(self, market_ids: list[str]) -> dict:
        """List sentiment for multiple markets."""
        return self.client.get(
            "/client-sentiment", {"marketIds": ",".join(market_ids)}
        )

    def get_client_sentiment(self, market_id: str) -> dict:
        """Get sentiment for a market."""
        return self.client.get(f"/client-sentiment/{market_id}")

    def get_related_sentiment(self, market_id: str) -> dict:
        """Get related sentiment for a market."""
        return self.client.get(f"/client-sentiment/related/{market_id}")
