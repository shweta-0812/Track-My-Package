import datetime
import time
from typing import Any
from urllib.parse import urlencode

from common.app_settings import app_settings


def date_to_datetime(dt):
    return datetime.datetime.combine(dt, datetime.datetime.min.time())


def get_current_timestamp():
    return int(time.time())

def get_absolute_url(
    path: str,
    index_view: bool = True,
    params: Any = None,
) -> str:
    if not path:
        return path

    path = path.strip()
    if not path:
        return path
    path = path[1:] if path[0] == "/" else path  # removing extra slash if present
    domain = app_settings.APP_SERVER_URL
    if not app_settings.IS_PRODUCTION:
        domain = "http://localhost:8000"

    url = "{domain}/{hash}{path}".format(domain=domain, path=path, hash="#/" if index_view else "")

    if params:
        param_string = urlencode(params)
        url = "{}?{}".format(url, param_string)

    return url
