import pandas as pd

from utils.config import DATABASE_URL, REPORTS_DIR
from utils.helpers import get_database_engine, write_csv_file


REPORT_QUERIES = {
    "daily_sales_report.csv": """
        SELECT 
            transaction_date,
            ROUND(SUM(total_amount)::numeric, 2) AS total_sales,
            SUM(transaction_qty) AS total_items_sold,
            COUNT(transaction_id) AS total_transactions
        FROM sales
        GROUP BY transaction_date
        ORDER BY transaction_date;
    """,
    "category_sales_report.csv": """
        SELECT 
            product_category,
            ROUND(SUM(total_amount)::numeric, 2) AS total_sales,
            SUM(transaction_qty) AS total_items_sold,
            COUNT(transaction_id) AS total_transactions
        FROM sales
        GROUP BY product_category
        ORDER BY total_sales DESC;
    """,
    "store_sales_report.csv": """
        SELECT 
            store_location,
            ROUND(SUM(total_amount)::numeric, 2) AS total_sales,
            SUM(transaction_qty) AS total_items_sold,
            COUNT(transaction_id) AS total_transactions
        FROM sales
        GROUP BY store_location
        ORDER BY total_sales DESC;
    """,
    "top_products_report.csv": """
        SELECT 
            product_detail,
            product_category,
            product_type,
            ROUND(SUM(total_amount)::numeric, 2) AS total_sales,
            SUM(transaction_qty) AS total_items_sold
        FROM sales
        GROUP BY product_detail, product_category, product_type
        ORDER BY total_sales DESC
        LIMIT 20;
    """,
}


def export_query_to_csv(query: str, output_file_name: str) -> None:
    engine = get_database_engine(DATABASE_URL)

    with engine.begin() as connection:
        df = pd.read_sql_query(query, connection)

    output_path = REPORTS_DIR / output_file_name
    write_csv_file(df, output_path)

    print(f"Created report: {output_path}")


def create_sales_reports() -> None:
    for output_file_name, query in REPORT_QUERIES.items():
        export_query_to_csv(query, output_file_name)

    print("All reports created.")


if __name__ == "__main__":
    create_sales_reports()