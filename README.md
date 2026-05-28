# Coffee Shop Airflow PostgreSQL ETL

This project is an end-to-end coffee shop sales ETL pipeline built with Apache Airflow, Python, pandas, PostgreSQL, SQLAlchemy, and Docker.

The pipeline extracts transaction data from an Excel file, cleans and validates the records, loads the processed data into a PostgreSQL database, and generates automated sales reports by date, product category, store location, and top products.

Apache Airflow is used to orchestrate, schedule, and monitor each stage of the workflow.

## Tech Stack

- Apache Airflow
- PostgreSQL
- Docker
- Python
- pandas
- SQLAlchemy
- SQL
- DBeaver

## Project Structure

```text
coffee_shop_etl/
├── dags/
│   └── coffee_sales_dag.py
├── data/
│   ├── raw/
│   │   └── coffee_shop_sales.xlsx
│   ├── processed/
│   │   ├── extracted_sales.csv
│   │   └── clean_sales.csv
│   └── reports/
│       ├── daily_sales_report.csv
│       ├── category_sales_report.csv
│       ├── store_sales_report.csv
│       └── top_products_report.csv
├── logs/
├── plugins/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── report.py
│   └── utils/
│       ├── config.py
│       └── helpers.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Pipeline Steps

1. Extract sales data from `data/raw/coffee_shop_sales.xlsx`.
2. Transform column names, data types, text fields, dates, times, and sales totals.
3. Validate required fields, positive values, unique transactions, and total amount calculations.
4. Load cleaned records into PostgreSQL table `sales`.
5. Generate CSV reports in `data/reports/`.

## Reports

- Daily sales report
- Product category sales report
- Store location sales report
- Top products report

## Setup

Install:

- VS Code
- Docker Desktop
- Git
- Python
- DBeaver

PostgreSQL does not need to be installed separately. It runs inside Docker using the `postgres:16` image from `docker-compose.yaml`.

## Environment Variables

Create a `.env` file from `.env.example`:

```env
POSTGRES_USER=coffee_user
POSTGRES_PASSWORD=coffee_password
POSTGRES_DB=coffee_sales_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

## Run With Docker

Build and start the services:

```bash
docker compose build
docker compose up
```

Open Airflow:

```text
http://localhost:8080
```

Trigger the DAG:

```text
coffee_shop_sales_postgres_etl
```

## Connect With DBeaver

Use these PostgreSQL connection settings:

| Field | Value |
| --- | --- |
| Host | `localhost` |
| Port | `5433` |
| Database | `coffee_sales_db` |
| Username | `coffee_user` |
| Password | `coffee_password` |

After the DAG runs successfully, refresh the database connection and open:

```text
Schemas > public > Tables > sales
```

## PostgreSQL vs SQLite

| Part | SQLite Version | PostgreSQL Version |
| --- | --- | --- |
| Database | `coffee_sales.db` file | PostgreSQL Docker container |
| Python connection | `sqlite3.connect()` | SQLAlchemy engine |
| Database driver | Built-in SQLite | `psycopg2-binary` |
| Viewing tool | DB Browser for SQLite | DBeaver |
| Docker services | Airflow only | Airflow + PostgreSQL |
| Portfolio level | Beginner | More realistic |

## Portfolio Description

Built an end-to-end coffee shop sales ETL pipeline using Apache Airflow, Python, pandas, PostgreSQL, SQLAlchemy, and Docker. The pipeline extracts sales data from an Excel file, cleans and validates transaction records, loads the processed data into PostgreSQL, and generates automated business reports for daily sales, product categories, store locations, and top-selling products.

Short version:

End-to-end ETL pipeline using Airflow, Python, PostgreSQL, and Docker for automated coffee shop sales reporting.
