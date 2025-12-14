import pandas as pd
from app.mydata.db import connect_database


def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert a new dataset metadata entry."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    dataset_id = cursor.lastrowid
    return dataset_id


def get_all_datasets(conn):
    """Return all datasets as DataFrame."""
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    return df


def update_dataset_records(conn, dataset_id, new_record_count):
    """Update the record count of a dataset."""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata
        SET record_count = ?
        WHERE id = ?
    """, (new_record_count, dataset_id))
    conn.commit()
    affected_rows = cursor.rowcount
    return affected_rows


def delete_dataset(conn, dataset_id):
    """Delete a dataset by ID."""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM datasets_metadata
        WHERE id = ?
    """, (dataset_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    return affected_rows


def get_datasets_by_category_count(conn):
    """
    Count datasets by category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_large_datasets(conn, min_size_mb=100):
    """
    Find datasets larger than min_size_mb.
    Uses: SELECT, FROM, WHERE, ORDER BY
    """
    query = """
    SELECT *
    FROM datasets_metadata
    WHERE file_size_mb > ?
    ORDER BY file_size_mb DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_size_mb,))
    return df


def get_total_storage_by_category(conn):
    """
    Calculate total storage used by each category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY, SUM
    """
    query = """
    SELECT category, SUM(file_size_mb) as total_size_mb, COUNT(*) as dataset_count
    FROM datasets_metadata
    GROUP BY category
    ORDER BY total_size_mb DESC
    """
    df = pd.read_sql_query(query, conn)
    return df