# UK Property Management & Compliance Tracker (Django MVP)

A simple Django app to manage UK rental properties, tenancies, and compliance certificates/documents.

## Features

- Property, Tenancy, ComplianceRecord, and Document models.
- File uploads for compliance evidence (PDF/images/etc.).
- Dashboard with compliance status buckets:
  - **Overdue**
  - **Due Soon (<= 30 days)**
  - **OK**
- Basic UI pages for properties, tenancies, and compliance records.
- CSV export endpoints for properties, tenancies, and compliance status.
- Weekly digest management command for due/overdue items.
- Sample data management command.
- SQLite by default (Windows-friendly).

---

## Tech Requirements

- Python **3.11+**
- Django **5+**
- SQLite (bundled with Python)

---

## Quick Start (Windows PowerShell)

From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .

# Create DB schema
python manage.py migrate

# (Optional) load sample data
python manage.py seed_sample_data

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Open:
- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Useful Commands

### Run tests (due-soon/overdue logic)

```powershell
python manage.py test properties
```

### Send weekly digest (manual for now)

```powershell
python manage.py send_weekly_digest --to you@example.com
```

If `--to` is omitted, the command uses `ADMINS` in settings.

### CSV exports

While server is running:

- `/export/properties/`
- `/export/tenancies/`
- `/export/compliance/`

---

## Data Model (MVP)

- `Property`: address, postcode, bedrooms, landlord.
- `Tenancy`: linked to property, tenant, term dates, rent, deposit.
- `ComplianceRecord`: linked to property, certificate type (Gas Safety, EICR, EPC, etc.), issue/expiry dates.
- `Document`: file upload linked to a compliance record.

Compliance status is calculated from `expiry_date`:
- **Overdue**: expired already.
- **Due Soon**: expires in next 30 days.
- **OK**: expiry is more than 30 days away.

---

## Notes

- Media uploads are stored under `media/` in development.
- Email backend is console by default in settings (safe for local development).
