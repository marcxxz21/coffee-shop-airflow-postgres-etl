import os
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

REPORTS_DIR = BASE_DIR / "data" / "reports"

RAW_EXCEL_FILE = RAW_DATA_DIR / "coffee_shop_sales.xlsx"

EXTRACTED_CSV_FILE = PROCESSED_DATA_DIR / "extracted_sales.csv"

CLEAN_CSV_FILE = PROCESSED_DATA_DIR / "clean_sales.csv"

POSTGRES_USER = os.getenv("POSTGRES_USER", "coffee_user")

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "coffee_password")

POSTGRES_DB = os.getenv("POSTGRES_DB", "coffee_sales_db")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")

POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "prefer")

DATABASE_URL = (

    f"postgresql+psycopg2://{quote_plus(POSTGRES_USER)}:"

    f"{quote_plus(POSTGRES_PASSWORD)}@{POSTGRES_HOST}:"

    f"{POSTGRES_PORT}/{quote_plus(POSTGRES_DB)}"

    f"?sslmode={quote_plus(POSTGRES_SSLMODE)}"

)
