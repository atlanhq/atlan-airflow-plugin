from airflow.configuration import conf  # type: ignore
import requests
import json

from airflow.configuration import conf  # type: ignore
from airflow.utils.log.logging_mixin import LoggingMixin  # type: ignore
from atlan_airflow_plugin.lineage.backend import Backend

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

    try:
        _url = conf.get('atlan', 'url')
        _token = conf.get('atlan', 'token')
    except Exception:
        _url = ''
        _token = ''

    _headers = {'APIKEY': _token, 'Content-Type': 'application/json'}

    bulk_url = _url + BULK_ENDPOINT

    request_body = {'entities': data}

    response = requests.request(method='POST', url=bulk_url, json=request_body,
                                headers=_headers)

    response.raise_for_status()

    if response is not None and not response.ok:
        logger.error('Unable to create lineage. Response: {resp}'.format(
                          resp=response.text))
