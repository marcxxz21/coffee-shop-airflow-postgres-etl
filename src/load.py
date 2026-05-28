from datetime import datetime

from utils.config import CLEAN_CSV_FILE, DATABASE_URL
from utils.helpers import get_database_engine, read_csv_file


def load_sales_data() -> None:
    df = read_csv_file(CLEAN_CSV_FILE)

    df["loaded_at"] = datetime.now()

    engine = get_database_engine(DATABASE_URL)

    with engine.begin() as connection:
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False,
            method="multi",
        )

    print("Loading complete.")
    print(f"Rows loaded: {len(df)}")
    print("Table created: sales")


if __name__ == "__main__":
    load_sales_data()