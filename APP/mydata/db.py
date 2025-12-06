import sqlite3
from pathlib import Path

DB_Path=Path('mydata')/"intelligence_platform.db"

def connect_database(db_path=DB_Path):
    return sqlite3.connect(str(db_path))