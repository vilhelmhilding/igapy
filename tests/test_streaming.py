import pytest
from igapy.streaming import IGStreamingClient
from types import SimpleNamespace


class DummyLSClient:
    def __init__(self, endpoint, user):
        self.endpoint = endpoint
        self.user = user
        self.connectionDetails = DummyConnDetails()
        self.connected = False
        self.subscribed = []
        self.unsubscribed = []
        self.disconnected = False
        self.listeners = []

    def connect(self):
        self.connected = True

    def subscribe(self, sub):
        self.subscribed.append(sub)

    def unsubscribe(self, sub):
        self.unsubscribed.append(sub)

    def disconnect(self):
        self.disconnected = True

    def addListener(self, listener):
        self.listeners.append(listener)


class DummyConnDetails:
    def set_password(self, pw):
        self.pw = pw

    def setPassword(self, pw):
        self.set_password(pw)

    def setAdapterSet(self, adapter_set):
        self.adapter_set = adapter_set


class DummySubscription:
    def __init__(self, mode, items, fields):
        self.mode = mode
        self.items = items
        self.fields = fields
        self.listeners = []
        self.adapter = None

    def addListener(self, cb):
        self.listeners.append(cb)

    def setDataAdapter(self, adapter):
        self.adapter = adapter

    def trigger(self, data):
        for cb in self.listeners:
            # If cb is a class with onItemUpdate, call that method
            if hasattr(cb, "onItemUpdate"):
                cb.onItemUpdate(DummyItemUpdate(self.fields, data))
            else:
                cb(DummyItemUpdate(self.fields, data))


class DummyItemUpdate:
    def __init__(self, fields, data):
        self._fields = fields
        self._data = data

    def getValue(self, field):
        return self._data.get(field)


@pytest.fixture(autouse=True)
def patch_ls(monkeypatch):
    monkeypatch.setattr("igapy.streaming.LightstreamerClient", DummyLSClient)
    monkeypatch.setattr("igapy.streaming.Subscription", DummySubscription)


@pytest.fixture
def dummy_client():
    client = SimpleNamespace()
    client.session = SimpleNamespace()
    client.session.headers = {
        "CST": "dummycst",
        "X-SECURITY-TOKEN": "dummytoken",
    }
    client.session_data = {
        "currentAccountId": "dummyId",
        "lightstreamerEndpoint": "https://dummy.lightstreamer.endpoint",
    }
    return client


def test_start_and_stop(dummy_client):
    """Test start and stop connect/disconnect Lightstreamer."""
    s = IGStreamingClient(dummy_client)
    s.start()
    assert s._ls_client.connected
    s.stop()
    assert s._ls_client.disconnected


def test_subscribe_price(dummy_client):
    """Test price subscription and callback."""
    s = IGStreamingClient(dummy_client)
    s.start()
    received = []
    s.subscribe_price("EPIC", ["BID", "OFFER"], lambda d: received.append(d))
    account_id = dummy_client.session_data["currentAccountId"]
    sub = s._subscriptions[f"PRICE:{account_id}:EPIC"]
    sub.trigger({"BID": "1.1", "OFFER": "2.2"})
    assert received[0]["BID"] == "1.1"
    assert received[0]["OFFER"] == "2.2"


def test_subscribe_account(dummy_client):
    """Test account subscription and callback."""
    s = IGStreamingClient(dummy_client)
    s.start()
    received = []
    s.subscribe_account(["PNL"], lambda d: received.append(d))
    account_id = dummy_client.session_data["currentAccountId"]
    sub = s._subscriptions[f"ACCOUNT:{account_id}"]
    sub.trigger({"PNL": "100"})
    assert received[0]["PNL"] == "100"


def test_subscribe_trade(dummy_client):
    """Test trade subscription and callback."""
    s = IGStreamingClient(dummy_client)
    s.start()
    received = []
    s.subscribe_trade(["CONFIRMS"], lambda d: received.append(d))
    account_id = dummy_client.session_data["currentAccountId"]
    sub = s._subscriptions[f"TRADE:{account_id}"]
    sub.trigger({"CONFIRMS": "OK"})
    assert received[0]["CONFIRMS"] == "OK"


