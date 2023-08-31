
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="19_pool.py",
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["pool"],
    default_args={
        "pool": "pool_small"
    }
) as dag:
    
    task_bash1 = BashOperator(
        task_id = "task_bash1",
        bash_command="sleep 30",
        priority_weight=6
    )
    
    task_bash2 = BashOperator(
        task_id = "task_bash2",
        bash_command="sleep 30",
        priority_weight=5
    )
    
    task_bash3 = BashOperator(
        task_id = "task_bash3",
        bash_command="sleep 30",
        priority_weight=4
    )
    
    task_bash4 = BashOperator(
        task_id = "task_bash4",
        bash_command="sleep 30",
    )
    
    task_bash5 = BashOperator(
        task_id = "task_bash5",
        bash_command="sleep 30",
    )
    
    task_bash6 = BashOperator(
        task_id = "task_bash6",
        bash_command="sleep 30",
        # default priority_weight=1
    )
    
    task_bash7 = BashOperator(
        task_id = "task_bash7",
        bash_command="sleep 30",
        priority_weight=7
    )
    
    task_bash8 = BashOperator(
        task_id = "task_bash8",
        bash_command="sleep 30",
        priority_weight=8
    )
    
    task_bash9 = BashOperator(
        task_id = "task_bash9",
        bash_command="sleep 30",
        priority_weight=9
    )