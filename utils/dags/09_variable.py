
"""
1. Variable에 등록한 변수를 사용하기 위해선 {{ var.value.등록변수 }} 템플릿 사용
"""

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="09_variable",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["variable"]
) as dag:

    task_variable = BashOperator(
        task_id="task_variable",
        bash_command=f"echo variable: {{ var.value.sample }}",
    )
    
    task_token_variable = BashOperator(
        task_id="task_token_variable",
        bash_command=f"echo variable: {{ var.value.token_sample }}",
    )

    
