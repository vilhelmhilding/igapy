import pytest
from igapy.watchlists import Watchlists
from igapy.exceptions import IGAPIError
from conftest import DummyResponse


def test_list_watchlists(dummy_client):
    """Test list_watchlists returns watchlists."""
    data = {"watchlists": []}
    dummy_client.session._response = DummyResponse(200, data)
    api = Watchlists(dummy_client)
    assert api.list_watchlists() == data


def test_create_watchlist(dummy_client):
    """Test create_watchlist returns new watchlist ID."""
    payload = {"name": "MyList"}
    data = {"watchlistId": "WL1"}
    dummy_client.session._response = DummyResponse(201, data)
    api = Watchlists(dummy_client)
    assert api.create_watchlist(payload) == data


def test_get_watchlist(dummy_client):
    """Test get_watchlist returns watchlist data."""
    data = {"watchlist": {}}
    dummy_client.session._response = DummyResponse(200, data)
    api = Watchlists(dummy_client)
    assert api.get_watchlist("WL1") == data


def test_delete_watchlist(dummy_client):
    """Test delete_watchlist returns deleted status."""
    data = {"status": "DELETED"}
    dummy_client.session._response = DummyResponse(200, data)
    api = Watchlists(dummy_client)
    assert api.delete_watchlist("WL1") == data


def test_add_market(dummy_client):
    """Test add_market returns added status."""
    data = {"status": "ADDED"}
    dummy_client.session._response = DummyResponse(200, data)
    api = Watchlists(dummy_client)
    assert api.add_market("WL1", "E") == data


def test_remove_market(dummy_client):
    """Test remove_market returns removed status."""
    data = {"status": "REMOVED"}
    dummy_client.session._response = DummyResponse(200, data)
    api = Watchlists(dummy_client)
    assert api.remove_market("WL1", "E") == data


def test_watchlists_error(dummy_client):
    """Test error in watchlists raises IGAPIError."""
    dummy_client.session._response = DummyResponse(
        400, {"errorCode": "ERR", "errorDetails": "Bad"}
    )
    api = Watchlists(dummy_client)
    with pytest.raises(IGAPIError):
        api.list_watchlists()
