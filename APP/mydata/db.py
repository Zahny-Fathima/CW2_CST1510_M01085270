import sqlite3
from pathlib import Path
import pandas as pd

# ----------------------------
# DATA DIRECTORY (REQUIRED)
# ----------------------------
# This path points to the DATA folder at the project root
DATA_DIR = Path(__file__).resolve().parent.parent / "mydata"

# ----------------------------
# DATABASE PATH
# ----------------------------
DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))

# ----------------------------
# CSV LOADING FUNCTION
# ----------------------------
def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a table using pandas.
    Drops CSV 'id' column if it exists.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        print("CSV file not found:", csv_path)
        return 0
    
    df = pd.read_csv(csv_path)

    # Drop id column if it exists (SQLite auto-handles IDs)
    if 'id' in df.columns:
        print(f"Dropping 'id' column from CSV for table '{table_name}'...")
        df = df.drop(columns=['id'])

    df.to_sql(
        name=table_name,
        con=conn,
        if_exists='append',
        index=False
    )

    print(f"Loaded {len(df)} rows into '{table_name}'")
    return len(df)
