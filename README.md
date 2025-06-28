# igapy – IG API Wrapper

<!-- [![Downloads](https://static.pepy.tech/badge/igapy)](https://pepy.tech/project/igapy) -->
[![PyPI version](https://img.shields.io/pypi/v/igapy.svg)](https://pypi.org/project/igapy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/igapy.svg)](https://pypi.org/project/igapy)
[![CI](https://github.com/vilhelmhilding/igapy/actions/workflows/python-ci.yml/badge.svg)](https://github.com/vilhelmhilding/igapy/actions)
[![codecov](https://codecov.io/gh/vilhelmhilding/igapy/branch/main/graph/badge.svg)](https://codecov.io/gh/vilhelmhilding/igapy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A complete, modern, production-ready Python wrapper for the IG REST and streaming API.

---

## Why igapy?

**igapy** is an unofficial, open source Python client for IG's REST and streaming API. It is designed for quant developers, algo traders, and anyone who wants a robust, well-documented and production-ready interface to IG's trading platform. The project aims to be a reference implementation for clean API wrappers in Python.

- 100% endpoint coverage (REST & streaming)
- Modern, type-annotated, PEP8/Black-formatted codebase
- CLI for all public API endpoints
- Full test suite and CI/CD
- No unnecessary complexity – easy to read, extend, and audit

---

## Features

- Full REST API coverage (session, accounts, markets, orders, prices, watchlists, sentiment, history, costs, operations)
- WebSocket streaming client with reconnect, ping, custom subscription management
- Authentication (session management, token handling, account switching, encryption keys)
- Market data retrieval (search, details, bulk, navigation)
- Order management (positions, working orders, confirmations)
- Client sentiment access (single, related, batch)
- Historical prices (multiple date/resolution variants)
- Account preferences management
- Watchlist management (create, modify, delete, add/remove markets)
- Command-line interface (CLI)
- GitHub Actions CI workflow
- Unit tests with pytest (90 tests, 100% coverage)
- PEP8-compliant, Black-formatted codebase

---

## Quickstart

### Install

```bash
pip install igapy
```

### Python Example

```python
from igapy import IGClient, Accounts, Markets

client = IGClient(
    api_key="YOUR_API_KEY",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    is_demo=True
)
client.login()

accounts = Accounts(client).list_accounts()
print(accounts)

# Search for Apple stock (AAPL)
apple_search = Markets(client).search_markets("APPLE")
print(apple_search)

# Get details for the first Apple market found (if any)
if apple_search and apple_search["markets"]:
    apple_epic = apple_search["markets"][0]["epic"]
    apple_details = Markets(client).get_market_details(apple_epic)
    print(apple_details)
```

### CLI Example

```bash
# List accounts
igapy accounts list --api-key KEY --username USER --password PASS --demo

# Get market details
igapy markets get-details --api-key KEY --username USER --password PASS --demo --epic IX.D.FTSE.DAILY.IP

# Create order
igapy orders create --api-key KEY --username USER --password PASS --demo --order '{"epic":"IX.D.FTSE.DAILY.IP","expiry":"DFB","direction":"BUY","size":1,"orderType":"MARKET","currencyCode":"GBP"}'

# Get prices
igapy prices get --api-key KEY --username USER --password PASS --demo --epic IX.D.FTSE.DAILY.IP

# Get transactions for type and period
igapy history transactions-period --api-key KEY --username USER --password PASS --demo --transaction-type ALL --last-period MONTH

# Get cost history
igapy costs history --api-key KEY --username USER --password PASS --demo --from-date 2024-01-01 --to-date 2024-06-01
```

### Streaming Example

```python
from igapy import IGClient, IGStreamingClient
import time

client = IGClient(
    api_key="YOUR_API_KEY",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    is_demo=False
)
client.login()

def on_chart_tick(data):
    print("Chart tick update:", data)

# IGStreamingClient supports automatic reconnect and re-subscription on connection loss.
# You can control this with the 'reconnect' and 'reconnect_delay' parameters.
stream = IGStreamingClient(client, reconnect=True, reconnect_delay=5)
stream.start()
stream.subscribe_chart_tick(
    epic = "CS.D.BITCOIN.CFD.IP",
    fields=["BID", "OFR", "UTM"],
    callback=on_chart_tick
)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping streaming...")
    stream.stop()
```

---

## API Documentation

- [IG REST API Reference](https://labs.ig.com/rest-trading-api-reference.html)

---

## Development & Contribution

- Clone repo, create a virtualenv, install with `pip install -e .[dev]`
- Run tests: `pytest`
- Lint: `flake8 src/igapy tests`
- Format: `black src/igapy tests`

Pull requests and issues are welcome!

---

## Project Structure

```
.
├── LICENSE
├── pyproject.toml
├── MANIFEST.in
├── README.md
├── .gitignore
├── .github/
│   └── workflows/
│       └── python-ci.yml
├── src/
│   └── igapy/
│       ├── __init__.py
│       ├── cli.py
│       ├── client.py
│       ├── session.py
│       ├── accounts.py
│       ├── markets.py
│       ├── prices.py
│       ├── orders.py
│       ├── sentiment.py
│       ├── history.py
│       ├── repeat.py
│       ├── watchlists.py
│       ├── costs.py
│       ├── operations.py
│       ├── streaming.py
│       ├── exceptions.py
│       └── utils.py
└── tests/
    ├── conftest.py
    ├── test_accounts.py
    ├── test_cli.py
    ├── test_client.py
    ├── test_costs.py
    ├── test_exceptions.py
    ├── test_history.py
    ├── test_markets.py
    ├── test_operations.py
    ├── test_orders.py
    ├── test_prices.py
    ├── test_repeat.py
    ├── test_sentiment.py
    ├── test_session.py
    ├── test_streaming.py
    ├── test_utils.py
    └── test_watchlists.py
```

---

## Code Style

- PEP8 via flake8
- Black formatting
- Type annotations and docstrings for all public classes/methods

---

## Continuous Integration

- GitHub Actions: `.github/workflows/python-ci.yml`
- Coverage via pytest-cov

---

## License

MIT License – see [LICENSE](LICENSE) file for details.

---

## Contact

hi@vilhelmhilding.com

---

*This project is not affiliated with or endorsed by IG Group. Use at your own risk.*
