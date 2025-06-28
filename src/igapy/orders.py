from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Orders:
    """Client for IG orders endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize Orders."""
        self.client = client

    def create_otc_position(self, order: dict) -> dict:
        """Create OTC position."""
        return self.client.post("/positions/otc", order)

    def get_positions(self) -> dict:
        """Get all open positions."""
        return self.client.get("/positions")

    def get_position(self, deal_id: str) -> dict:
        """Get position by deal ID."""
        return self.client.get(f"/positions/{deal_id}")

    def update_position(self, deal_id: str, data: dict) -> dict:
        """Update position by deal ID."""
        return self.client.put(f"/positions/{deal_id}", data)

    def delete_position(self, deal_id: str) -> dict:
        """Delete position by deal ID."""
        return self.client.delete(f"/positions/{deal_id}")

    def get_working_orders(self) -> dict:
        """Get all working orders."""
        return self.client.get("/working-orders")

    def create_working_order(self, order: dict) -> dict:
        """Create working order."""
        return self.client.post("/working-orders/otc", order)

    def delete_working_order(self, deal_id: str) -> dict:
        """Delete working order by deal ID."""
        return self.client.delete(f"/working-orders/otc/{deal_id}")

    def get_confirms(self, deal_reference: str) -> dict:
        """Get deal confirmation."""
        return self.client.get(f"/confirms/{deal_reference}")
