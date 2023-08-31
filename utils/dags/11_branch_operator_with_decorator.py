
import pendulum
from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="11_branch_operator_with_decorator",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    tags=["branch", "decorator", "python"],
) as dag:
    
    @task.branch(task_id="task_branch")
    def task_branch():
        import random
        games = ["lostark", "overwatch", "dbd"]
        game = random.choice(games)
        if game == "lostark":
            return "task_lostark"
        elif game in ["overwatch", "dbd"]:
            return ["task_overwatch", "task_dbd"]
    
    @task(task_id="task_lostark")
    def task_lostark():
        print("bard")
        
    @task(task_id="task_overwatch")
    def task_overwatch():
        print("ana")
        
    @task(task_id="task_dbd")
    def task_dbd():
        print("surviver")
    
    task_branch() >> [task_lostark(), task_overwatch(), task_dbd()]
        