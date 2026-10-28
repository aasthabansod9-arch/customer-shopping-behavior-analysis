"""Load the cleaned dataset into PostgreSQL (table: customer).

Usage:
    cp .env.example .env   # then edit credentials
    python scripts/load_to_db.py
"""
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
database = os.getenv("DB_NAME", "customer_behavior")

df = pd.read_csv(ROOT / "data" / "processed" / "customer_shopping_behavior_clean.csv")

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
df.to_sql("customer", engine, if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into '{database}.customer'.")
