from __future__ import annotations
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "inventory.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items(
  sku            TEXT PRIMARY KEY,
  name           TEXT NOT NULL,
  category       TEXT NOT NULL,
  on_hand        INTEGER NOT NULL,
  reorder_point  INTEGER NOT NULL,
  unit_cost      REAL NOT NULL,
  unit_price     REAL NOT NULL,
  sales_30d      INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sales(
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  sku       TEXT NOT NULL,
  qty       INTEGER NOT NULL,
  ts        TEXT NOT NULL,
  FOREIGN KEY(sku) REFERENCES items(sku) ON DELETE CASCADE
);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()