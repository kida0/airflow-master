
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="02_bash_operator_with_plugins",
    schedule="30 8 */2 * 1",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["bash", "plugins"]
) as dag:
    
    orange_task = BashOperator(
        task_id="orange_task",
        bash_command="/opt/airflow/plugins/shell/select_fruit.sh ORANGE",
        # docker-compose 파일의 위치를 기준 디렉터리 설정
    )
    
    avocado_task = BashOperator(
        task_id="avocado_task",
        bash_command="/opt/airflow/plugins/shell/select_fruit.sh AVOCADO",
    )
    
    orange_task >> avocado_task
    
    