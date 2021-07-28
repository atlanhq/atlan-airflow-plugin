from airflow.lineage.datasets import DataSet  # type: ignore

class AtlanProcess(DataSet):

    type_name = "AtlanProcess"
    attributes = ["name", "description", "inputs", "outputs"]
