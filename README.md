# BrewTech Operations Hub

A portfolio-grade operations system for clients, coffee machines, assignments, service records, inventory, dashboards, analytics, and Excel workflows.

## Architecture

`Streamlit -> Django REST Framework -> Django ORM -> PostgreSQL`

The frontend never connects directly to PostgreSQL. PostgreSQL is used when `POSTGRES_PASSWORD` is configured; local development falls back to SQLite for a quick start.

## Features

JWT authentication, protected CRUD APIs, transactional assignment and inventory operations, machine service status transitions, activity logs, filtering/search/pagination, Swagger documentation, Streamlit dashboard navigation, Pandas/OpenPyXL import helpers, Plotly-ready analytics endpoints, and repeatable synthetic demo data.

## Setup

### PostgreSQL

Set a password and start the optional local PostgreSQL container:

```powershell
$env:POSTGRES_PASSWORD = 'choose-a-local-password'
docker compose up -d db
```

Copy that password into `backend/.env`. If `POSTGRES_PASSWORD` is omitted, development uses SQLite; PostgreSQL remains the deployment database.

### Application

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt -r frontend/requirements.txt
copy backend/.env.example backend/.env
python backend/manage.py migrate
python backend/manage.py createsuperuser
python backend/manage.py seed_demo_data
python backend/manage.py runserver
```

Run the frontend in another terminal:

```powershell
copy frontend/.env.example frontend/.env
.venv\Scripts\streamlit.exe run frontend/app.py
```

API documentation is available at `/api/docs/` and the schema at `/api/schema/`. Docker PostgreSQL is optional via `docker compose up -d db`.

The repeatable demo account is `demo_admin` with password `demo-password`. Change this credential outside local demonstrations.

Run the backend tests with:

```powershell
python backend/manage.py test clients machines inventory service_records accounts dashboard
```

All included data is synthetic and created for demonstration purposes.

## Structure

- `backend/`: Django, DRF, domain services, migrations, and tests
- `frontend/`: Streamlit application and HTTP API clients
- `docs/`: PostgreSQL learning queries and index rationale
- `sample_data/`: place for import templates and examples

## Screenshots

_Add dashboard and operations screenshots here._
