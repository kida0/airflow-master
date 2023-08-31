
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from hooks.custom_postgres_hook import CustomPostgresHook

with DAG(
    dag_id="17_base_hook",
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["postgres", "base", "hook"]
) as DAG:
    
    def insert_postgres(postgres_conn_id, table, file_name, **kwargs):
        custom_postgres_hook = CustomPostgresHook(postgres_conn_id=postgres_conn_id)
        custom_postgres_hook.bulk_load(
            table=table, file_name=file_name, delimiter=",", is_header=True, is_replace=True)
        
    insert_postgres = PythonOperator(
        task_id="insert_postgres",
        python_callable=insert_postgres,
        op_kwargs={
            "postgres_conn_id": "conn-custom-postgres",
            "table": "NumCorona",
            "file_name": "/opt/airflow/files/corona/{{ data_interval_end.in_timezone('Asia/Seoul') | ds_nodash }}/num_corona.csv"
        },
    )
    
    insert_postgres