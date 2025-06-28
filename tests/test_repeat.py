from igapy.repeat import RepeatDealWindow
from conftest import DummyResponse


def test_get_repeat_deal_window(dummy_client):
    """Test get_repeat_deal_window returns deal window."""
    expected = {"dealWindow": []}
    dummy_client.session._response = DummyResponse(200, expected)
    api = RepeatDealWindow(dummy_client)
    assert api.get_repeat_deal_window() == expected
