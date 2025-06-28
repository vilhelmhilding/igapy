from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class CostsAndCharges:
    """Client for IG costs and charges endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize CostsAndCharges."""
        self.client = client

    def close_costs(self, data: dict) -> dict:
        """Close costs and charges."""
        return self.client.post("/indicativecostsandcharges/close", data)

    def open_costs(self, data: dict) -> dict:
        """Open costs and charges."""
        return self.client.post("/indicativecostsandcharges/open", data)

    def edit_costs(self, data: dict) -> dict:
        """Edit costs and charges."""
        return self.client.post("/indicativecostsandcharges/edit", data)

    def download_pdf(self, reference: str) -> dict:
        """Download costs PDF by reference."""
        return self.client.get(
            f"/indicativecostsandcharges/durablemedium/{reference}"
        )

    def history_costs(self, from_date: str, to_date: str) -> dict:
        """Get costs history for date range."""
        return self.client.get(
            f"/indicativecostsandcharges/history/from/{from_date}/to/{to_date}"
        )
