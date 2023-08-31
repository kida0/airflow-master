

"""
    1. DAG 스케쥴이 매월 말 일에 도는 상황에서 SQL의 BETWEEN 값에 전월 마지막일부터 어제까지를 주고 싶은 상황
    2. data_interval_start.in_timezone('Asia/Seoul')을 통해 UTC로 나오는 결과 조정 가능
    3. @task를 사용하는 경우 DAG 지정 시 task_id가 아닌 함수 명 사용
    4. relativedelta의 months, days, day의 차이 조심
"""

import pendulum
import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task

with DAG(
    dag_id="07_macro",
    schedule="1 0 L * *",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["macro", "bash", "python"]
) as dag:
    
    bash_task = BashOperator(
        task_id="bash_task",
        env={
            "START_DATE": "{{ data_interval_start.in_timezone('Asia/Seoul') | ds }}",
            "END_DATE": "{{ (data_interval_end.in_timezone('Asia/Seoul') - macros.dateutil.relativedelta.relativedelta(days=1)) | ds }}"
        },
        bash_command='echo "START_DATE: $START_DATE" &&  echo "END_DATE: $END_DATE"'
    )
    
    
    @task(task_id="python_task1",
          templates_dict={
              "start_date": "{{ (data_interval_end.in_timezone('Asia/Seoul') + macros.dateutil.relativedelta.relativedelta(months=-1, day=1)) | ds }}",
              "end_date": "{{ (data_interval_end.in_timezone('Asia/Seoul').replace(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1)) | ds }}"
          })
    def get_datetime_macro(**kwargs):
        templates_dict = kwargs.get("templates_dict") or {}
        if templates_dict:
            start_date = templates_dict.get("start_date") or "start_date 없음"
            end_date = templates_dict.get("end_date") or "end_date 없음"
            print(start_date)
            print(end_date)
        
        
    @task(task_id="python_task2")
    def get_datetime_calc(**kwargs):
        from dateutil.relativedelta import relativedelta
        
        data_interval_end = kwargs["data_interval_end"]
        prev_month_day_first = data_interval_end.in_timezone("Asia/Seoul") + relativedelta(months=-1, day=1)
        prev_month_day_last = data_interval_end.in_timezone("Asia/Seoul") + relativedelta(days=-1)
        print(prev_month_day_first.strftime("%Y-%m-%d"))
        print(prev_month_day_last.strftime("%Y-%m-%d"))
        
    bash_task >> get_datetime_macro() >> get_datetime_calc()
        
        
        
        
        