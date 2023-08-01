import datetime
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from func import select_fruit

with DAG(
    dag_id="dags_python_operator",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag:    
    py_t1 = PythonOperator(
        task_id="py_t1",
        python_callable=select_fruit
    )

    