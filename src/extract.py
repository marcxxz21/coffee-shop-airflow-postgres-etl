import pandas as pd

from utils.config import RAW_EXCEL_FILE, EXTRACTED_CSV_FILE
from utils.helpers import write_csv_file


def extract_sales_data() -> None:
    if not RAW_EXCEL_FILE.exists():
        raise FileNotFoundError(f"Raw Excel file not found: {RAW_EXCEL_FILE}")

    df = pd.read_excel(RAW_EXCEL_FILE)
    write_csv_file(df, EXTRACTED_CSV_FILE)

    print("Extraction complete.")
    print(f"Rows extracted: {len(df)}")
    print(f"Output file: {EXTRACTED_CSV_FILE}")


if __name__ == "__main__":
    extract_sales_data()