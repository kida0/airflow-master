
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="15_trigger_dag_run_operator",
    description="triggered by 03_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["trigger"],
) as dag:
    
    task_start = BashOperator(
        task_id="task_start",
        bash_command='echo "START"'
    )
    
    task_trigger_dag_run = TriggerDagRunOperator(
        task_id="task_trigger_dag_run",
        trigger_dag_id="03_python_operator",
        trigger_run_id=None,
        execution_date="{{ data_interval_start }}",
        reset_dag_run=True,
        wait_for_completion=False,
        poke_interval=60,
        allowed_states=["success"],
        failed_states=None,
    )
    
    task_start >> task_trigger_dag_run