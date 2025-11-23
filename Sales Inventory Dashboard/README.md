# Sales & Inventory Insights Dashboard

A responsive **Sales & Inventory Insights Dashboard** that visualizes key business metrics with a clean, card-based UI and a Python + DuckDB backend.

This project is developed and managed in **IntelliJ IDEA Ultimate**, using it as a full-stack environment for:

- Frontend: Dashboard UI (HTML/CSS/JS + charts)
- Backend: Python API powered by DuckDB and CSV data

---

## Overview

The dashboard is designed to answer questions such as:

- Which products and categories are driving revenue?
- How do sales trends change over time?
- What is the breakdown by channel (Online vs Store)?
- Which items may be low on stock?

Although it has a data backend, this is primarily a **Dashboard & UI project**: the focus is on presenting data clearly, interactively, and accessibly.

---

## Features

- 🧩 **Dashboard UI**
    - KPI cards: Total Revenue, Orders, Average Order Value, Low Stock Items
    - Responsive layout suitable for desktop (and tablet-friendly)
    - Clean Bootstrap-style components (cards, modals, tables, badges)

- 📈 **Data Visualizations**
    - Revenue over time (daily/weekly/monthly)
    - Top categories / products by revenue or units sold
    - Channel breakdown (Online vs Store)
    - Filterable, sortable tables for detailed records

- 🗃️ **Data Backend (Support Layer)**
    - DuckDB mini data mart (e.g. `fact_sales`, `dim_product`, `dim_date`)
    - Data loaded from CSV files (synthetic or real)
    - Python API endpoints that serve JSON to the dashboard

> The UI and user experience are the main focus; the backend exists to support the dashboard.

---

## Tech Stack

**Frontend (Dashboard & UI)**
- HTML5, CSS3
- Bootstrap (or similar UI framework)
- JavaScript (vanilla)
- Charting library (e.g., Chart.js / similar)

**Backend (Data & API)**
- Python (Flask or FastAPI)
- DuckDB for analytics queries
- Pandas for data loading and aggregation
- CSV / JSON as input and export formats

**Development Environment**
- **IntelliJ IDEA Ultimate**
    - Python plugin for backend development
    - HTML/CSS/JS support for UI
    - Single project for both frontend and backend

---

## Architecture

```mermaid
graph TD
    U[User Browser] --> UI[Dashboard UI (HTML/CSS/JS)]
    UI --> API[Python API Backend]
    API --> DB[DuckDB Mini Data Mart]

    subgraph Data Layer
        DB --> F_FACT[fact_sales]
        DB --> D_PROD[dim_product]
        DB --> D_DATE[dim_date]
    end

    DB --> SRC[(CSV Data Sources)]