def test_subscribe_chart_tick(dummy_client):
    """Test chart tick subscription and callback."""
    s = IGStreamingClient(dummy_client)
    s.start()
    received = []
    s.subscribe_chart_tick("EPIC", ["BID"], lambda d: received.append(d))
    sub = s._subscriptions["CHART:EPIC:TICK"]
    sub.trigger({"BID": "1.5"})
    assert received[0]["BID"] == "1.5"


def test_subscribe_chart_candle(dummy_client):
    """Test chart candle subscription and callback."""
    s = IGStreamingClient(dummy_client)
    s.start()
    received = []
    s.subscribe_chart_candle(
        "EPIC", "1MINUTE", ["BID_OPEN"], lambda d: received.append(d)
    )
    sub = s._subscriptions["CHART:EPIC:1MINUTE"]
    sub.trigger({"BID_OPEN": "1.7"})
    assert received[0]["BID_OPEN"] == "1.7"


def test_unsubscribe(dummy_client):
    """Test unsubscribe."""
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_price("EPIC", ["BID"], lambda d: None)
    account_id = dummy_client.session_data["currentAccountId"]
    item = f"PRICE:{account_id}:EPIC"
    s.unsubscribe(item)
    assert item not in s._subscriptions
    assert (
        s._ls_client.unsubscribed
    )  # Should contain the DummySubscription instance


def test_reconnect_and_resubscribe(dummy_client, capsys):
    """Test that reconnect triggers and subscriptions are re-added."""
    s = IGStreamingClient(dummy_client, reconnect=True, reconnect_delay=0)
    s.start()
    received = []
    s.subscribe_price("EPIC", ["BID"], lambda d: received.append(d))
    account_id = dummy_client.session_data["currentAccountId"]
    item = f"PRICE:{account_id}:EPIC"
    # Simulate disconnect event
    for listener in s._ls_client.listeners:
        if hasattr(listener, "onStatusChange"):
            listener.onStatusChange("DISCONNECTED")
    # After reconnect, subscription should still exist
    assert item in s._subscriptions
    # Simulate update after reconnect
    sub = s._subscriptions[item]
    sub.trigger({"BID": "2.2"})
    assert received[-1]["BID"] == "2.2"
    out = capsys.readouterr().out
    assert "Reconnected and re-subscribed" in out


def test_callback_exception_handling(dummy_client, capsys):
    """Test that exception in callback does not crash and is logged."""
    s = IGStreamingClient(dummy_client)
    s.start()

    def bad_callback(data):
        raise ValueError("fail!")

    s.subscribe_price("EPIC", ["BID"], bad_callback)
    account_id = dummy_client.session_data["currentAccountId"]
    sub = s._subscriptions[f"PRICE:{account_id}:EPIC"]
    sub.trigger({"BID": "1.1"})
    out = capsys.readouterr().out
    assert "Exception in onItemUpdate callback" in out


def test_on_subscription_error_and_unsubscription(dummy_client, capsys):
    """Test that onSubscriptionError and onUnsubscription are logged."""
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_price("EPIC", ["BID"], lambda d: None)
    account_id = dummy_client.session_data["currentAccountId"]
    sub = s._subscriptions[f"PRICE:{account_id}:EPIC"]
    # Simulate error
    for cb in sub.listeners:
        if hasattr(cb, "onSubscriptionError"):
            cb.onSubscriptionError("404", "Not found")
        if hasattr(cb, "onUnsubscription"):
            cb.onUnsubscription()
    out = capsys.readouterr().out
    assert "Error for" in out
    assert "Unsubscribed from" in out


def test_on_server_error(dummy_client, capsys):
    """Test that onServerError is logged."""
    s = IGStreamingClient(dummy_client)
    s.start()
    # Trigga onServerError via listener
    for listener in s._ls_client.listeners:
        if hasattr(listener, "onServerError"):
            listener.onServerError("500", "Server fail!")
    out = capsys.readouterr().out
    assert "Server error" in out


