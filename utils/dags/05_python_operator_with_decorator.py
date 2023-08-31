
import pendulum
from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="05_python_operator_with_decorator",
    schedule="0 0 L * * ",
    start_date=pendulum.datetime(2023, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["python", "decorator", "kwargs"]
) as dag:
    from pprint import pprint
    import time
    
    @task(task_id="print_context")
    def print_context(context=None, **kwargs):
        pprint(kwargs)
        print(context)
        return "Whatever you return gets printed in the logs"
        
    run_this = print_context()
    
    for i in range(1, 4):
        
        # @task(task_id="log_sql_query", template_dict={"query": "sql/sample.sql"}, templates_exts=[".sql"])
        # def log_sql(**kwargs):
        #     logging.info("Python task decorator query: %s", str(kwargs["templates_dict"]["query"]))
        
        # log_the_sql = log_sql()
        
        @task(task_id=f"sleep_for_{i}")
        def my_sleeping_function(time_sleep):
            time.sleep(time_sleep)
            
        sleeping_task = my_sleeping_function(time_sleep=(i*5))
    
    
    run_this >> sleeping_task # >> log_the_sql