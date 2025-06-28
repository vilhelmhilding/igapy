from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .client import IGClient

from datetime import datetime


def parse_date(date_str: str) -> datetime:
    """Parse ISO 8601 date string."""
    return datetime.fromisoformat(date_str)


def build_headers(client: "IGClient") -> Dict[str, str]:
    """Build headers for API requests."""
    headers = {
        "X-IG-API-KEY": client.api_key,
        "Content-Type": "application/json",
    }
    if "CST" in client.session.headers:
        headers["CST"] = client.session.headers["CST"]
    if "X-SECURITY-TOKEN" in client.session.headers:
        headers["X-SECURITY-TOKEN"] = client.session.headers[
            "X-SECURITY-TOKEN"
        ]
    return headers
