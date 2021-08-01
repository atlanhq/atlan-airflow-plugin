import six
from jinja2 import Environment
from typing import List, Any
from atlan_airflow_plugin.lineage.assets import AtlanAsset


class AtlanTable(AtlanAsset):

    type_name = 'AtlanTable'
    attributes = ['name']

    def __init__(
        self,
        name: str = None,
        data: dict = None,
        **kwargs: Any,
    ):

        super(AtlanAsset, self).__init__(name=name, data=data)
        if name:
            self._qualified_name = name

    def as_nested_dict(self):

        # type: () -> List[dict]

        d = self.as_dict()

        entities = []  # type: List[dict]
        entities.append(d)

        return entities

    def as_dict(self):

        # type: () -> dict

        attributes = dict(self._data)
        attributes.update({'qualifiedName': self.qualified_name})

        env = Environment()
        if self.context:
            for (key, value) in six.iteritems(attributes):
                try:
                    attributes[key] = \
                        env.from_string(value).render(**self.context)
                except Exception as e:  # noqa: F841
                    pass

        d = {'typeName': self.type_name, 'attributes': attributes}
        return d
