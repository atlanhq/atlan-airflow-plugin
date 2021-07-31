from atlan_airflow_plugin.lineage.assets import AtlanAsset
class AtlanProcess(AtlanAsset):

    type_name = 'AtlanProcess'
    attributes = ['name', 'description', 'inputs', 'outputs']

    def __init__(
        self,
        name: str = None,
        data: dict = None,
        **kwargs
    ):

        super(AtlanAsset, self).__init__(name=name, data=data)
        if name:
            self._qualified_name = name
