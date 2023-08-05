import os
from json.decoder import JSONDecodeError
from typing import Optional, Type

import aiohttp
from aiohttp import ClientSession

from .constants import MSG_API_FAILED, MSG_BAD_CONNECTION, MSG_BAD_RESPONSE
from .exceptions import ClientConnectionError, ClientError, ClientResponseError
from .response import BaseAsyncResponse
from .validators import BaseValidator


class BaseAsyncClient:
    def __init__(
        self,
        api_url: Optional[str] = None,
        session: Optional[ClientSession] = None
    ):
        self.session: ClientSession = session
        self.api_url: str = api_url or os.getenv("SERVICE_API_URL")

    async def api_call(  # pylint: disable=too-many-arguments
        self,
        path: str,
        http_verb: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,  # skipcq: PYL-W0621
        headers: Optional[dict] = None,
        validator_class: Optional[Type[BaseValidator]] = BaseValidator,
        **kwargs
    ) -> BaseAsyncResponse:
        """Create a request and execute the API call to Slack.
        Args:
            path (str): The target API method.
                e.g. '/users/123'
            http_verb (str): HTTP Verb. e.g. 'POST'
            data: The body to attach to the request. If a dictionary is
                provided, form-encoding will take place.
                e.g. {'key1': 'value1', 'key2': 'value2'}
            params (dict): The URL parameters to append to the URL.
                e.g. {'key1': 'value1', 'key2': 'value2'}
            json (dict): JSON for the body to attach to the request
                (if files or data is not specified).
                e.g. {'key1': 'value1', 'key2': 'value2'}
            headers (dict): Additional request headers
        Returns:
            (BaseAsyncResponse)
                The server's response to an HTTP request. Data
                from the response can be accessed like a dict.
        Raises:
            ClientError: The request to the following API failed: http:://path/to/api
            ClientResponseError: Unsupported response body type
            ClientConnectionError: Could not connect to: http:://path/to/api
        """
        url = self.api_url + path
        request_args = {
            "method": http_verb,
            "url": url,
            "params": params,
            "data": data,
            "json": json,
            "headers": headers,
            **kwargs
        }
        use_current_session = self.session and not self.session.closed
        if use_current_session:
            response_dict = await self._request_with_session(session=self.session, **request_args)
        else:
            async with ClientSession() as session:
                response_dict = await self._request_with_session(session=session, **request_args)
        response = BaseAsyncResponse(
            api_url=url,
            http_verb=http_verb,
            req_args=request_args,
            **response_dict,
        )
        return validator_class(response).validate()

    async def _request_with_session(
        self,
        session: ClientSession,
        **request_args
    ):
        url = request_args.get("url")
        try:
            async with session.request(**request_args) as resp:
                try:
                    data = await resp.json()
                except (JSONDecodeError, aiohttp.ContentTypeError) as error:
                    data = await resp.text()
                response = {
                    "data": data,
                    "headers": resp.headers,
                    "status_code": resp.status,
                }
        except aiohttp.ClientConnectionError as error:
            raise ClientConnectionError(MSG_BAD_CONNECTION.format(url=url)) from error
        except aiohttp.ClientError as error:
            raise ClientError(MSG_API_FAILED.format(url=url)) from error
        return response
