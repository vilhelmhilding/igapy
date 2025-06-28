from igapy.history import History
from conftest import DummyResponse


def test_get_activity(dummy_client):
    """Test get_activity returns activities."""
    dummy_client.session._response = DummyResponse(200, {"activities": []})
    res = History(dummy_client).get_activity()
    assert "activities" in res


def test_get_activity_by_period(dummy_client):
    """Test get_activity_by_period returns activities."""
    dummy_client.session._response = DummyResponse(200, {"activities": []})
    res = History(dummy_client).get_activity_by_period("WEEK_1")
    assert "activities" in res


def test_get_activity_by_date_range(dummy_client):
    """Test get_activity_by_date_range returns activities."""
    dummy_client.session._response = DummyResponse(200, {"activities": []})
    res = History(dummy_client).get_activity_by_date_range(
        "2025-01-01", "2025-01-31"
    )
    assert "activities" in res


def test_get_transactions(dummy_client):
    """Test get_transactions returns transactions."""
    dummy_client.session._response = DummyResponse(200, {"transactions": []})
    res = History(dummy_client).get_transactions()
    assert "transactions" in res


def test_get_transactions_by_period(dummy_client):
    """Test get_transactions_by_period returns transactions."""
    dummy_client.session._response = DummyResponse(200, {"transactions": []})
    res = History(dummy_client).get_transactions_by_period("MONTH_1")
    assert "transactions" in res


def test_get_transactions_by_date_range(dummy_client):
    """Test get_transactions_by_date_range returns transactions."""
    dummy_client.session._response = DummyResponse(200, {"transactions": []})
    res = History(dummy_client).get_transactions_by_date_range(
        "2025-01-01", "2025-01-31"
    )
    assert "transactions" in res


def test_get_transactions_by_type_and_period(dummy_client):
    """Test get_transactions_by_type_and_period returns transactions."""
    dummy_client.session._response = DummyResponse(200, {"transactions": []})
    res = History(dummy_client).get_transactions_by_type_and_period(
        "ALL", "MONTH_1"
    )
    assert "transactions" in res


def test_get_transactions_by_type_and_date_range(dummy_client):
    """Test get_transactions_by_type_and_date_range returns transactions."""
    dummy_client.session._response = DummyResponse(200, {"transactions": []})
    res = History(dummy_client).get_transactions_by_type_and_date_range(
        "ALL", "2025-01-01", "2025-01-31"
    )
    assert "transactions" in res
