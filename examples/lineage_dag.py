import airflow
from airflow import DAG
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator

from atlan_airflow_plugin.lineage.assets import AtlanTable

args = {"owner": "Atlan Technologies Pvt Ltd", "start_date": airflow.utils.dates.days_ago(1)}

dag = DAG(
    dag_id="atlan_airflow_lineage_demo", default_args=args, schedule_interval='@daily'
)

move_data_query = '''
INSERT INTO AIRFLOW_LINEAGE.public.child_table
SELECT * FROM AIRFLOW_LINEAGE.public.parent_table
'''


with dag:

    move_data = SnowflakeOperator(

        task_id="move_data",

        sql=move_data_query,

        snowflake_conn_id="snowflake_common",

        inlets={"datasets": [AtlanTable(name="snowflake/abc.ap-south-1/airflow_lineage/public/parent_table")]},

        outlets={"datasets": [AtlanTable(name="snowflake/abc.ap-south-1/airflow_lineage/public/child_table")]}

    )


move_data

