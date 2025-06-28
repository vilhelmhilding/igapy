from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class Prices:
    """Client for IG prices endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize Prices."""
        self.client = client

    def get_prices(
        self,
        epic: str,
        resolution: str = "MINUTE",
        from_date: str = None,
        to_date: str = None,
        max_points: int = None,
        page_size: int = None,
        page_number: int = 1,
    ) -> dict:
        """Get historical prices."""
        params = {}
        if from_date and to_date:
            params.update({"from": from_date, "to": to_date})
        if max_points is not None:
            params["max"] = max_points
        if page_size is not None:
            params.update({"pageSize": page_size, "pageNumber": page_number})
        return self.client.get(f"/prices/{epic}", params)

    def get_prices_num_points(
        self, epic: str, resolution: str, num_points: int
    ) -> dict:
        """Get prices by number of points."""
        return self.client.get(f"/prices/{epic}/{resolution}/{num_points}")

    def get_prices_date_range(
        self, epic: str, resolution: str, start: str, end: str
    ) -> dict:
        """Get prices by date range."""
        return self.client.get(f"/prices/{epic}/{resolution}/{start}/{end}")

    def get_prices_query_range(
        self, epic: str, resolution: str, start: str, end: str
    ) -> dict:
        """Get prices by query range."""
        return self.client.get(
            f"/prices/{epic}/{resolution}",
            {"startdate": start, "enddate": end},
        )
