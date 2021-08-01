from requests import exceptions as requests_exceptions
from typing import Any

ERROR_STATUS_CODE = [
    status_code
    for status_code in range(400, 600)
    if status_code not in [400, 403, 404, 401, 413, 501]
]


def check_exception(exception):
    # type: (Any) -> bool

    return isinstance(exception, (requests_exceptions.ConnectionError,
                      requests_exceptions.Timeout)) \
        or exception.response is not None \
        and exception.response.status_code in ERROR_STATUS_CODE
