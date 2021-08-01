from typing import Any  # noqa: F401
from airflow.models import BaseOperator
from atlan_airflow_plugin.hooks import AtlanHook


class AtlanBMOperator(BaseOperator):

    """
    Atlan BM Operator
    :param asset_guid:        Asset GUID.
    :type asset_guid:         string
    :param bm:        BM to be attached to asset.
    :type bm:         dict
    :param overwrite:        Weather to overwrite BM or not.
    :type overwrite:         bool
    """

    BM_ENDPOINT = "/api/metadata/atlas/tenants/default/entity/guid/{asset_guid}/businessmetadata?isOverwrite={overwrite}"

    def __init__(
        self,
        atlan_conn_id: str = "atlan_default",
        retry_limit: int = 3,
        retry_delay: int = 5,
        timeout: int = 30,
        asset_guid: str = None,
        bm: dict = None,
        overwrite: bool = None,
        **kwargs: Any,
    ):

        super().__init__(**kwargs)
        self.asset_guid = asset_guid
        self.bm = bm
        self.overwrite = overwrite

        self.atlan_conn_id = atlan_conn_id
        self.retry_limit = retry_limit
        self.retry_delay = retry_delay  # type: ignore
        self.timeout = timeout

    def execute(self, context):
        # type: (Any) -> None

        url = self.BM_ENDPOINT.format(
            asset_guid=self.asset_guid, overwrite=self.overwrite
        )

        request_info = ("POST", url)

        session = AtlanHook(
            atlan_conn_id=self.atlan_conn_id,
            retry_limit=self.retry_limit,
            retry_delay=self.retry_delay,  # type: ignore
            timeout=self.timeout,
        )

        response = session.call_api(request_info=request_info, payload=self.bm)

        if response is not None and not response.ok:
            self.log.error(
                "Unable to update BM for Asset GUID {guid}. Response: {resp}".format(
                    guid=self.asset_guid, resp=response.text
                )
            )
