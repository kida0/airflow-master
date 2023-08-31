
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from airflow.decorators import task

with DAG(
    dag_id="13_trigger_rule",
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["trigger"],
) as dag:
    
    bash_upstream = BashOperator(
        task_id="bash_upstream",
        bash_command="echo upstream"
    )
    
    @task(task_id="upstream1")
    def upstream1():
        raise AirflowException("raise exception")
    
    @task(task_id="downstream1", trigger_rule="all_done")
    def downstream1():
        print("downstream: 정상 처리")
        
    [bash_upstream, upstream1()] >> downstream1()
    
    
    @task.branch(task_id="task_branch")
    def task_branch():
        import random
        games = ["lostark", "dbd"]
        game = random.choice(games)
        if game == "lostark":
            return "task_lostark"
        else:
            return "task_dbd"
    
    @task(task_id="task_lostark")
    def task_lostark():
        print("정상 처리")
        
    @task(task_id="task_dbd")
    def task_dbd():
        print('정상 처리')
        
    @task(task_id="downstream2", trigger_rule="none_skipped")
    def downstream2():
        print("정상 처리")
        
    task_branch() >> [task_lostark(), task_dbd()] >> downstream2()
    
    