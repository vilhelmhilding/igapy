import pytest
from igapy.client import IGClient


class DummyResponse:
    """A dummy response object for simulating HTTP responses."""

    def __init__(self, status_code=200, json_data=None, headers=None, text=""):
        self.status_code = status_code
        self._json = json_data or {}
        self.headers = headers or {}
        self.text = text

    def json(self):
        """Return the dummy JSON data."""
        return self._json


class DummySession:
    """A dummy session object for simulating requests.Session."""

    def __init__(self):
        self._response = DummyResponse()
        self.headers = {}

    def get(self, url, params=None, headers=None):
        """Simulate a GET request."""
        return self._response

    def post(self, url, json=None, headers=None):
        """Simulate a POST request."""
        return self._response

    def put(self, url, json=None, headers=None):
        """Simulate a PUT request."""
        return self._response

    def delete(self, url, headers=None):
        """Simulate a DELETE request."""
        return self._response


@pytest.fixture
def dummy_client():
    """Fixture providing a dummy IGClient with a dummy session for testing."""
    client = IGClient("key", "user", "pass", is_demo=True)
    client.session = DummySession()
    return client
