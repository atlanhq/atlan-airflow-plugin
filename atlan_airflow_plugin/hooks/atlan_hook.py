from typing import Optional, Dict, Any, Union, Tuple
from requests import Response
import requests
import time

from requests import exceptions as requests_exceptions
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from atlan_airflow_plugin.utils import check_exception


class AtlanHook(BaseHook):

    ALLOWED_METHOD = ["GET", "POST"]

    def __init__(
        self,
        atlan_conn_id: str = "atlan_default",
        retry_limit: int = 3,
        retry_delay: int = 5,
        timeout: int = 30,
    ):

        self.atlan_conn_id = atlan_conn_id
        self.atlan_conn = self.get_connection(atlan_conn_id)
        self.timeout = timeout
        if retry_limit < 1:
            raise ValueError("Retry limit needs to be more than or equal to 1")
        self.retry_limit = retry_limit
        self.retry_delay = retry_delay

    def call_api(self, request_info, payload=None):

        # type: (Tuple[str, str], Optional[Dict[str, Any]]) -> Union[Response, None]

        """
        Wrapper on top of Python requests client. It implements different auth methods.
        This wrapper also handles retries for failed requests.
        :param request_info: Tuple of HTTP method and endpoint
        :type request_info: tuple[string, string]
        :param payload: JSON for request.
        :type payload: dict
        :return: If the api call returns a OK status code,
            this function returns the response in JSON. Otherwise,
            we throw an AirflowException.
        """
        method, endpoint = request_info

        api_key = self.atlan_conn.password
        url = self.atlan_conn.host + endpoint
        headers = {"APIKEY": api_key}

        if method not in self.ALLOWED_METHOD:
            raise AirflowException("HTTP Method not allowed")

        req_attempt = 1
        while True:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response
            except requests_exceptions.RequestException as e:
                if not check_exception(e):
                    raise AirflowException(
                        "Failed to call Atlan API. Response: {}, Status Code: {}".format(
                            e.response.content, e.response.status_code
                        )
                    )

                self._logger(
                    "error",
                    "Unable to connect to Atlan. Attempt: {} Error: {}, retrying....".format(
                        req_attempt, e
                    ),
                )

            if req_attempt == self.retry_limit:
                raise AirflowException(
                    "Unable to send API Request to Atlan. Tried {attempts} times".format(
                        attempts=req_attempt
                    )
                )

            req_attempt += 1
            time.sleep(self.retry_delay)

    def _logger(self, level, error):
        # type: (str, str) -> None

        if level == "info":
            logger = self.log.info
        elif level == "warn":
            logger = self.log.warn
        elif level == "error":
            logger = self.log.error
        else:
            raise AirflowException("Unexpected logging level.")

        logger(error)
