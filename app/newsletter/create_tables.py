import json
import os
import argparse
from pathlib import Path

from peewee import PostgresqlDatabase


def load_pg_credentials():
    secrets_path = Path(__file__).resolve().parents[2] / ".secrets" / "render_pg_connect"
    with secrets_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_schema_and_table(db: PostgresqlDatabase, drop=False):
    schema_sql = """
    CREATE SCHEMA IF NOT EXISTS newsletter_dev;
    """
    drop_table_sql = """
    DROP TABLE IF EXISTS newsletter_dev.snippet CASCADE;
    """
    table_sql = """
    CREATE TABLE IF NOT EXISTS newsletter_dev.snippet (
        id SERIAL PRIMARY KEY,
        uuid VARCHAR(36) NOT NULL UNIQUE,
        project VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        approval_state INTEGER NOT NULL DEFAULT 0,
        added_ts INTEGER NOT NULL,
        deleted INTEGER NOT NULL DEFAULT 0,
        published VARCHAR(255),
        published_ts INTEGER
    );
    """
    with db.connection_context():
        db.execute_sql(schema_sql)
        if drop:
            db.execute_sql(drop_table_sql)
            print("Dropped table 'newsletter_dev.snippet' (if it existed).")
        db.execute_sql(table_sql)


def main():
    parser = argparse.ArgumentParser(description='Create newsletter_dev schema and snippet table')
    parser.add_argument('--drop', action='store_true', help='Drop existing tables before creating')
    args = parser.parse_args()
    
    creds = load_pg_credentials()
    db = PostgresqlDatabase(
        database=creds["dbname"],
        user=creds["user"],
        password=creds["password"],
        host=creds["host"],
    )
    ensure_schema_and_table(db, drop=args.drop)
    print("Schema 'newsletter_dev' and table 'snippet' ensured.")


if __name__ == "__main__":
    main()


