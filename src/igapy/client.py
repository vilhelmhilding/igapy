import requests
from .exceptions import ApiKeyMissingError, IGAPIError
from .utils import build_headers


class IGClient:
    """Authenticated IG REST API client."""

    def __init__(
        self, api_key: str, username: str, password: str, is_demo: bool = True
    ) -> None:
        """Initialize IGClient."""
        self.api_key = api_key
        self.username = username
        self.password = password
        self.is_demo = is_demo
        self.base_url = (
            "https://demo-api.ig.com/gateway/deal"
            if is_demo
            else "https://api.ig.com/gateway/deal"
        )
        self.session = requests.Session()

    def login(self) -> dict:
        """Authenticate and start session."""
        if not self.api_key:
            raise ApiKeyMissingError("API key is missing")
        url = f"{self.base_url}/session"
        headers = {
            "X-IG-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {"identifier": self.username, "password": self.password}
        resp = self.session.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            raise IGAPIError(f"Login failed: {resp.status_code}")
        cst = resp.headers.get("CST")
        token = resp.headers.get("X-SECURITY-TOKEN")
        if cst and token:
            self.session.headers.update(
                {"CST": cst, "X-SECURITY-TOKEN": token}
            )
        self.session_data = (
            resp.json()
        )  # Save full session response for streaming endpoint
        return self.session_data

    def get(self, path: str, params: dict = None) -> dict:
        """Send GET request."""
        url = self.base_url + path
        headers = build_headers(self)
        resp = self.session.get(url, params=params, headers=headers)
        return self._handle_response(resp)

    def post(self, path: str, data: dict) -> dict:
        """Send POST request."""
        url = self.base_url + path
        headers = build_headers(self)
        resp = self.session.post(url, json=data, headers=headers)
        return self._handle_response(resp)

    def put(self, path: str, data: dict) -> dict:
        """Send PUT request."""
        url = self.base_url + path
        headers = build_headers(self)
        resp = self.session.put(url, json=data, headers=headers)
        return self._handle_response(resp)

    def delete(self, path: str) -> dict:
        """Send DELETE request."""
        url = self.base_url + path
        headers = build_headers(self)
        resp = self.session.delete(url, headers=headers)
        return self._handle_response(resp)

    def _handle_response(self, resp) -> dict:
        """Handle API response."""
        if resp.status_code >= 400:
            raise IGAPIError(f"API error: {resp.status_code} {resp.text}")
        try:
            return resp.json()
        except ValueError:
            return {}
