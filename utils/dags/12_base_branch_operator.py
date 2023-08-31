
import pendulum
from airflow import DAG
from airflow.operators.branch import BaseBranchOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="12_base_branch_operator",
    schedule="0 0 L * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["base", "branch"],
) as dag:
    
    class CustomizedBranch(BaseBranchOperator):
        def __init__(self, params=None, *args, **kwargs):
            super().__init__(*args, **kwargs) # super의 init을 상속
            self.params = params
        
        def choose_branch(self, context):
            import random
            from pprint import pprint
            print("CONTEXT: ")
            pprint(context)
            games = ["lostark", "overwatch", "dbd"]
            game = random.choice(games)
            if game == "lostark":
                return "task_lostark"
            elif game in ["overwatch", "dbd"]:
                return ["task_overwatch", "task_dbd"]
            else:
                return self.params

    
    task_branch = CustomizedBranch(task_id="task_branch")
    
    def return_fn(**kwargs):
        from pprint import pprint
        if kwargs["user"] == "bard":
            pprint(kwargs)
        else:
            print(kwargs["user"])
    
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