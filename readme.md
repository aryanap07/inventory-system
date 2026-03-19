<div align="center">

# StockFlow

**Cloud-connected CLI inventory system for small workshops**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-6366f1?style=flat-square)](#changelog)

StockFlow replaces paper registers and messy spreadsheets with a structured digital workflow — logging every stock movement against a live cloud database. Stock is always computed from the full movement history, never stored as a mutable counter, so the data stays auditable and consistent even if a write fails mid-operation.

[Quick Start](#quick-start) · [How It Works](#how-it-works) · [Project Structure](#project-structure) · [Database Schema](#database-schema) · [Design Decisions](#design-decisions) · [Changelog](#changelog)

</div>

---

## Prerequisites

- Python 3.10 or higher
- A [Supabase](https://supabase.com) account and project
- Your Supabase project URL and anon key (found under **Settings → API**)

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/aryanap07/inventory-system.git
cd inventory-system

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# macOS / Linux:
cp services/.env.example services/.env
# Windows:
copy services\.env.example services\.env

# 6. Open services/.env and add your Supabase credentials:
#    URL="your_supabase_project_url"
#    KEY="your_supabase_anon_key"

# 7. Run
python main.py
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### Alternative install — editable mode

If you plan to modify the source code, install in editable mode instead of step 4 above. Changes to the source take effect immediately without reinstalling:

```bash
pip install -e .
```

This reads `pyproject.toml` and symlinks the source directory into the virtual environment's `site-packages`.

---

## How It Works

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

**Inward stock** — Select a distributor and part using autocomplete, enter a quantity. The record is written to `inward_log`.

**Outward stock** — Select a customer and part, enter a quantity. Live stock is checked before the entry is accepted — you cannot dispatch more than what is currently available.

**Check stock** — Look up any part by ID. The stock level is computed in real time as `Σ inward − Σ outward` for that `part_id`.

Type `cancel` at any prompt to return to the dashboard without writing any record.

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
├── pyproject.toml
└── .gitignore
```

---

## Tech Stack

| Component | Technology |
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

## Design Decisions

**Stock as a derived value.** Rather than maintaining a count column and updating it on every transaction, stock is always computed from the movement logs. This makes every transaction a permanent record, prevents inconsistencies from failed updates, and means the full audit trail is always intact.

**Validation before write.** Part IDs, distributor names, and quantities are all validated against the database before any insert is attempted. The system will not write a record it cannot verify.

**Lazy imports in the dashboard.** Each module (`add_inward`, `add_outward`, `check_stock`) is imported only when the user selects that option. This keeps startup time minimal and avoids opening database connections until they are actually needed.

---

## Changelog

| Version | Highlights |
|---|---|
| v1.0.1 | Added `main.py` entry point, wrapped dashboard in `run()`, fixed null quantity crash, added `.gitignore` and `pyproject.toml` |
| v1.0 | Initial release — inward/outward logging, live stock check, Supabase integration, autocomplete inputs |

---

<div align="center">

Built by [Aryan Patel](https://github.com/aryanap07)

</div>