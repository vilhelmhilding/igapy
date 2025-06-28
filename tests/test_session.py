import pytest
from igapy.session import SessionAPI
from igapy.exceptions import IGAPIError
from conftest import DummyResponse


def test_get_session_details_success(dummy_client):
    """Test get_session_details returns accountId."""
    dummy_client.session._response = DummyResponse(200, {"accountId": "ABC"})
    api = SessionAPI(dummy_client)
    res = api.get_session_details(fetch_session_tokens=True)
    assert res["accountId"] == "ABC"


def test_logout_success(dummy_client):
    """Test logout returns success status."""
    dummy_client.session._response = DummyResponse(200, {"status": "SUCCESS"})
    api = SessionAPI(dummy_client)
    res = api.logout()
    assert res["status"] == "SUCCESS"


def test_get_encryption_key(dummy_client):
    """Test get_encryption_key returns key."""
    dummy_client.session._response = DummyResponse(
        200, {"encryptionKey": "key"}
    )
    api = SessionAPI(dummy_client)
    res = api.get_encryption_key()
    assert res["encryptionKey"] == "key"


def test_refresh_session(dummy_client):
    """Test refresh_session returns new token."""
    dummy_client.session._response = DummyResponse(200, {"token": "new-token"})
    api = SessionAPI(dummy_client)
    res = api.refresh_session("old-token")
    assert res["token"] == "new-token"


def test_switch_account(dummy_client):
    """Test switch_account returns new accountId."""
    dummy_client.session._response = DummyResponse(
        200, {"currentAccountId": "acc2"}
    )
    api = SessionAPI(dummy_client)
    res = api.switch_account("acc2", default_account=True)
    assert res["currentAccountId"] == "acc2"


def test_session_error_raises(dummy_client):
    """Test error in session raises IGAPIError."""
    dummy_client.session._response = DummyResponse(
        400, {"errorCode": "ERR", "errorDetails": "Bad"}
    )
    api = SessionAPI(dummy_client)
    with pytest.raises(IGAPIError):
        api.get_session_details()
