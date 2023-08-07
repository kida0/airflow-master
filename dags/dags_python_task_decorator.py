
import pendulum
from airflow import DAG
from airflow.decorators import task

def x():
    pass

with DAG(
    dag_id="dags_python_task_decorator",
    schedule="0 2 * * 1",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    
    @task(task_id="print_the_context")
    def print_context(some_input):
        print(some_input)
    
    python_task_1 = print_context("task_decorator 실행")
    python_task_1
    