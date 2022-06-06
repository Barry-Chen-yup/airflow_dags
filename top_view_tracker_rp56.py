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
    dag_id='SSH_And_Mail_rpi5&6',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='0 21 * * *',
    start_date=days_ago(2),
    catchup=False, # missing a dag not run again
    tags=['rpi5_6'],
    max_active_runs=1, # Follow a sequence to avoid deadlock when using MySQL
) as dag:

    ssh = SSHOperator(
        task_id='ssh2workspace',
        ssh_conn_id='workspace_5_6',
        command='/workspace/tracker.sh ',
    ) 
    email_task = EmailOperator(
        task_id='send_email',
        to='akj00173@gmail.com',
        subject='Airflow success',
        html_content=""" <h3>Top-view-rpi5&6-tracker-success</h3> {{ execution_date }}<br/>""",
        dag=dag
    )
    ssh >> email_task