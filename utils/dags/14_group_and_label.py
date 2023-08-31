
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task, task_group
from airflow.utils.task_group import TaskGroup
from airflow.utils.edgemodifier import Label

with DAG(
    dag_id="14_group_and_label",
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["group", "label"]
) as dag:
    
    # @task_group 데코레이터를 이용하는 방법
    def task_inner(**kwargs):
        text = kwargs.get("text") or ""
        print(text)
        
    @task_group(group_id="task_group")
    def group1():
        """ task_group 데코레이터를 이용하는 경우 docstring이 tooltip으로 표기 """
        
        @task(task_id="task_inner1")
        def task_inner1(**kwargs):
            print("task_group의 첫 task")
            
        task_inner2 = PythonOperator(
            task_id="task_inner2",
            python_callable=task_inner,
            op_kwargs={"text": "task_group의 두 번째 task"}
        )
        
        task_inner1() >> task_inner2
        
    
    # TaskGroup 메서드를 이용하는 방법
    with TaskGroup(group_id="TaskGroup", tooltip="TaskGroup 메서드의 경우 tooltip arg를 사용") as group2:
        """ 여기에 적은 docstring을 표시되지 않음"""
        
        @task(task_id="task_inner1")
        def task_inner1(**kwargs):
            print("TaskGroup의 첫 task")
            
        task_inner2 = PythonOperator(
            task_id="task_inner2",
            python_callable=task_inner,
            op_kwargs={"text": "TaskGroup의 두 번째 task"}
        )
        
        task_inner1() >> task_inner2
        
    group1() >> Label("conn groups")>> group2