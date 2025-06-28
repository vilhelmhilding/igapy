from igapy.markets import Markets
from conftest import DummyResponse


def test_search_markets(dummy_client):
    """Test search_markets returns markets."""
    dummy_client.session._response = DummyResponse(
        200, {"markets": [{"epic": "E"}]}
    )
    result = Markets(dummy_client).search_markets("foo")
    assert "markets" in result


def test_get_market_details(dummy_client):
    """Test get_market_details returns correct epic."""
    dummy_client.session._response = DummyResponse(
        200, {"market": {"epic": "E"}}
    )
    result = Markets(dummy_client).get_market_details("E")
    assert result["market"]["epic"] == "E"


def test_get_markets_bulk(dummy_client):
    """Test get_markets returns list of markets."""
    dummy_client.session._response = DummyResponse(200, {"markets": []})
    result = Markets(dummy_client).get_markets(["E1", "E2"])
    assert isinstance(result["markets"], list)


def test_market_navigation(dummy_client):
    """Test get_market_navigation and get_market_sub_nodes."""
    dummy_client.session._response = DummyResponse(200, {"nodes": []})
    nav = Markets(dummy_client).get_market_navigation()
    assert "nodes" in nav
    sub = Markets(dummy_client).get_market_sub_nodes("N")
    assert isinstance(sub, dict)
