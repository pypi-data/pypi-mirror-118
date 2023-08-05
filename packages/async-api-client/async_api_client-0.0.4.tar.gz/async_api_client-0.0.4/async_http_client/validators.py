from http import HTTPStatus
from typing import List

from .constants import MSG_API_FAILED
from .exceptions import ClientResponseError
from .response import BaseAsyncResponse


class BaseValidator:
    """Base class for response validators in async API clients."""
    accepted_status_codes: List[int] = [status.value for status in HTTPStatus if status.value < 400]

    def __init__(self, response: BaseAsyncResponse):
        self.response = response

    def raise_for_status(self):
        if self.response.status_code not in self.accepted_status_codes:
            raise ClientResponseError(message=MSG_API_FAILED.format(url=self.response.api_url), response=self.response)

    def validate(self):
        """Check if the response from API was successful.
        Returns:
            (BaseAsyncResponse)
                This method returns validated response object.
        Raises:
            ClientResponseError: Server responded with unexpected content.
        """
        self.raise_for_status()
        return self.response
