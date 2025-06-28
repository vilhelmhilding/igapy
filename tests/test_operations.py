import pytest
from igapy.operations import Operations
from igapy.exceptions import IGAPIError
from conftest import DummyResponse


def test_list_applications(dummy_client):
    """Test list_applications returns applications."""
    data = {"applications": []}
    dummy_client.session._response = DummyResponse(200, data)
    api = Operations(dummy_client)
    assert api.list_applications() == data


def test_update_application(dummy_client):
    """Test update_application returns updated data."""
    data = {"status": "UPDATED"}
    dummy_client.session._response = DummyResponse(200, data)
    api = Operations(dummy_client)
    assert api.update_application({"setting": "val"}) == data


def test_disable_application(dummy_client):
    """Test disable_application returns disabled status."""
    data = {"status": "DISABLED"}
    dummy_client.session._response = DummyResponse(200, data)
    api = Operations(dummy_client)
    assert api.disable_application() == data


def test_operations_error(dummy_client):
    """Test error in operations raises IGAPIError."""
    dummy_client.session._response = DummyResponse(
        400, {"errorCode": "ERR", "errorDetails": "Bad"}
    )
    api = Operations(dummy_client)
    with pytest.raises(IGAPIError):
        api.list_applications()
