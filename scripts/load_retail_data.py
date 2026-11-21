
import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"

# Parent tables must be loaded before dependent tables.
TABLES = [
    "customers",
    "stores",
    "products",
    "employees",
    "orders",
    "order_items",
]

def load_table(conn, table_name):
    file_path = DATA_DIR / f"{table_name}.csv"

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.reader(file)
        columns = next(reader)

        column_sql = ", ".join(
            f'"{column}"' for column in columns
        )

        copy_sql = (
            f"COPY retail.{table_name} "
            f"({column_sql}) FROM STDIN"
        )

        with conn.cursor() as cur:
            # COPY into a temporary staging table so
            # repeat runs do not violate primary keys.
            cur.execute(
                f"CREATE TEMP TABLE stage_{table_name} "
                f"(LIKE retail.{table_name} "
                f"INCLUDING DEFAULTS) ON COMMIT DROP"
            )

            stage_sql = copy_sql.replace(
                f"retail.{table_name}",
                f"stage_{table_name}"
            )

            with cur.copy(stage_sql) as copy:
                for row in reader:
                    cleaned_row = [
                        value if value != "" else None
                        for value in row
                    ]
                    copy.write_row(cleaned_row)

            # Insert only records not already present.
            # Existing records are intentionally unchanged.
            cur.execute(
                f"INSERT INTO retail.{table_name} "
                f"SELECT * FROM stage_{table_name} "
                f"ON CONFLICT DO NOTHING"
            )

            print(
                f"Loaded {table_name}: "
                f"{cur.rowcount} new rows"
            )

def main():
    conn_info = {
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }

    with psycopg.connect(**conn_info) as conn:
        with conn.transaction():
            for table in TABLES:
                load_table(conn, table)

    print("Historical ingestion completed successfully.")

if __name__ == "__main__":
    main()
