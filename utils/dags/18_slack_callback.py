
import pendulum
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from config.on_failure_callback_to_slack import on_failure_callback_to_slack

with DAG(
    dag_id="18_slack_callback",
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["slack"],
    default_args={    # default_args 들어야겠네 => 아래 모든 task가 default_args를 가지게 됨
        "on_failure_callback": on_failure_callback_to_slack,
        "execution_timeout": timedelta(seconds=60),  # 60초 동안 돌고 안끝나면 실패
    }
) as dag:
    
    task_sleep_30 = BashOperator(
        task_id="task_sleep_90",
        bash_command="sleep 90",
    )
    
    task_exit_1 = BashOperator(
        task_id="task_exit_1",
        trigger_rule="all_done",
        bash_command="exit 1",
    )
    
    task_sleep_30 >> task_exit_1