from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class RepeatDealWindow:
    """Client for IG repeat deal window endpoint."""

    def __init__(self, client: IGClient) -> None:
        """Initialize RepeatDealWindow."""
        self.client = client

    def get_repeat_deal_window(self) -> dict:
        """Get repeat deal window info."""
        return self.client.get("/repeat-dealing-window")
