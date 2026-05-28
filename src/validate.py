import pandas as pd

from utils.config import CLEAN_CSV_FILE
from utils.helpers import read_csv_file


def validate_no_nulls(df: pd.DataFrame, columns: list[str]) -> list[str]:
    failed_checks = []

    for column in columns:
        if df[column].isna().any():
            failed_checks.append(f"{column}_has_null_values")

    return failed_checks


def validate_positive_values(df: pd.DataFrame) -> list[str]:
    failed_checks = []

    if not (df["transaction_qty"] > 0).all():
        failed_checks.append("transaction_qty_must_be_positive")

    if not (df["unit_price"] > 0).all():
        failed_checks.append("unit_price_must_be_positive")

    return failed_checks


def validate_unique_transaction_id(df: pd.DataFrame) -> list[str]:
    if not df["transaction_id"].is_unique:
        return ["transaction_id_must_be_unique"]

    return []


def validate_total_amount(df: pd.DataFrame) -> list[str]:
    expected_total = (df["transaction_qty"] * df["unit_price"]).round(2)
    actual_total = df["total_amount"].round(2)

    if not actual_total.eq(expected_total).all():
        return ["total_amount_calculation_is_invalid"]

    return []


def validate_sales_data() -> None:
    df = read_csv_file(CLEAN_CSV_FILE)

    required_non_null_columns = [
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
        "total_amount",
    ]

    failed_checks = []
    failed_checks.extend(validate_no_nulls(df, required_non_null_columns))
    failed_checks.extend(validate_positive_values(df))
    failed_checks.extend(validate_unique_transaction_id(df))
    failed_checks.extend(validate_total_amount(df))

    if failed_checks:
        raise ValueError(f"Data validation failed: {failed_checks}")

    print("Validation complete. All checks passed.")


if __name__ == "__main__":
    validate_sales_data()
