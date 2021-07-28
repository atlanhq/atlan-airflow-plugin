import six
from jinja2 import Environment

from airflow.lineage.datasets import *  # type: ignore # noqa: F401, F403
from airflow.lineage.datasets import DataSet  # type: ignore


class Table(DataSet):

    type_name = ''
    attributes = ['name']

    def __init__(
        self,
        name=None,
        data=None,
        **kwargs
        ):
        super(DataSet, self).__init__(name=name, data=data)


class AtlanTable(Table):

    type_name = 'AtlanTable'
    attributes = ['name']

    def __init__(
        self,
        name=None,
        data=None,
        **kwargs
        ):
        super(Table, self).__init__(name=name, data=data)
        if name:
            self._qualified_name = name

    # TODO: change function name

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
                except Exception as e:
                    pass

        d = {'typeName': self.type_name, 'attributes': attributes}
        return d
