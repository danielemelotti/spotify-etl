from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import logging
from logging.config import dictConfig

from spotify_etl import run_spotify_etl

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr, change it to stdout
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)
logger.debug("Starting to parse the DAG file")

# Creating a dictionary for the parameters we want to pass to Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 20), #starting date should be hard coded
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes = 1)
}

dag = DAG(
    'spotify_dag',
    default_args = default_args,
    description = 'Our first DAG with ETL process!',
    schedule = timedelta(days = 1),
)

def just_a_function():
    print("I'm going to show you something :)")

run_etl = PythonOperator(
    task_id = 'whole_spotify_etl',
    python_callable = run_spotify_etl,
    dag = dag,
)

run_etl