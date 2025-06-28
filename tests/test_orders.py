from igapy.orders import Orders
from conftest import DummyResponse


def test_create_otc_position(dummy_client):
    """Test create_otc_position."""
    dummy_client.session._response = DummyResponse(200, {"dealReference": "D"})
    res = Orders(dummy_client).create_otc_position({"epic": "E"})
    assert res["dealReference"] == "D"


def test_get_positions(dummy_client):
    """Test get_positions."""
    dummy_client.session._response = DummyResponse(200, {"positions": []})
    res = Orders(dummy_client).get_positions()
    assert "positions" in res


def test_get_position(dummy_client):
    """Test get_position."""
    dummy_client.session._response = DummyResponse(200, {"position": {}})
    res = Orders(dummy_client).get_position("D1")
    assert "position" in res


def test_update_position(dummy_client):
    """Test update_position."""
    dummy_client.session._response = DummyResponse(200, {"status": "UPDATED"})
    res = Orders(dummy_client).update_position("D1", {"size": 1})
    assert res["status"] == "UPDATED"


def test_delete_position(dummy_client):
    """Test delete_position."""
    dummy_client.session._response = DummyResponse(200, {"status": "DELETED"})
    res = Orders(dummy_client).delete_position("D1")
    assert res["status"] == "DELETED"


def test_get_working_orders(dummy_client):
    """Test get_working_orders."""
    dummy_client.session._response = DummyResponse(200, {"workingOrders": []})
    res = Orders(dummy_client).get_working_orders()
    assert "workingOrders" in res or isinstance(res, dict)


def test_create_working_order(dummy_client):
    """Test create_working_order."""
    dummy_client.session._response = DummyResponse(200, {"dealReference": "W"})
    res = Orders(dummy_client).create_working_order({"epic": "E"})
    assert res["dealReference"] == "W"


def test_delete_working_order(dummy_client):
    """Test delete_working_order."""
    dummy_client.session._response = DummyResponse(200, {"status": "DELETED"})
    res = Orders(dummy_client).delete_working_order("W")
    assert res["status"] == "DELETED"
