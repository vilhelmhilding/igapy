import pytest
from igapy.client import IGClient
from igapy.exceptions import ApiKeyMissingError, IGAPIError
from conftest import DummyResponse


def test_login_success(dummy_client):
    """Test successful login and token storage."""
    dummy_client.session._response = DummyResponse(
        200,
        {"accountId": "ABC"},
        headers={"CST": "cst", "X-SECURITY-TOKEN": "token"},
    )
    result = dummy_client.login()
    assert result["accountId"] == "ABC"
    assert dummy_client.session.headers["CST"] == "cst"
    assert dummy_client.session.headers["X-SECURITY-TOKEN"] == "token"


def test_login_missing_key():
    """Test login raises if API key is missing."""
    client = IGClient("", "user", "pass", True)
    with pytest.raises(ApiKeyMissingError):
        client.login()


def test_handle_error_status(dummy_client):
    """Test error response raises IGAPIError."""
    dummy_client.session._response = DummyResponse(
        400, {"errorCode": "ERR", "errorDetails": "Bad"}
    )
    with pytest.raises(IGAPIError):
        dummy_client.get("/foo")
