from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
import os, airflow
from airflow.utils.dates import days_ago
from airflow.operators.email import EmailOperator
import pendulum
import time
from airflow.contrib.operators.ssh_operator import SSHOperator

local_tz = pendulum.timezone("Asia/Taipei")

default_args = {
    'owner': 'barry',
    'depends_on_past': False,
    #'start_date': airflow.utils.dates.days_ago(1),
    'email': ['akj00173@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id='ssh_test',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    catchup=False, # missing a dag not run again
    tags=['example'],
    max_active_runs=1, # Follow a sequence to avoid deadlock when using MySQL
) as dag:

    ssh = SSHOperator(
        task_id='ssh',
        ssh_conn_id='workspace',
        command='/workspace/tracker.sh ',
    ) 
    # python_timestamp = PythonOperator(
    #     task_id='python',
    #     python_callable=fun,
    #     #provide_context=True,
    #     #dag=dag
    # )        python /workspace/tracker/code/track_chicken_date_gpu.py /workspace/nas-data/Animal/chicken_video/20210131
    # cleanup_task = BashOperator(
    #     task_id='task_1_data_file_cleanup',
    #     # cmd = 'python3 /workspace/tracker/code/track_chicken_test.py "/workspace/nas-data/Animal/chicken_video/"$(date -d "yesterday" +%Y%m%d)'
    #     bash_command='python3 /workspace/tracker/code/track_chicken_date_gpu.py "/workspace/nas-data/Animal/chicken_video/"$(date -d "yesterday" +%Y%m%d)',
    #     dag=dag
    # )
    # email_task = EmailOperator(
    #     task_id='send_email',
    #     to='akj00173@gmail.com',
    #     subject='Airflow success',
    #     html_content=""" <h3>Email Test</h3> {{ execution_date }}<br/>""",
    #     dag=dag
    # )
    # cleanup_task >> email_task
    ssh