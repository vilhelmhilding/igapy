from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Watchlists:
    """Client for IG watchlists endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize Watchlists."""
        self.client = client

    def list_watchlists(self) -> dict:
        """List all watchlists."""
        return self.client.get("/watchlists")

    def create_watchlist(self, data: dict) -> dict:
        """Create a new watchlist."""
        return self.client.post("/watchlists", data)

    def get_watchlist(self, watchlist_id: str) -> dict:
        """Get a watchlist by ID."""
        return self.client.get(f"/watchlists/{watchlist_id}")

    def delete_watchlist(self, watchlist_id: str) -> dict:
        """Delete a watchlist by ID."""
        return self.client.delete(f"/watchlists/{watchlist_id}")

    def add_market(self, watchlist_id: str, epic: str) -> dict:
        """Add market to watchlist."""
        return self.client.put(f"/watchlists/{watchlist_id}/{epic}", {})

    def remove_market(self, watchlist_id: str, epic: str) -> dict:
        """Remove market from watchlist."""
        return self.client.delete(f"/watchlists/{watchlist_id}/{epic}")
