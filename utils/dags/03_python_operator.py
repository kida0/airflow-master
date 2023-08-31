

"""
1. PythonOperator는 task_id, python_callable, op_args, op_kwargs를 기본적으로 숙지하고
2. templates_dict, templates_exts에 대해서도 생각해봐야 함
3. @task를 쓰면 dag 내에서 함수를 정의하고 PythonOperator를 사용하지 않아서 장점
"""

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="03_python_operator",
    schedule="0 8-16 * 8 5",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["python"],
) as dag:
    
    import random
    def select_game():
        games = ["lostark", "overwatch", "dbd"]
        rand_int = random.randint(0, len(games)-1)
        print(games[rand_int])
        
    select_game_task = PythonOperator(
        task_id="select_game_task",
        python_callable=select_game,
        # templates_dict=None,
        # templates_exts=[".sql", ".hql"],
    )
    
    select_game_task