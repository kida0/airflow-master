
"""
1. BashOperator의 경우 bash_command와 env에 template_fields를 사용할 수 있음
    - 여기서는 env에 template_fields를 사용
2. PythonOperator는 templates_dict, op_args, op_kwargs에 template_fields 사용 가능
    - @task에는 op_args, op_kwargs를 넣을 수 없음
    - 따라서, op_kwargs를 사용하려면 PythonOperator를 사용해야 함
3. 
"""

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.decorators import task

with DAG(
    dag_id="06_template",
    description="description을 달아보자!",
    schedule="0 0 1,2,3 * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["template", "bash", "python"],
) as dag:
    
    bash_basic = BashOperator(
        task_id="bash_basic",
        bash_command="echo 'data_interval_end: {{ data_interval_end }}'",
    )
    
    bash_env = BashOperator(
        task_id="bash_env",
        env={
            "START_DATE": "{{ data_interval_start | ds }}",
            "END_DATE": "{{ data_interval_end | ds_nodash }}"
        },
        bash_command="echo $START_DATE && echo $END_DATE"
    )
    
    bash_basic >> bash_env
    
    def python_fn1(start_date, end_date):
        print(start_date)
        print(end_date)
        
    python_task1 = PythonOperator(
        task_id="python_task1",
        python_callable=python_fn1,
        op_kwargs={
            "start_date": "{{ data_interval_start | ds }}",
            "end_date": "{{ data_interval_end | ds_nodash }}"
        }
    )
        
    @task(task_id="python_task2")
    def python_fn2(**kwargs):
        print("data_interval_start:" + str(kwargs["data_interval_start"]))
        print("data_interval_end:" + str(kwargs["data_interval_end"]))
        print("task_instance:" + str(kwargs["ti"]))
        
    python_task1 >> python_fn2()