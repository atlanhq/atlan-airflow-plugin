from airflow.configuration import conf  # type: ignore
from requests import exceptions as requests_exceptions
from typing import Dict, Any, List
import requests
import time

from airflow.utils.log.logging_mixin import LoggingMixin  # type: ignore
from atlan_airflow_plugin.lineage.backend import Backend
from atlan_airflow_plugin.utils import check_exception

logger = LoggingMixin().log

BULK_ENDPOINT = '/api/metadata/atlas/tenants/default/entity/bulk'


class AtlanBackend(Backend):

    @staticmethod
    def send_lineage(
        operator,
        inlets,
        outlets,
        context,
    ):

        # type: (object, list, list, dict) -> None

        (inlet_list, outlet_list, atlan_process) = \
            Backend.create_lineage_meta(operator, inlets, outlets,
                                        context)

        try:
            _send_bulk(data=atlan_process)
        except Exception as e:
            logger.info('Failed to create lineage assets. Error: {}'.format(e))


def _send_bulk(data):

    # type: (List[Dict[Any, Any]]) -> None

    retry_limit = 5
    retry_delay = 10

    try:
        _url = conf.get('atlan', 'url')
        _token = conf.get('atlan', 'token')
    except Exception:
        _url = ''
        _token = ''

    _headers = {'APIKEY': _token, 'Content-Type': 'application/json'}

    bulk_url = _url + BULK_ENDPOINT

    request_body = {'entities': data}

    req_attempt = 1
    while True:
        try:
            response = requests.request(method='POST', url=bulk_url, json=request_body, headers=_headers)
            response.raise_for_status()
            return
        except requests_exceptions.RequestException as e:
            if not check_exception(e):
                raise Exception(
                    'Failed to call Atlan API. Response: {}, Status Code: {}'.format(
                        e.response.content, e.response.status_code))

            logger.error(
                'Unable to connect to Atlan. Attempt: {attempts} Error: {error}, retrying....'.format(
                    attempts=req_attempt, error=e))

        if req_attempt == retry_limit:
            raise Exception('Unable to send API Request to Atlan. Tried {attempts} times'.format(attempts=req_attempt))

        req_attempt += 1
        time.sleep(retry_delay)

    if response is not None and not response.ok:
        logger.error('Unable to create lineage. Response: {resp}'.format(resp=response.text))
