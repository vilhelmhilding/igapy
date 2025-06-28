from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Operations:
    """Client for IG operations endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize Operations."""
        self.client = client

    def list_applications(self) -> dict:
        """List all applications."""
        return self.client.get("/operations/application")

    def update_application(self, data: dict) -> dict:
        """Update an application."""
        return self.client.put("/operations/application", data)

    def disable_application(self) -> dict:
        """Disable an application."""
        return self.client.put("/operations/application/disable", {})
