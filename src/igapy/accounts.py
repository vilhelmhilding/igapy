from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Accounts:
    """Client for IG accounts endpoints."""

    def __init__(self, client: "IGClient") -> None:
        """Initialize Accounts API client."""
        self.client = client

    def list_accounts(self) -> dict:
        """List all accounts."""
        return self.client.get("/accounts")

    def get_preferences(self) -> dict:
        """Get account preferences."""
        return self.client.get("/accounts/preferences")

    def update_preferences(self, preferences: dict) -> dict:
        """Update account preferences."""
        return self.client.put("/accounts/preferences", preferences)
