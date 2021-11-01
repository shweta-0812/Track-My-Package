import asyncio
from typing import Any, Union

from httpx import AsyncClient
from httpx._types import AuthTypes, QueryParamTypes, HeaderTypes, CookieTypes
from six.moves import urllib

URLTypes = Union[str]


class HTTPClient:
    def __init__(self, host: str, port: str = None, scheme: str = "http"):
        self.host = host
        self.port = port
        self.scheme = scheme
        self._port_string = f":{self.port}" if port else ""
        self.base_url = f"{self.scheme}://{self.host}{self._port_string}"
        self._session = None
        self._loop = asyncio.get_event_loop()

    def url(self, path: str, params: Any = None) -> Any:
        url = self.base_url + urllib.parse.quote(path, safe="/:")
        if params:
            url = "%s?%s" % (url, urllib.parse.urlencode(params))
        return url

    async def get(
        self,
        path: str,
        params: QueryParamTypes = None,
        cookies: CookieTypes = None,
        auth: AuthTypes = None,
        headers: HeaderTypes = None,
    ) -> Any:
        url = self.url(path, params)
        async with AsyncClient() as ac:
            return await ac.get(url=url, params=params, headers=headers, cookies=cookies, auth=auth)

    async def post(
        self,
        path: str,
        params: QueryParamTypes = None,
        json: Any = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: AuthTypes = None,
    ) -> Any:
        url = self.url(path, params)
        async with AsyncClient() as ac:
            return await ac.post(url=url, params=params, headers=headers, cookies=cookies, json=json, auth=auth)
