import sys
import json
import pytest
from igapy import cli
from igapy.client import IGClient


@pytest.fixture(autouse=True)
def dummy_cli(monkeypatch):
    """Fixture for dummy CLI dependencies."""

    class DummyClient(IGClient):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.session = None

        def login(self):
            return {}

    monkeypatch.setattr(cli, "IGClient", DummyClient)

    class DummyAccounts:
        def __init__(self, client):
            pass

        def list_accounts(self):
            return {"accounts": [{"id": "A"}]}

    monkeypatch.setattr(cli, "Accounts", DummyAccounts)

    class DummyMarkets:
        def __init__(self, client):
            pass

        def get_market_details(self, epic):
            return {"market": {"epic": epic}}

    monkeypatch.setattr(cli, "Markets", DummyMarkets)

    class DummyOrders:
        def __init__(self, client):
            pass

        def create_otc_position(self, data):
            return {"dealReference": "D"}

    monkeypatch.setattr(cli, "Orders", DummyOrders)


def run_cli(args):
    """Helper to run CLI with given args."""
    old_argv = sys.argv
    sys.argv = ["igapy"] + args
    try:
        cli.main()
    finally:
        sys.argv = old_argv


def test_cli_list_accounts(capsys):
    """Test CLI list accounts command."""
    run_cli(
        [
            "--api-key",
            "k",
            "--username",
            "u",
            "--password",
            "p",
            "--demo",
            "accounts",
            "list",
        ]
    )
    out = json.loads(capsys.readouterr().out)
    assert out == {"accounts": [{"id": "A"}]}


def test_cli_get_market(capsys):
    """Test CLI get market command."""
    run_cli(
        [
            "--api-key",
            "k",
            "--username",
            "u",
            "--password",
            "p",
            "--demo",
            "markets",
            "get-details",
            "--epic",
            "E",
        ]
    )
    out = json.loads(capsys.readouterr().out)
    assert out == {"market": {"epic": "E"}}


def test_cli_place_order(capsys):
    """Test CLI place order command."""
    order_json = (
        '{"epic":"E","expiry":"DFB","direction":"BUY",'
        '"size":1,"orderType":"MARKET","currencyCode":"GBP"}'
    )
    run_cli(
        [
            "--api-key",
            "k",
            "--username",
            "u",
            "--password",
            "p",
            "--demo",
            "orders",
            "create",
            "--order",
            order_json,
        ]
    )
    out = json.loads(capsys.readouterr().out)
    assert out == {"dealReference": "D"}


def test_cli_help(capsys):
    run_cli(["--api-key", "k", "--username", "u", "--password", "p", "--demo"])
    captured = capsys.readouterr().out
    assert "usage:" in captured
