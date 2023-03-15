from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'AUTOMATISATION',
    default_args=default_args,
    description='Charger les données de POSTGRESQL ==> ELK',
    schedule_interval=timedelta(seconds=3),
)

task1 = BashOperator(
    task_id='demarre_ELK',
    bash_command='docker-compose -f /home/dev/soute/ELK/docker-compose.yml up -d',
    dag=dag,
)

task2 = BashOperator(
    task_id='Chargement_des_données_in_ELK',
    bash_command='echo dev | sudo -S /usr/share/logstash/bin/logstash --path.settings=/etc/logstash/ -f /etc/logstash/conf.d/data.conf',
    retries=3,
    dag=dag,
)

task1 >> task2
