"""
SQLite helpers for the conservation tracker.
The database file lives at db/conservation.db.
"""

import json
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "conservation.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create all tables if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS species (
            taxonid         INTEGER PRIMARY KEY,
            scientific_name TEXT NOT NULL,
            kingdom         TEXT,
            phylum          TEXT,
            class           TEXT,
            "order"         TEXT,
            family          TEXT,
            genus           TEXT,
            category        TEXT,   -- current Red List category
            population_trend TEXT,
            marine_system   INTEGER,
            freshwater_system INTEGER,
            terrestrial_system INTEGER
        );

        CREATE TABLE IF NOT EXISTS assessments (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            taxonid         INTEGER NOT NULL,
            scientific_name TEXT,
            category        TEXT,
            assessment_date TEXT,
            FOREIGN KEY (taxonid) REFERENCES species(taxonid)
        );

        CREATE TABLE IF NOT EXISTS threats (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            taxonid         INTEGER NOT NULL,
            threat_code     TEXT,
            threat_title    TEXT,
            FOREIGN KEY (taxonid) REFERENCES species(taxonid)
        );

        CREATE TABLE IF NOT EXISTS occurrences (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            taxon_key       INTEGER,
            scientific_name TEXT,
            country_code    TEXT,
            latitude        REAL,
            longitude       REAL,
            year            INTEGER
        );
    """)

    conn.commit()
    conn.close()
    print(f"Database ready at {DB_PATH}")


def df_to_table(df: pd.DataFrame, table: str, if_exists="append"):
    """Write a DataFrame to a SQLite table.
    Any columns containing lists or dicts are automatically converted to JSON strings,
    since SQLite can only store simple types like text and numbers.
    """
    conn = get_connection()
    df = df.copy()
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].apply(json.dumps)
    df.to_sql(table, conn, if_exists=if_exists, index=False)
    conn.close()


def query(sql: str, params=()) -> pd.DataFrame:
    """Run a SQL query and return a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df
