import pandas as pd

from utils.config import EXTRACTED_CSV_FILE, CLEAN_CSV_FILE
from utils.helpers import read_csv_file, write_csv_file


REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "transaction_time",
    "transaction_qty",
    "store_id",
    "store_location",
    "product_id",
    "unit_price",
    "product_category",
    "product_type",
    "product_detail",
]


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df


def check_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    text_columns = [
        "store_location",
        "product_category",
        "product_type",
        "product_detail",
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce",
    )

    df["transaction_time"] = pd.to_datetime(
        df["transaction_time"],
        format="%H:%M:%S",
        errors="coerce",
    ).dt.time

    numeric_columns = [
        "transaction_id",
        "transaction_qty",
        "store_id",
        "product_id",
        "unit_price",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.dropna(
        subset=[
            "transaction_id",
            "transaction_date",
            "transaction_qty",
            "store_id",
            "store_location",
            "product_id",
            "unit_price",
            "product_category",
            "product_type",
            "product_detail",
        ]
    )

    df = df[df["transaction_qty"] > 0]
    df = df[df["unit_price"] > 0]

    return df


def add_business_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["total_amount"] = (df["transaction_qty"] * df["unit_price"]).round(2)
    df["year"] = df["transaction_date"].dt.year
    df["month"] = df["transaction_date"].dt.month
    df["day"] = df["transaction_date"].dt.day
    df["day_name"] = df["transaction_date"].dt.day_name()

    return df


def transform_sales_data() -> None:
    df = read_csv_file(EXTRACTED_CSV_FILE)

    df = standardize_column_names(df)
    check_required_columns(df)
    df = clean_text_columns(df)
    df = convert_data_types(df)
    df = remove_invalid_rows(df)
    df = df.drop_duplicates(subset=["transaction_id"])
    df = add_business_columns(df)

    write_csv_file(df, CLEAN_CSV_FILE)

    print("Transformation complete.")
    print(f"Rows after cleaning: {len(df)}")
    print(f"Output file: {CLEAN_CSV_FILE}")


if __name__ == "__main__":
    transform_sales_data()
