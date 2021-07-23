import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from atlan_airflow_plugin.operators.bm_operator import AtlanBmOperator

args = {"owner": "Atlan Technologies Pvt Ltd", "start_date": airflow.utils.dates.days_ago(1)}

dag = DAG(dag_id="atlan_airflow_bm_demo", default_args=args, schedule_interval=None)

guid = "f947a0ad-e34f-45e6-b29f-e004e60e72f0"

bm = {
    "ETL": {
            "Job Link": "https://airflow.atlan.com/dag_ig/run_id",
            "Last Run Status": "Success",
            "Last Run Date": 1601317800000
        }
}

with dag:

    some_task = BashOperator(task_id="any_task", bash_command="echo Hello!")

    push_bm = AtlanBmOperator(
        task_id="send_bm_to_atlan", asset_guid=guid, bm=bm, if_overwrite=True
    )

some_task >> push_bm
