from igapy.utils import parse_date, build_headers
from datetime import datetime


def test_parse_date():
    """Test parse_date returns datetime object."""
    dt = parse_date("2025-06-23T15:30:00")
    assert isinstance(dt, datetime)
    assert dt.year == 2025


def test_build_headers(dummy_client):
    """Test build_headers returns correct headers."""
    dummy_client.session.headers.update({"CST": "c", "X-SECURITY-TOKEN": "t"})
    headers = build_headers(dummy_client)
    assert headers["X-IG-API-KEY"] == dummy_client.api_key
    assert headers["CST"] == "c"
    assert headers["X-SECURITY-TOKEN"] == "t"
