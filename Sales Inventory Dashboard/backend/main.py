from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import get_conn, init_db

app = FastAPI(title="Sales Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

@app.on_event("startup")
def _startup():
    with get_conn() as conn:
        init_db(conn)

@app.get("/api/sales_by_category")
def sales_by_category():
    with get_conn() as conn:
        rows = conn.execute("""
                            SELECT category, SUM(sales_30d) AS total
                            FROM items GROUP BY category ORDER BY category
                            """).fetchall()
    return [{"category": r["category"], "sales_30d": r["total"]} for r in rows]

@app.get("/api/low_stock")
def low_stock():
    with get_conn() as conn:
        rows = conn.execute("""
                            SELECT sku, name, category, on_hand, reorder_point
                            FROM items
                            WHERE on_hand <= reorder_point
                            ORDER BY on_hand ASC
                                LIMIT 50
                            """).fetchall()
    keys = ["sku","name","category","on_hand","reorder_point"]
    return [dict(zip(keys, r)) for r in rows]

@app.get("/api/inventory_summary")
def inventory_summary():
    with get_conn() as conn:
        rows = conn.execute("""
                            SELECT category,
                                   SUM(on_hand) AS on_hand,
                                   SUM(reorder_point) AS reorder_total
                            FROM items GROUP BY category
                            """).fetchall()
    return [dict(r) for r in rows]

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63343",
        "http://127.0.0.1:63343",
        "http://localhost:8000",      # optional
        "http://127.0.0.1:8000",      # optional
        "*"                           # easiest while developing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)