# Coffee Shop Airflow PostgreSQL ETL

This project is an end-to-end coffee shop sales ETL pipeline built with Apache Airflow, Python, pandas, PostgreSQL, SQLAlchemy, Docker, and Streamlit.

The pipeline extracts transaction data from an Excel file, cleans and validates the records, loads the processed data into a PostgreSQL database, generates automated sales reports, and powers a Streamlit dashboard for revenue, product, and store analysis.

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
- Streamlit
- Plotly
- Neon PostgreSQL

## Project Structure

```text
coffee_shop_etl/
├── dags/
│   └── coffee_sales_dag.py
├── dashboard/
│   └── app.py
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
├── .streamlit/
│   └── secrets.toml.example
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
6. Visualize the loaded data in the Streamlit dashboard.

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
POSTGRES_SSLMODE=prefer
```

For Neon or another cloud PostgreSQL database, set `POSTGRES_SSLMODE=require`.

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

## Streamlit Dashboard

The dashboard is located at:

```text
dashboard/app.py
```

For local dashboard testing against your Docker PostgreSQL database, keep Docker running and run:

```bash
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

For online deployment, use Neon PostgreSQL and Streamlit Community Cloud.

## Streamlit Secrets

Copy the example secrets file:

```text
.streamlit/secrets.toml.example
```

Create a local file named:

```text
.streamlit/secrets.toml
```

Use your Neon database values:

```toml
[postgres]
host = "your_neon_host"
port = 5432
database = "your_neon_database"
user = "your_neon_user"
password = "your_neon_password"
sslmode = "require"
```

The real `.streamlit/secrets.toml` file is ignored by Git.

## Online Deployment

Recommended portfolio architecture:

```text
coffee_shop_sales.xlsx
    -> Airflow ETL pipeline
    -> Neon PostgreSQL
    -> Streamlit dashboard
    -> Public Streamlit app link
```

Deployment steps:

1. Create a Neon PostgreSQL database.
2. Update `.env` with Neon connection values and `POSTGRES_SSLMODE=require`.
3. Run the Airflow DAG locally to load the `sales` table into Neon.
4. Push this project to GitHub.
5. Deploy `dashboard/app.py` from Streamlit Community Cloud.
6. Add the same `[postgres]` secrets in the Streamlit app settings.
7. Redeploy the app and copy the public dashboard link.

The Airflow pipeline can stay local for this beginner portfolio. The dashboard is online because it reads from the cloud PostgreSQL database.

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

Built an end-to-end coffee shop sales data pipeline using Apache Airflow, Python, pandas, PostgreSQL, Docker, and Streamlit. The Airflow pipeline extracts and cleans Excel sales data, validates the records, and loads the processed data into PostgreSQL. A Streamlit dashboard visualizes sales trends, product performance, store performance, and top-selling products.

Short version:

End-to-end ETL pipeline using Airflow, Python, PostgreSQL, Docker, and Streamlit for automated coffee shop sales reporting.