def test_unsubscribe_price(dummy_client):
    """Test unsubscribe_price removes sub and calls unsubscribe."""
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_price("EPIC", ["BID"], lambda d: None)
    account_id = dummy_client.session_data["currentAccountId"]
    s.unsubscribe_price("EPIC")
    assert f"PRICE:{account_id}:EPIC" not in s._subscriptions
    assert s._ls_client.unsubscribed


def test_unsubscribe_account(dummy_client):
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_account(["PNL"], lambda d: None)
    s.unsubscribe_account()
    assert (
        f"ACCOUNT:{dummy_client.session_data['currentAccountId']}"
        not in s._subscriptions
    )
    assert s._ls_client.unsubscribed


def test_unsubscribe_trade(dummy_client):
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_trade(["CONFIRMS"], lambda d: None)
    s.unsubscribe_trade()
    assert (
        f"TRADE:{dummy_client.session_data['currentAccountId']}"
        not in s._subscriptions
    )
    assert s._ls_client.unsubscribed


def test_unsubscribe_chart_tick(dummy_client):
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_chart_tick("EPIC", ["BID"], lambda d: None)
    s.unsubscribe_chart_tick("EPIC")
    assert "CHART:EPIC:TICK" not in s._subscriptions
    assert s._ls_client.unsubscribed


def test_unsubscribe_chart_candle(dummy_client):
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_chart_candle("EPIC", "1MIN", ["BID"], lambda d: None)
    s.unsubscribe_chart_candle("EPIC", "1MIN")
    assert "CHART:EPIC:1MIN" not in s._subscriptions
    assert s._ls_client.unsubscribed


def test_missing_tokens_raises():
    """Test that missing CST/XST raises RuntimeError."""
    from igapy.streaming import IGStreamingClient

    client = SimpleNamespace()
    client.session = SimpleNamespace()
    client.session.headers = {}
    client.session_data = {
        "currentAccountId": "dummyId",
        "lightstreamerEndpoint": "https://dummy.lightstreamer.endpoint",
    }
    s = IGStreamingClient(client)
    import pytest

    with pytest.raises(RuntimeError):
        s.start()


def test_print_endpoint(dummy_client, capsys):
    """Test that endpoint print in start() täcks."""
    s = IGStreamingClient(dummy_client)
    s.start()
    out = capsys.readouterr().out
    assert "Using Lightstreamer endpoint" in out


def test_on_subscription_print(dummy_client, capsys):
    """Test att onSubscription print täcks."""
    s = IGStreamingClient(dummy_client)
    s.start()
    s.subscribe_price("EPIC", ["BID"], lambda d: None)
    account_id = dummy_client.session_data["currentAccountId"]
    sub = s._subscriptions[f"PRICE:{account_id}:EPIC"]
    # Trigga onSubscription
    for cb in sub.listeners:
        if hasattr(cb, "onSubscription"):
            cb.onSubscription()
    out = capsys.readouterr().out
    assert "Subscribed to" in out


def test_reconnect_print(dummy_client, capsys):
    """Test att reconnect print täcks."""
    s = IGStreamingClient(dummy_client, reconnect=True, reconnect_delay=0)
    s.start()
    s.subscribe_price("EPIC", ["BID"], lambda d: None)
    # Tvinga reconnect
    s._reconnect_subscriptions()
    out = capsys.readouterr().out
    assert "Reconnected and re-subscribed" in out


def test_dummy_subscription_direct_function_callback():
    received = []

    def direct_callback(update):
        received.append(update)

    sub = DummySubscription("MERGE", ["FIELD1"], ["FIELD1"])
    sub.listeners = [direct_callback]  # Bypass addListener
    sub.trigger({"FIELD1": "123"})

    assert isinstance(received[0], DummyItemUpdate)
    assert received[0].getValue("FIELD1") == "123"
