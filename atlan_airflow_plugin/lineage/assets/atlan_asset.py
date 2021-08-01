from airflow.lineage.datasets import DataSet  # type: ignore
from typing import Any


class AtlanAsset(DataSet):

    type_name = ''
    attributes = ['name']

    def __init__(
        self,
        name: str = None,
        data: dict = None,
        **kwargs: Any,
    ):

        super(DataSet, self).__init__(name=name, data=data)
