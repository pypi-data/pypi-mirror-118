from .constants import MSG_OPERATION_TYPE_ERROR


class BaseAsyncResponse:
    def __init__(
        self,
        *,
        http_verb: str,
        api_url: str,
        req_args: dict,
        data: dict,
        headers: dict,
        status_code: int,
    ):
        self.http_verb = http_verb
        self.api_url = api_url
        self.req_args = req_args
        self.data = data
        self.headers = headers
        self.status_code = status_code

    def __str__(self):
        """Return the Response data if object is converted to a string."""
        return f"{self.status_code} {self.data}"

    def __getitem__(self, key):
        """Retrieves any key from the data store.
        Note:
            This is implemented so users can reference the
            AsyncResponse object like a dictionary.
            e.g. response["ok"]
        Returns:
            The value from data or None.
        """
        if not isinstance(self.data, dict):
            raise TypeError(MSG_OPERATION_TYPE_ERROR.format(type_name=type(self.data)))
        return self.data.get(key, None)

    def get(self, key, default=None):
        """Retrieves any key from the response data.
        Note:
            This is implemented so users can reference the
            AsyncResponse object like a dictionary.
            e.g. response.get("ok", False)
        Returns:
            The value from data or the specified default.
        """
        if not isinstance(self.data, dict):
            raise TypeError(MSG_OPERATION_TYPE_ERROR.format(type_name=type(self.data)))
        return self.data.get(key, default)
