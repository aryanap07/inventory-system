<div align="center">

# StockFlow

**A cloud-connected CLI inventory system for small workshops**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-f59e0b?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.1-ef4444?style=flat-square)

</div>

---

## What is StockFlow?

StockFlow is a command-line inventory system built for small workshops and spare-parts environments. It replaces paper registers and messy spreadsheets with a structured digital workflow — logging every stock movement against a live cloud database, so your inventory is always accurate and always accessible.

The focus is on **reliability and simplicity**: clean input validation, no silent failures, and a stock calculation that is always derived from the full movement history rather than a mutable counter.

---

## How it works

```
python main.py
```

```
==================================================
               STOCKFLOW
        Inventory Management CLI
==================================================

Dashboard

1) Add Inward Stock
2) Add Outward Stock
3) Check Stock
4) Exit
```

- **Inward** — Select a distributor and part (with autocomplete), enter quantity. Saved to `inward_log`.
- **Outward** — Select a customer and part, enter quantity. Live stock is checked before the entry is accepted — you cannot dispatch more than what's available.
- **Check Stock** — Look up any part by ID. Stock level is calculated in real time as `total inward − total outward`.
- Type `cancel` at any prompt to return to the dashboard.

---

## Project Structure

```
inventory-system/
│
├── main.py                       # Entry point
│
├── employee/
│   ├── employee_dashboard.py     # CLI menu and navigation
│   ├── add_inward.py             # Record incoming stock
│   └── add_outward.py            # Record outgoing stock
│
├── inventory/
│   ├── stock_service.py          # Stock calculation logic
│   └── check_stock.py            # Stock lookup interface
│
├── services/
│   ├── supabase_client.py        # Shared Supabase connection
│   └── .env.example              # Environment variable template
│
├── requirements.txt
└── .gitignore
```

---

## Tech Stack

| | |
|---|---|
| Language | Python 3.10+ |
| Database | Supabase (PostgreSQL) |
| DB Client | supabase-py 2.7.0 |
| CLI Input | prompt-toolkit 3.0.43 |
| Config | python-dotenv 1.0.1 |

---

## Database Schema

| Table | Columns | Purpose |
|---|---|---|
| `parts_master` | `part_id`, `part_name` | Master list of all parts |
| `distributor_list` | `distributors` | Approved distributor names |
| `inward_log` | `part_id`, `quantity`, `distributor` | Goods received |
| `outward_log` | `part_id`, `quantity`, `customer` | Goods dispatched |

> Stock is never stored directly. It is always computed as `Σ inward − Σ outward` for a given `part_id`.

---

## Setup

### 1. Clone

```bash
git clone https://github.com/aryanap07/inventory-system.git
cd inventory-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp services/.env.example services/.env
```

Open `services/.env` and add your Supabase credentials:

```env
URL="your_supabase_project_url"
KEY="your_supabase_anon_key"
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 4. Run

```bash
python main.py
```

---

## Design Decisions

**Stock as a derived value** — Rather than maintaining a stock count column and updating it on every transaction, stock is always computed from the movement logs. This makes the data auditable, prevents inconsistencies from failed updates, and means every transaction is a permanent record.

**Validation before write** — Part IDs, distributor names, and quantities are all validated against the database before any insert is attempted. The system will not write a record it cannot verify.

**Lazy imports in the dashboard** — Each module (`add_inward`, `add_outward`, `check_stock`) is imported only when the user selects that option, keeping startup time minimal and avoiding unnecessary DB connections.

---

## Changelog

| Version | Highlights |
|---|---|
| v1.1 | Added `main.py` entry point, wrapped dashboard in `run()`, fixed null quantity crash, added `.gitignore` and `.env.example` |
| v1.0 | Initial release — inward/outward logging, live stock check, Supabase integration, autocomplete inputs |

---

<div align="center">

Built by [Aryan Patel](https://github.com/aryanap07) · For learning and demonstration purposes only

</div>
