import datetime
import pendulum
from airflow import DAG
from airflow.operators.email import EmailOperator

with DAG(
    dag_id="dags_email_operator",
    schedule="0 8 1 * *",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    send_email = EmailOperator(
        task_id="send_email",
        to="",
        cc="",
        subject="[Airflow] Alarm",
        html_content="Ariflow 작업이 완료되었습니다. <br/>"
    )