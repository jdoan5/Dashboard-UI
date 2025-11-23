from __future__ import annotations
from datetime import datetime, timedelta
import random
from .db import get_conn, init_db

def seed_items():
    return [
        ("SKU001","Widget A","Gadgets", 12, 10, 2.50,  5.00, 120),
        ("SKU002","Widget B","Gadgets",  4, 10, 3.00,  6.50,  75),
        ("SKU003","Cable C" ,"Cables",  30, 20, 1.20,  3.99, 210),
        ("SKU004","Case D"  ,"Cases",   15,  8, 4.00, 12.00,  40),
        ("SKU005","Dock E"  ,"Docks",    2,  6, 8.00, 19.00,  18),
    ]

def seed_sales():
    now = datetime.utcnow()
    rows = []
    for sku, *_ in seed_items():
        for _ in range(20):
            when = now - timedelta(days=random.randint(0, 29))
            rows.append((sku, random.randint(1, 5), when.isoformat(timespec="seconds")))
    return rows

def main():
    with get_conn() as conn:
        init_db(conn)
        conn.execute("DELETE FROM sales")
        conn.execute("DELETE FROM items")

        conn.executemany("""
                         INSERT INTO items (sku,name,category,on_hand,reorder_point,unit_cost,unit_price,sales_30d)
                         VALUES (?,?,?,?,?,?,?,?)
                         """, seed_items())

        conn.executemany("""
                         INSERT INTO sales (sku,qty,ts) VALUES (?,?,?)
                         """, seed_sales())

        conn.commit()

if __name__ == "__main__":
    main()