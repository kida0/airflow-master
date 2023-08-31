
import pendulum
from airflow import DAG
from operators.seoul_api_to_csv_operator import SeoulApiToCsvOperator

with DAG(
    dag_id="16_base_operator",
    description="operators/seoul_api_to_csv_operator.py에 BaseOperator 정의",
    schedule="0 7 * * *",
    start_date=pendulum.datetime(2023, 4, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["base"],
) as dag:
    
    """ 서울시 코로나19 확진자 발생 동향 """
    num_corona = SeoulApiToCsvOperator(
        task_id="num_corona",
        data_name="TbCorona19CountStatus",
        file_path="/opt/airflow/files/corona/{{ data_interval_end.in_timezone('Asia/Seoul') | ds_nodash }}",
        file_name="num_corona.csv"
    )
    
    """ 서울시 코로나19 백신 예방접종 동향"""
    num_vacc = SeoulApiToCsvOperator(
        task_id="num_vacc",
        data_name="tvCorona19VaccinestatNew", 
        file_path="/opt/airflow/files/vacc/{{ data_interval_end.in_timezone('Asia/Seoul') | ds_nodash }}",
        file_name="num_vacc.csv"
    )
    
    num_corona >> num_vacc
