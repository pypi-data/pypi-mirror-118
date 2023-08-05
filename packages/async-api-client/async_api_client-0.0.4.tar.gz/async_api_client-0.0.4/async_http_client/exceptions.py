class ClientError(Exception):
    """Base class for all microservices API clients."""


class ClientConnectionError(ClientError):
    """Base class for errors related to connection. Raised when request could not be completed."""


class ClientResponseError(ClientError):
    """Base class for errors related to response content. Raised on response validation."""
    def __init__(self, message: str, response):
        msg = f"{message}\nThe server responded with: {response}"
        self.response = response
        super().__init__(msg)
