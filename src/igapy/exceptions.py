class IGAPIError(Exception):
    """Generic IG API error."""


class ApiKeyMissingError(IGAPIError):
    """Raised when the API key is missing on login."""


class InsufficientFundsError(IGAPIError):
    """Raised when there are insufficient funds for an order."""


class MarketClosedError(IGAPIError):
    """Raised when the market is closed."""


class InvalidInputError(IGAPIError):
    """Raised when input parameters are invalid."""
