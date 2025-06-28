from igapy.accounts import Accounts
from conftest import DummyResponse


def test_list_accounts(dummy_client):
    """Test listing accounts returns accounts key."""
    dummy_client.session._response = DummyResponse(
        200, {"accounts": [{"id": "A"}]}
    )
    acc = Accounts(dummy_client).list_accounts()
    assert "accounts" in acc


def test_get_preferences(dummy_client):
    """Test getting account preferences returns trailingStopsEnabled."""
    dummy_client.session._response = DummyResponse(
        200, {"trailingStopsEnabled": True}
    )
    prefs = Accounts(dummy_client).get_preferences()
    assert prefs["trailingStopsEnabled"] is True


def test_update_preferences(dummy_client):
    """Test updating account preferences returns SUCCESS status."""
    dummy_client.session._response = DummyResponse(200, {"status": "SUCCESS"})
    res = Accounts(dummy_client).update_preferences(
        {"trailingStopsEnabled": False}
    )
    assert res["status"] == "SUCCESS"
