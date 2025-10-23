from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.email import send_email_smtp
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from pendulum import datetime
from pathlib import Path
from dotenv import load_dotenv



from dags.scripts.download_gzip import download_pageviews 
from dags.scripts.extract_companies import filter_pageviews
from dags.scripts.load_data import load_pageviews
from utilities.format_html import format_results_as_html


# Configuration - Centralized data directory
load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR"))
TIMESTAMP = os.getenv("TIMESTAMP")

INPUT_FILE = DATA_DIR / f'pageviews-{TIMESTAMP}.txt'
OUTPUT_FILE = DATA_DIR / 'filtered_pageviews.txt'

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)



def notify_failure(context):
    """
    Custom function to send an email alert when a task fails.from airflow.utils.email import send_email_smtp
    """
    task_instance = context.get('task_instance')
    dag = context.get('dag')
    dag_id = dag.dag_id if dag else "unknown_dag"
    task_id = task_instance.task_id if task_instance else "unknown_task"
    execution_date = context.get('execution_date')
    log_url = task_instance.log_url if task_instance else ""

    subject = f"Airflow Task Failed: {dag_id}.{task_id}"
    html_content = f"""
    <h3 style="color:red;">Task Failed in DAG: {dag_id}</h3>
    <p><strong>Task:</strong> {task_id}</p>
    <p><strong>Execution Date:</strong> {execution_date}</p>
    <p><a href="{log_url}">View Task Log</a></p>
    """

    send_email_smtp(
        to="fatimaidris388@gmail.com",
        subject=subject,
        html_content=html_content,
    )




# Define the DAG
with DAG(
    dag_id="pageviews",
    start_date=datetime(2025, 10, 9),
    schedule=None,
    catchup=False,
    default_args={
        "retries": 0,
        #"retry_delay": timedelta(minutes=1),
        'owner': 'airflow',
        'email': ['fatimaidris388@gmail.com'],  # email(s) to notify
        'email_on_failure': False,            # send email when a task fails
        'email_on_retry': False,
        'on_failure_callback': notify_failure,
        },
    tags=['newdata', 'pageviews'],
) as dag:

    # Task 1: Download the pageview data
    download_data = PythonOperator(
        task_id='download_data',
        python_callable=lambda: download_pageviews(date_str=TIMESTAMP, out_dir=DATA_DIR),
    )

    # Task 2: Extract and filter pageviews
    extract_datapoints = PythonOperator(
        task_id='extract_datapoints',
        python_callable=lambda: filter_pageviews(input_file=INPUT_FILE, output_file=OUTPUT_FILE),
    )

    # Task 3: Create the Postgres table
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres_conn",
        sql="""
            DROP TABLE IF EXISTS pageviews;
            CREATE TABLE pageviews (
                project TEXT,
                page_title TEXT,
                count_views INT,
                total_response_size INT
            );
        """,
    )

    # Task 4: Load data to Postgres
    postgres_load = PythonOperator(
        task_id="postgres_load",
        python_callable=lambda: load_pageviews(),
    )

    # Task 5: Run simple analysis
    simple_analysis = SQLExecuteQueryOperator(
        task_id='simple_analysis',
        conn_id="postgres_conn",
        sql="""
            SELECT *
            FROM pageviews
            ORDER BY count_views DESC
            LIMIT 5;
        """,
        do_xcom_push=True,
    )

    # Python task to format SQL results
    format_html = PythonOperator(
    task_id='format_html',
    python_callable=format_results_as_html,
)


    send_results = EmailOperator(
    task_id='send_results',
    to='abdmlk.911@gmail.com',
    from_email='fatimaidris388@gmail.com',
    subject='Pageviews DAG Completed Successfully',
    html_content="{{ ti.xcom_pull(task_ids='format_html', key='formatted_html') }}",
    conn_id='smtp_conn',
    )

    # Define task dependencies
    download_data >> extract_datapoints >> create_table >> postgres_load >> simple_analysis >> format_html >> send_results