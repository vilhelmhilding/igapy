from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import IGClient


class SessionAPI:
    """Client for IG session endpoints."""

    def __init__(self, client: IGClient) -> None:
        """Initialize SessionAPI."""
        self.client = client

    def get_session_details(self, fetch_session_tokens: bool = False) -> dict:
        """Get session details."""
        params = {"fetchSessionTokens": str(fetch_session_tokens).lower()}
        return self.client.get("/session", params)

    def logout(self) -> dict:
        """Logout from session."""
        return self.client.delete("/session")

    def get_encryption_key(self) -> dict:
        """Get encryption key."""
        return self.client.get("/session/encryptionKey")

    def refresh_session(self, refresh_token: str) -> dict:
        """Refresh session."""
        return self.client.post(
            "/session/refresh-token", {"refresh_token": refresh_token}
        )

    def switch_account(
        self, account_id: str, default_account: bool = False
    ) -> dict:
        """Switch to another account."""
        data = {"accountId": account_id, "defaultAccount": default_account}
        return self.client.put("/session", data)
