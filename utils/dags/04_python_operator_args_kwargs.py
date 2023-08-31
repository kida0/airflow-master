
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from common.myfunc import member, member2

with DAG(
    dag_id="04_python_operator_args_kwargs",
    schedule="0 0 L * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["python", "kwargs"],
) as dag:
    
    member_task = PythonOperator(
        task_id="member_task",
        python_callable=member,
        op_args=["kida", "INTP", "data scientist", "happy"]
    )
    
    member2_task = PythonOperator(
        task_id="member2_task",
        python_callable=member2,
        op_args=["kida", "INTP", "data scientist", "happy"],
        op_kwargs={
            "email": "gmail",
            "interest": "game",
            "lover": "coffee",
        }
    )
    
    member_task >> member2_task
    