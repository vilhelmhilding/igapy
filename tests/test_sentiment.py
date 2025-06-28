from igapy.sentiment import Sentiment
from conftest import DummyResponse


def test_list_client_sentiment(dummy_client):
    """Test list_client_sentiment returns sentiment data."""
    dummy_client.session._response = DummyResponse(
        200, {"clientSentiment": []}
    )
    res = Sentiment(dummy_client).list_client_sentiment(["E"])
    assert "clientSentiment" in res


def test_get_client_sentiment(dummy_client):
    """Test get_client_sentiment returns sentiment data."""
    dummy_client.session._response = DummyResponse(200, {"sentiment": {}})
    res = Sentiment(dummy_client).get_client_sentiment("E")
    assert "sentiment" in res or isinstance(res, dict)


def test_get_related_sentiment(dummy_client):
    """Test get_related_sentiment returns related data."""
    dummy_client.session._response = DummyResponse(200, {"related": []})
    res = Sentiment(dummy_client).get_related_sentiment("E")
    assert isinstance(res, dict)
