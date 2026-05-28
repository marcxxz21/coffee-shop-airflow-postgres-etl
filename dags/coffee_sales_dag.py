from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "marc",
    "retries": 1,
}


with DAG(
    dag_id="coffee_shop_sales_postgres_etl",
    default_args=default_args,
    description="ETL pipeline for Brewline retail sales Excel data using PostgreSQL",
    start_date=datetime(2026, 5, 1),
    schedule="@daily",
    catchup=False,
    tags=["beginner", "etl", "coffee-shop", "postgresql"],
) as dag:

    extract_sales_data = BashOperator(
        task_id="extract_sales_data",
        bash_command="cd /opt/airflow && python src/extract.py",
    )

    transform_sales_data = BashOperator(
        task_id="transform_sales_data",
        bash_command="cd /opt/airflow && python src/transform.py",
    )

    validate_sales_data = BashOperator(
        task_id="validate_sales_data",
        bash_command="cd /opt/airflow && python src/validate.py",
    )

    load_sales_data = BashOperator(
        task_id="load_sales_data_to_postgres",
        bash_command="cd /opt/airflow && python src/load.py",
    )

    create_sales_reports = BashOperator(
        task_id="create_sales_reports_from_postgres",
        bash_command="cd /opt/airflow && python src/report.py",
    )

    (
        extract_sales_data
        >> transform_sales_data
        >> validate_sales_data
        >> load_sales_data
        >> create_sales_reports
    )
