import pendulum
from airflow import DAG
from airflow.decorators import task, task_group
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="dags_python_with_task_group",
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    
    def inner_func(**kwargs):
        msg = kwargs.get("msg") or ''
        print(msg)
        
        
    @task_group(group_id="first_gorup")
    def group_1():
        """ tooltip으로 표기됩니다: task_group 데코레이터를 이용한 첫 번째 그룹입니다 """
        
        @task(task_id="inner_function1")
        def inner_func1(**kwargs):
            print("첫 번째 TaskGroup 내 첫 번째 task입니다")
            
        inner_function2 = PythonOperator(
            task_id="inner_function2",
            python_callable=inner_func,
            op_kwargs={"msg": "첫 번째 TaskGroup내 두 번째 task입니다"}
        )
        
        inner_func1() >> inner_function2
        
        
    
    with TaskGroup(group_id="second_group", tooltip="두 번째 그룹입니다") as group_2:
        """ 여기에 적은 docstring은 표시되지 않습니다 """
        
        @task(task_id="inner_function1")
        def inner_func1(**kwargs):
            print("두 번째 TaskGroup 내 첫 번째 task입니다")
            
        inner_function2 = PythonOperator(
            task_id="inner_function2",
            python_callable=inner_func,
            op_kwargs={"msg": "두 번째 TaskGroup 내 두 번째 task입니다"}
        )
        
        inner_func1() >> inner_function2
        
    group_1() >> group_2
    