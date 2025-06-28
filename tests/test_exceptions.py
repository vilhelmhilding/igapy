import pytest
from igapy.exceptions import (
    IGAPIError,
    ApiKeyMissingError,
    InsufficientFundsError,
    MarketClosedError,
    InvalidInputError,
)


@pytest.mark.parametrize(
    "exc",
    [
        IGAPIError,
        ApiKeyMissingError,
        InsufficientFundsError,
        MarketClosedError,
        InvalidInputError,
    ],
)
def test_exceptions_inheritance(exc):
    """Test all custom exceptions inherit Exception."""
    assert issubclass(exc, Exception)
