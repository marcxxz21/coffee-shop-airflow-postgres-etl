# Coffee Shop Sales ETL Dashboard

End-to-end coffee shop sales data pipeline built with Apache Airflow, Python, pandas, PostgreSQL, SQLAlchemy, Docker, and a public sales dashboard.

The pipeline extracts transaction data from Excel, cleans and validates the records, loads the processed data into PostgreSQL, generates CSV business reports, and publishes a professional online dashboard for sales performance analysis.

## Live Dashboard

[View the dashboard](https://coffeeshopetl.vercel.app)

The public dashboard is a deployed static sales snapshot, so it stays available even when local Docker, Airflow, and PostgreSQL are not running.

## GitHub Repository

[marcxxz21/coffee-shop-airflow-postgres-etl](https://github.com/marcxxz21/coffee-shop-airflow-postgres-etl)

## Dashboard Highlights

- Total sales, transaction volume, items sold, and average order value
- Daily revenue performance
- Revenue by product category
- Store revenue comparison
- Best-selling products
- Transaction detail sample
- Store and category filters

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
- Vercel
- JavaScript, HTML, and CSS for the public static dashboard

## Architecture

```text
coffee_shop_sales.xlsx
    -> Airflow DAG
    -> Python ETL scripts
    -> PostgreSQL sales table
    -> CSV reports
    -> Static dashboard snapshot
    -> Vercel public dashboard
```

Airflow and PostgreSQL run locally with Docker for the ETL workflow. The deployed Vercel dashboard uses a generated snapshot of the cleaned sales data, which makes the public dashboard independent from the local Docker database.

## Project Structure

```text
coffee_shop_etl/
├── dags/
│   └── coffee_sales_dag.py
├── dashboard/
│   └── app.py
├── online_dashboard/
│   ├── app.js
│   ├── data.json
│   ├── index.html
│   └── styles.css
├── tools/
│   └── build_static_dashboard_data.mjs
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
├── package.json
├── requirements.txt
├── vercel.json
├── .streamlit/
│   └── secrets.toml.example
├── .env.example
├── .gitignore
└── README.md
```

## ETL Pipeline Steps

1. Extract sales data from `data/raw/coffee_shop_sales.xlsx`.
2. Standardize column names and clean text fields.
3. Convert dates, times, numeric fields, and sales totals.
4. Remove invalid rows and duplicate transaction IDs.
5. Validate required fields, positive values, unique transactions, and total amount calculations.
6. Load cleaned records into PostgreSQL table `sales`.
7. Generate CSV reports by date, category, store, and product.
8. Build a static dashboard data snapshot for online hosting.

## Reports

The ETL creates these reports in `data/reports/`:

- `daily_sales_report.csv`
- `category_sales_report.csv`
- `store_sales_report.csv`
- `top_products_report.csv`

## Local Setup

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

For Neon or another cloud PostgreSQL database, set:

```env
POSTGRES_SSLMODE=require
```

## Run the ETL With Docker

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

## Run the Static Dashboard Locally

Build the dashboard snapshot:

```bash
npm run build
```

Serve the generated files from `dist/`:

```bash
python3 -m http.server 4173 --directory dist
```

Open:

```text
http://localhost:4173
```

## Deploy the Static Dashboard

The production dashboard is deployed to Vercel:

[https://coffeeshopetl.vercel.app](https://coffeeshopetl.vercel.app)

The Vercel build uses:

```bash
npm run build
```

and serves the generated `dist/` directory.

## Optional Streamlit Dashboard

The repo also includes a Streamlit dashboard at:

```text
dashboard/app.py
```

For local testing against Docker PostgreSQL:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

For a live Streamlit deployment, use Neon PostgreSQL and Streamlit Community Cloud.

## Streamlit Secrets

Copy:

```text
.streamlit/secrets.toml.example
```

Create:

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

Built an end-to-end coffee shop sales data pipeline using Apache Airflow, Python, pandas, PostgreSQL, SQLAlchemy, Docker, and Vercel. The Airflow pipeline extracts Excel sales data, cleans and validates transaction records, loads the processed data into PostgreSQL, and generates CSV business reports. A public dashboard visualizes revenue trends, product category performance, store performance, and best-selling products.

Short version:

End-to-end coffee shop sales ETL pipeline using Airflow, Python, PostgreSQL, Docker, and a public Vercel dashboard.
