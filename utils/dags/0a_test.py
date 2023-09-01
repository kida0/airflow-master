
import pendulum
import datetime
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='0a_test.py',
    description='airflow documentation tutorial DAG',
    ownder='kida',
    schedule=None,
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=['example'],
    
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'retries': 1,                                   # 실패 시 재시도 횟수
        'retry_delay': datetime.timedelta(minutes=5),   # 재시도 시간 간격
        'email': None,                                  # str, 이메일을 보낼 주소
        'eamil_on_retry': None,                         # 재시도에도 이메일을 보낼 것인지
        'email_on_failuer': True,                       # 실패했을 때도 이메일 보낼 것인지
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',                           # task를 실행할 때 어떤 pool에서 실행할지
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),  # task가 얼마나 돌면 실패로 간주할지
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'trigger_rule': 'all_success'
    }
) as dag:
    
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date'
    )
    
    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
    )
    
    t1.doc_md = dedent(
        """\
        ## Hello Airflow!
        #### Task Documentation
        You can document your task using the attributes `doc_md`(markdown)
        """
    )
    
    dag.doc_md = __doc__  # 
    dag_doc_md = """
    This is a documentation placed anywhere
    """
    
    templated_command = dedent(
        """
        {% for i in range(5) %}  # code logic {% %}
            echo '{{ ds }}'
            echo '{{ macros.ds_add(ds, 7) }}'
        {% endfor %}
        """  
    )
    
    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
    )
    
    t1 >> [t2, t3]
    
    