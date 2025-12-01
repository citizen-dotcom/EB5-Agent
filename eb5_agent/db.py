# Purpose: Database helper functions for fetching and updating case data.
import sqlite3
from typing import List, Dict, Tuple, Optional

def connect(db_path: str) -> sqlite3.Connection:
    """Open a SQLite connection with row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_transactions(conn: sqlite3.Connection, case_id: str) -> List[Dict]:
    """Get all transactions for a case, ordered by date."""
    q = "SELECT * FROM transactions WHERE case_id=? ORDER BY date ASC"
    return [dict(r) for r in conn.execute(q, [case_id]).fetchall()]

def fetch_assets(conn: sqlite3.Connection, case_id: str) -> List[Dict]:
    """Get all assets (properties, businesses, etc.) for a case."""
    q = "SELECT * FROM assets WHERE case_id=?"
    return [dict(r) for r in conn.execute(q, [case_id]).fetchall()]

def fetch_passport_name(conn: sqlite3.Connection, case_id: str) -> Tuple[Optional[str], Optional[str]]:
    """Return passport name and doc_id if already indexed for a case."""
    q = "SELECT name, doc_id FROM passports WHERE case_id=?"
    row = conn.execute(q, [case_id]).fetchone()
    return (row["name"], row["doc_id"]) if row and row["name"] else (None, None)

def upsert_passport_name(conn: sqlite3.Connection, case_id: str, name: str, doc_id: str = None, storage_uri: str = None, ocr_text: str = None):
    """Insert or update passport name for a case (used after OCR fallback)."""
    conn.execute("""
        INSERT INTO passports (case_id, name, doc_id, storage_uri, ocr_text)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(case_id) DO UPDATE SET name=excluded.name, doc_id=excluded.doc_id,
        storage_uri=excluded.storage_uri, ocr_text=excluded.ocr_text
    """, (case_id, name, doc_id, storage_uri, ocr_text))
    conn.commit()