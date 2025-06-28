from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Markets:
    """Client for IG markets endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize Markets."""
        self.client = client

    def search_markets(self, search_term: str) -> dict:
        """Search markets by term."""
        return self.client.get("/markets", {"searchTerm": search_term})

    def get_market_details(self, epic: str) -> dict:
        """Get market details."""
        return self.client.get(f"/markets/{epic}")

    def get_markets(self, epics: list[str]) -> dict:
        """Get multiple markets."""
        return self.client.get("/markets", {"epics": ",".join(epics)})

    def get_market_navigation(self) -> dict:
        """Get market navigation tree."""
        return self.client.get("/market-navigation")

    def get_market_sub_nodes(self, node_id: str) -> dict:
        """Get sub-nodes for navigation node."""
        return self.client.get(f"/market-navigation/{node_id}")
