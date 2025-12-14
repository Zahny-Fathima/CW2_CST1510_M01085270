import pandas as pd
from app.mydata.db import connect_database


def insert_ticket(conn, ticket_id, status, category, subject, description, created_date, assigned_to=None):
    """Insert new IT ticket."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets 
        (ticket_id, status, category, subject, descripton, created_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, status, category, subject, description, created_date, assigned_to))
    conn.commit()
    id = cursor.lastrowid
    return id


def get_all_tickets(conn):
    """Get all IT tickets as DataFrame."""
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    return df


def update_ticket_status(conn, ticket_id, new_status):
    """Update the status of a ticket."""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (new_status, ticket_id))
    conn.commit()
    affected_rows = cursor.rowcount
    return affected_rows


def resolve_ticket(conn, ticket_id, resolved_date):
    """Resolve a ticket by setting status and resolved date."""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets
        SET status = 'Resolved', resolved_date = ?
        WHERE ticket_id = ?
    """, (resolved_date, ticket_id))
    conn.commit()
    affected_rows = cursor.rowcount
    return affected_rows


def delete_ticket(conn, ticket_id):
    """Delete a ticket by ticket_id."""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM it_tickets
        WHERE ticket_id = ?
    """, (ticket_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    return affected_rows


def get_tickets_by_category_count(conn):
    """
    Count tickets by category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM it_tickets
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_tickets_by_status(conn):
    """
    Count tickets by status.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_unresolved_tickets(conn):
    """
    Get all unresolved tickets.
    Uses: SELECT, FROM, WHERE, ORDER BY
    """
    query = """
    SELECT *
    FROM it_tickets
    WHERE status != 'Resolved'
    ORDER BY created_date DESC
    """
    df = pd.read_sql_query(query, conn)
    return df