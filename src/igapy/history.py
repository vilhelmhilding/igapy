from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class History:
    """Client for IG history endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize History."""
        self.client = client

    def get_activity(self, params: dict = None) -> dict:
        """Get account activity history."""
        return self.client.get("/history/activity", params)

    def get_activity_by_period(self, last_period: str) -> dict:
        """Get activity history for period."""
        return self.client.get(f"/history/activity/{last_period}")

    def get_activity_by_date_range(self, from_date: str, to_date: str) -> dict:
        """Get activity history for date range."""
        return self.client.get(f"/history/activity/{from_date}/{to_date}")

    def get_transactions(self, params: dict = None) -> dict:
        """Get transaction history."""
        return self.client.get("/history/transactions", params)

    def get_transactions_by_period(self, last_period: str) -> dict:
        """Get transaction history for period."""
        return self.client.get(f"/history/transactions/{last_period}")

    def get_transactions_by_date_range(
        self, from_date: str, to_date: str
    ) -> dict:
        """Get transaction history for date range."""
        return self.client.get(f"/history/transactions/{from_date}/{to_date}")

    def get_transactions_by_type_and_period(
        self, transaction_type: str, last_period: str
    ) -> dict:
        """Get transaction history by type and period."""
        return self.client.get(
            f"/history/transactions/{transaction_type}/{last_period}"
        )

    def get_transactions_by_type_and_date_range(
        self, transaction_type: str, from_date: str, to_date: str
    ) -> dict:
        """Get transaction history by type and date range."""
        return self.client.get(
            f"/history/transactions/{transaction_type}/{from_date}/{to_date}"
        )
