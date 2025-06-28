import pytest
from igapy.prices import Prices
from igapy.exceptions import IGAPIError
from conftest import DummyResponse


def test_get_prices_basic(dummy_client):
    """Test get_prices returns data."""
    data = {"prices": []}
    dummy_client.session._response = DummyResponse(200, data)
    api = Prices(dummy_client)
    assert api.get_prices("E") == data


def test_get_prices_with_params(dummy_client):
    """Test get_prices with params returns data."""
    data = {"prices": ["A"]}
    dummy_client.session._response = DummyResponse(200, data)
    api = Prices(dummy_client)
    res = api.get_prices(
        "E",
        resolution="HOUR",
        from_date="2025-01-01",
        to_date="2025-01-02",
        max_points=10,
        page_size=5,
        page_number=2,
    )
    assert res == data


def test_get_prices_num_points(dummy_client):
    """Test get_prices_num_points returns data."""
    data = {"prices": [1, 2, 3]}
    dummy_client.session._response = DummyResponse(200, data)
    api = Prices(dummy_client)
    assert api.get_prices_num_points("E", "MINUTE", 20) == data


def test_get_prices_date_range(dummy_client):
    """Test get_prices_date_range returns data."""
    data = {"prices": []}
    dummy_client.session._response = DummyResponse(200, data)
    api = Prices(dummy_client)
    assert (
        api.get_prices_date_range("E", "DAY", "2025-01-01", "2025-02-01")
        == data
    )


def test_get_prices_query_range(dummy_client):
    """Test get_prices_query_range returns data."""
    data = {"prices": []}
    dummy_client.session._response = DummyResponse(200, data)
    api = Prices(dummy_client)
    assert (
        api.get_prices_query_range("E", "DAY", "2025-01-01", "2025-02-01")
        == data
    )


def test_get_prices_error(dummy_client):
    """Test error in get_prices raises IGAPIError."""
    dummy_client.session._response = DummyResponse(
        404, {"errorCode": "NOT_FOUND", "errorDetails": "No data"}
    )
    api = Prices(dummy_client)
    with pytest.raises(IGAPIError):
        api.get_prices("E")
