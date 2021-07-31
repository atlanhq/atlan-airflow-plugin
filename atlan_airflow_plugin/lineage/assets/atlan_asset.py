from airflow.lineage.datasets import DataSet  # type: ignore


class AtlanAsset(DataSet):

    type_name = ''
    attributes = ['name']

    def __init__(
        self,
        name: str = None,
        data: dict = None,
        **kwargs
    ):

        super(DataSet, self).__init__(name=name, data=data)
