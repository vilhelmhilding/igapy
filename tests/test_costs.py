import pytest
from igapy.costs import CostsAndCharges
from igapy.exceptions import IGAPIError
from conftest import DummyResponse


def test_close_costs(dummy_client):
    """Test close_costs returns data."""
    data = {"quoteReference": "Q1"}
    dummy_client.session._response = DummyResponse(200, data)
    api = CostsAndCharges(dummy_client)
    assert api.close_costs({"param": "value"}) == data


def test_edit_costs(dummy_client):
    """Test edit_costs returns data."""
    data = {"quoteReference": "Q2"}
    dummy_client.session._response = DummyResponse(200, data)
    api = CostsAndCharges(dummy_client)
    assert api.edit_costs({"param": "value"}) == data


def test_download_pdf(dummy_client):
    """Test download_pdf returns PDF data."""
    data = {"pdf": "base64data"}
    dummy_client.session._response = DummyResponse(200, data)
    api = CostsAndCharges(dummy_client)
    assert api.download_pdf("Q1") == data


def test_history_costs(dummy_client):
    """Test history_costs returns history data."""
    data = {"history": []}
    dummy_client.session._response = DummyResponse(200, data)
    api = CostsAndCharges(dummy_client)
    assert api.history_costs("2025-01-01", "2025-02-01") == data


def test_costs_error(dummy_client):
    """Test error in costs raises IGAPIError."""
    dummy_client.session._response = DummyResponse(
        400, {"errorCode": "ERR", "errorDetails": "Bad"}
    )
    api = CostsAndCharges(dummy_client)
    with pytest.raises(IGAPIError):
        api.close_costs({})
