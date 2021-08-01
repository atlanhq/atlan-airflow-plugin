from airflow.lineage.backend.atlas import AtlasBackend  # type: ignore
import hashlib
from typing import List, Tuple, Dict, Any

from airflow.utils.log.logging_mixin import LoggingMixin  # type: ignore
from atlan_airflow_plugin.lineage.assets import AtlanProcess

logger = LoggingMixin().log


class Backend(AtlasBackend):

    @staticmethod  # noqa: C901
    def create_lineage_meta(
        operator,
        inlets,
        outlets,
        context,
    ):

        # type: (object, list, list, dict) -> Tuple[List[dict], List[dict], List[dict]]
        # Creating input entities

        inlet_list = []  # type: List[dict]
        inlet_ref_list = []  # type: List[dict]
        if inlets:
            for entity in inlets:
                if entity is None:
                    continue

                entity.set_context(context)
                try:
                    entity_dict = entity.as_nested_dict()
                except Exception as e:  # noqa: F841

                    entity_dict = entity.as_dict()

                inlet_list.append(entity_dict)
                logger.info('Inlet Entity : {}'.format(entity.type_name))
                inlet_ref_list.append({'typeName': entity.type_name,
                                       'uniqueAttributes': {'qualifiedName': entity.qualified_name}})

        # Creating output entities

        outlet_list = []  # type: List[dict]
        outlet_ref_list = []  # type: List[dict]
        if outlets:
            for entity in outlets:
                if not entity:
                    continue

                entity.set_context(context)
                try:
                    entity_dict = entity.as_nested_dict()
                except Exception as e:  # noqa: F841

                    entity_dict = entity.as_dict()

                logger.info('Outlet Entity : {}'.format(entity.type_name))

                outlet_list.append(entity_dict)
                outlet_ref_list.append({'typeName': entity.type_name,
                                        'uniqueAttributes': {'qualifiedName': entity.qualified_name}})

        # Creating dag and operator entities

        atlan_process = []  # type: List[dict]

        data = {
            'name': operator.task_id,  # type: ignore
            'description': 'Lineage pushed from Airflow',
            'inputs': inlet_ref_list,
            'outputs': outlet_ref_list,
        }

        iostring = getIOhash(inlet_ref_list, outlet_ref_list)
        iohash = hashlib.sha224(iostring.encode()).hexdigest()

        qualified_name = '{source_prefix}/{query_hash}/{granularity}/{iohash}'.format(
            source_prefix='airflow', query_hash='', granularity='table', iohash=iohash)

        process = AtlanProcess(name=qualified_name, data=data)

        atlan_process.append(process.as_dict())

        return (inlet_list, outlet_list, atlan_process)


def getIOhash(source, target):
    # type: (List[Dict[Any, Any]], List[Dict[Any, Any]]) -> str

    (source_asset, target_asset) = ([], [])

    for asset in source:
        source_asset.append(asset['uniqueAttributes']['qualifiedName'])

    for asset in target:
        target_asset.append(asset['uniqueAttributes']['qualifiedName'])

    iostring = ''.join(sorted(source_asset)) \
        + ''.join(sorted(target_asset))
    return iostring
