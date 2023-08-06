
from __future__ import annotations
import logging
import shutil
import sys
import tempfile
import time
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import ExternalPythonOperator, PythonVirtualenvOperator

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable

def x():
    pass

with DAG(
    dag_id="dags_python_task_decorator",
    scedule="0 2 * * 1",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    
    @task(task_id="print_the_context")
    def print_context(some_input):
        print(some_input)
    
    python_task_1 = print_context("task_decorator 실행")
        