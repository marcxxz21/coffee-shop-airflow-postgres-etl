from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


def ensure_directory_exists(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)


def read_csv_file(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def write_csv_file(df: pd.DataFrame, file_path: Path) -> None:
    ensure_directory_exists(file_path.parent)
    df.to_csv(file_path, index=False)


def get_database_engine(database_url: str):
    return create_engine(database_url)