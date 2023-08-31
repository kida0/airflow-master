
"""
1. BashOperator는 task_id, bash_command, #dag선택 으로 구성
    dag 파라미터를 사용하는 경우
    dag = DAG()를 정의한 후 BashOperator(task_id, bash_command, dag)로 task 설정

2. Cron 스케쥴링 방법 눈여겨 보기
3. dags를 제외한 py, sh 파일은 plugins 폴더에 구조화하여 저장
"""


import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="01_bash_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["bash"],
) as dag:
    
    bash_task1 = BashOperator(
        task_id="bash_task1",
        bash_command="echo whoami",
    )
    
    bash_task2 = BashOperator(
        task_id="bash_task2",
        bash_command="echo $HOSTNAME"
    )
    
    bash_task1 >> bash_task2
    
    
    