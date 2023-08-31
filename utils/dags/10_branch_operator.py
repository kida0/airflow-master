
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator

with DAG(
    dag_id="10_branch_operator",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    tags=["branch", "python"],
) as dag:
    
    def select_task():
        import random
        games = ["lostark", "overwatch", "dbd"]
        game = random.choice(games)
        if game == "lostark":
            return "task_lostark"
        elif game in ["overwatch", "dbd"]:
            return ["task_overwatch", "task_dbd"]
        
    def return_fn(**kwargs):
        from pprint import pprint
        if kwargs["user"] == "bard":
            pprint(kwargs)
        else:
            print(kwargs["user"])
    
    task_branch = BranchPythonOperator(
        task_id="task_branch",
        python_callable=select_task,
        # op_args=None,
        # op_kwargs=None,
    )
    
    task_lostark = PythonOperator(
        task_id="task_lostark",
        python_callable=return_fn,
        op_kwargs={"user": "bard"}
    )
    
    task_overwatch = PythonOperator(
        task_id="task_overwatch",
        python_callable=return_fn,
        op_kwargs={"user": "ana"}
    )
    
    task_dbd = PythonOperator(
        task_id="task_dbd",
        python_callable=return_fn,
        op_kwargs={"user": "surviver"}
    )
    
    task_branch >> [task_lostark, task_overwatch, task_dbd]
        