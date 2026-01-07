"""
Database layer for AfriLens AI.
Handles SQLite connection and schema management with auto-upgrade capability.
"""
import sqlite3
import os
from pathlib import Path
from typing import Optional
from contextlib import contextmanager
from datetime import datetime


DB_PATH = Path(__file__).parent.parent / "afrilens.db"


def get_db_path() -> Path:
    """Return the database file path."""
    return DB_PATH


@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize database schema."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Receipts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                image_path TEXT NOT NULL,
                vendor_name TEXT,
                transaction_date TEXT,
                total_amount REAL,
                currency TEXT DEFAULT 'KES',
                trust_score INTEGER DEFAULT 0,
                flags TEXT,  -- JSON array of flag strings
                raw_ocr_text TEXT,
                extracted_data TEXT,  -- JSON of structured data
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Line items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS line_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                description TEXT,
                quantity REAL,
                unit_price REAL,
                total_price REAL,
                line_number INTEGER,
                FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_receipts_date ON receipts(transaction_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_receipts_vendor ON receipts(vendor_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_line_items_receipt ON line_items(receipt_id)")


def upgrade_database():
    """Auto-upgrade database schema if needed."""
    # Future-proofing: check schema version and apply migrations
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if schema_version table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='schema_version'
        """)
        
        if not cursor.fetchone():
            # First time setup
            cursor.execute("""
                CREATE TABLE schema_version (
                    version INTEGER PRIMARY KEY
                )
            """)
            cursor.execute("INSERT INTO schema_version (version) VALUES (1)")
        
        # Future migrations would go here
        # Example: if version < 2: apply migration_2()


if __name__ == "__main__":
    # Initialize database on direct execution
    init_database()
    upgrade_database()
    print(f"Database initialized at: {DB_PATH}")
