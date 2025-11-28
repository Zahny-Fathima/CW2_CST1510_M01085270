import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

# Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")
def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    
    This is a COMPLETE IMPLEMENTATION as an example.
    Study this carefully before implementing the other tables!
    
    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()
    
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("Users table created successfully!")