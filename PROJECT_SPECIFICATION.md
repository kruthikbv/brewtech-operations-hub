# BrewTech Operations Hub

## 1. Project Overview
**Project Name:** BrewTech Operations Hub

A full-stack operations management application for managing clients, machines, machine assignments, service records, inventory, inventory transactions, dashboards, analytics, and Excel import/export.

### Primary Objective
Demonstrate:
- Python backend development
- Django and Django REST Framework
- PostgreSQL and database design
- REST APIs and JWT authentication
- Django ORM
- Streamlit dashboards
- Pandas data handling
- Excel import/export
- Plotly visualization

### Out of Scope
Do not add AI, ML, GenAI, prediction, forecasting, chatbots, automated reporting, complex multi-tenancy, or payment systems.

---

## 2. Technology Stack
### Backend
- Python 3.12+
- Django
- Django REST Framework
- Django ORM
- PostgreSQL

### Authentication
- Django Authentication
- SimpleJWT

### Frontend
- Streamlit

### Supporting Tools
- Pandas
- OpenPyXL
- Plotly
- django-filter
- drf-spectacular
- python-dotenv
- Git and GitHub

---

## 3. Architecture

```text
USER
  |
  v
STREAMLIT
Operations UI / Dashboard / Analytics
  |
  | HTTP REST API + JWT
  v
DJANGO + DJANGO REST FRAMEWORK
Business Logic / Validation / Authentication
  |
  v
DJANGO ORM
  |
  v
POSTGRESQL
```

**Critical Rule:** Streamlit must never connect directly to PostgreSQL.

All data communication follows:

`Streamlit -> Django REST API -> Django ORM -> PostgreSQL`

---

## 4. Root Structure

```text
brewtech-operations-hub/
├── backend/
├── frontend/
├── sample_data/
├── docs/
├── PROJECT_SPECIFICATION.md
├── COPILOT_MASTER_PROMPT.md
├── README.md
├── .gitignore
└── docker-compose.yml
```

Docker is optional and must not block local development.

---

## 5. Backend Structure

```text
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── clients/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── tests.py
├── machines/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── tests.py
├── service_records/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── tests.py
├── inventory/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── tests.py
├── activity_logs/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
├── dashboard/
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── common/
    ├── constants.py
    ├── exceptions.py
    ├── pagination.py
    ├── permissions.py
    └── utils.py
```

---

## 6. Frontend Structure

```text
frontend/
├── app.py
├── requirements.txt
├── .env.example
├── api_client/
│   ├── base_client.py
│   ├── auth_client.py
│   ├── clients_client.py
│   ├── machines_client.py
│   ├── services_client.py
│   ├── inventory_client.py
│   └── dashboard_client.py
├── auth/
│   └── auth_manager.py
├── pages/
│   ├── dashboard.py
│   ├── clients.py
│   ├── machines.py
│   ├── assignments.py
│   ├── service_management.py
│   ├── inventory.py
│   ├── analytics.py
│   └── data_management.py
└── utils/
    ├── constants.py
    ├── formatters.py
    ├── validators.py
    └── excel_handler.py
```

---

## 7. Canonical Naming Rules

### IDs
```python
client_id
machine_id
assignment_id
service_record_id
inventory_item_id
inventory_transaction_id
activity_log_id
```

### Booleans
```python
is_authenticated
is_active
is_low_stock
has_active_assignment
is_loading
is_valid
```

### Collections
```python
clients
machines
assignments
service_records
inventory_items
inventory_transactions
activity_logs
```

### Service Functions
```python
create_client()
update_client()
deactivate_client()
create_machine()
update_machine()
assign_machine()
return_machine()
create_service_record()
update_service_record()
create_inventory_item()
record_stock_in()
record_stock_out()
```

Do not randomly rename equivalent concepts.

---

# 8. Database Design

Use PostgreSQL. All timestamps should use timezone-aware Django fields.

## 9. Accounts
Use Django's built-in User model. Do not create a custom user model.

Fields used:
- username
- password
- first_name
- last_name
- email
- is_active
- is_staff

---

## 10. Client Model

Application: `clients`
Model: `Client`

Fields:
- id: BigAutoField, primary key
- client_code: CharField, unique
- client_name: CharField, required
- contact_person: CharField, optional
- phone_number: CharField, optional
- email: EmailField, optional
- address: TextField, optional
- city: CharField, optional
- status: CharField
- created_at: DateTimeField
- updated_at: DateTimeField

Statuses:
- ACTIVE
- INACTIVE

Indexes:
- client_code
- client_name
- status

---

## 11. Machine Model

Application: `machines`
Model: `Machine`

Fields:
- id: BigAutoField
- machine_code: CharField, unique
- machine_model: CharField
- serial_number: CharField, unique
- purchase_date: DateField
- status: CharField
- created_at: DateTimeField
- updated_at: DateTimeField

Statuses:
- AVAILABLE
- DEPLOYED
- UNDER_SERVICE
- INACTIVE

Indexes:
- machine_code
- serial_number
- status

---

## 12. MachineAssignment Model

Application: `machines`
Model: `MachineAssignment`

Fields:
- id: BigAutoField
- machine: ForeignKey Machine
- client: ForeignKey Client
- assigned_date: DateField
- returned_date: DateField, nullable
- assignment_status: CharField
- notes: TextField, optional
- created_at: DateTimeField
- updated_at: DateTimeField

Relationships:
- machine: `related_name="assignments"`
- client: `related_name="machine_assignments"`
- use `on_delete=models.PROTECT`

Statuses:
- ACTIVE
- RETURNED

Business Rules:
1. Only AVAILABLE machines can be assigned.
2. One machine can have only one ACTIVE assignment.
3. Creating an assignment changes machine status to DEPLOYED.
4. Returning a machine sets returned_date, sets assignment_status to RETURNED, and changes machine status to AVAILABLE.
5. Use `transaction.atomic()` for assignment and return.
6. Add a PostgreSQL conditional UniqueConstraint for one ACTIVE assignment per machine.

---

## 13. ServiceRecord Model

Application: `service_records`
Model: `ServiceRecord`

Fields:
- id: BigAutoField
- machine: ForeignKey Machine
- service_date: DateField
- service_type: CharField
- technician_name: CharField
- description: TextField
- status: CharField
- previous_machine_status: CharField, nullable/blank as appropriate
- created_at: DateTimeField
- updated_at: DateTimeField

Relationship:
- `related_name="service_records"`
- `on_delete=models.PROTECT`

Service Types:
- ROUTINE_SERVICE
- CLEANING
- REPAIR
- INSPECTION

Statuses:
- SCHEDULED
- IN_PROGRESS
- COMPLETED
- CANCELLED

Rules:
- SCHEDULED does not change machine status.
- IN_PROGRESS stores previous operational status and sets machine to UNDER_SERVICE.
- COMPLETED restores previous_machine_status.
- Keep previous_machine_status for history.
- CANCELLED must not incorrectly corrupt machine status.
- Use service-layer logic and transactions.

---

## 14. InventoryItem Model

Application: `inventory`
Model: `InventoryItem`

Fields:
- id: BigAutoField
- item_code: CharField, unique
- item_name: CharField
- category: CharField
- current_quantity: DecimalField
- unit: CharField
- minimum_stock_level: DecimalField
- created_at: DateTimeField
- updated_at: DateTimeField

Categories:
- BEVERAGE_INGREDIENT
- CONSUMABLE
- MACHINE_SUPPLY
- CLEANING_SUPPLY
- OTHER

Constraints:
- current_quantity >= 0
- minimum_stock_level >= 0

Indexes:
- item_code
- item_name
- category

---

## 15. InventoryTransaction Model

Model: `InventoryTransaction`

Fields:
- id: BigAutoField
- inventory_item: ForeignKey
- transaction_type: CharField
- quantity: DecimalField
- transaction_date: DateField
- remarks: TextField
- created_at: DateTimeField

Relationship:
- `related_name="transactions"`
- `on_delete=models.PROTECT`

Transaction Types:
- STOCK_IN
- STOCK_OUT

Rules:
- STOCK_IN increases current_quantity.
- STOCK_OUT decreases current_quantity.
- Quantity must never become negative.
- Reject stock-out when requested quantity exceeds current quantity.
- Use `transaction.atomic()` and `select_for_update()` where appropriate.

---

## 16. ActivityLog Model

Application: `activity_logs`
Model: `ActivityLog`

Fields:
- id: BigAutoField
- user: ForeignKey User
- action_type: CharField
- entity_type: CharField
- entity_id: BigIntegerField
- description: TextField
- created_at: DateTimeField

Action types:
- CREATE
- UPDATE
- DEACTIVATE
- ASSIGN
- RETURN
- SERVICE_CREATE
- SERVICE_UPDATE
- STOCK_IN
- STOCK_OUT
- IMPORT

Use:
- `related_name="activity_logs"`
- `on_delete=models.SET_NULL`
- `null=True`

Examples:
- Created client CLT-0001
- Assigned machine MCH-0005 to CLT-0002
- Recorded stock in for INV-0003

---

# 17. Database Relationship Summary

```text
USER
 |
 +-- * ACTIVITY_LOG

CLIENT
 |
 +-- * MACHINE_ASSIGNMENT * -- 1 MACHINE
                              |
                              +-- * SERVICE_RECORD

INVENTORY_ITEM
 |
 +-- * INVENTORY_TRANSACTION
```

---

# 18. REST API

Base URL: `/api/v1/`

## Authentication
- POST `/api/v1/auth/login/`
- POST `/api/v1/auth/refresh/`
- GET `/api/v1/auth/me/`

Login request:
```json
{
  "username": "admin",
  "password": "password"
}
```

Login response:
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

## Clients
- GET `/api/v1/clients/`
- POST `/api/v1/clients/`
- GET `/api/v1/clients/{id}/`
- PATCH `/api/v1/clients/{id}/`

Do not physically delete clients. Set status to INACTIVE.

Filtering:
- status
- city

Search:
- client_code
- client_name
- contact_person

## Machines
- GET `/api/v1/machines/`
- POST `/api/v1/machines/`
- GET `/api/v1/machines/{id}/`
- PATCH `/api/v1/machines/{id}/`

Filtering:
- status
- machine_model

Search:
- machine_code
- serial_number
- machine_model

## Assignments
- GET `/api/v1/assignments/`
- POST `/api/v1/assignments/`
- POST `/api/v1/assignments/{id}/return/`

Assignment request:
```json
{
  "machine_id": 1,
  "client_id": 2,
  "assigned_date": "2026-08-30",
  "notes": "Initial deployment"
}
```

Return request:
```json
{
  "returned_date": "2026-09-15",
  "notes": "Returned after contract completion"
}
```

## Service Records
- GET `/api/v1/service-records/`
- POST `/api/v1/service-records/`
- GET `/api/v1/service-records/{id}/`
- PATCH `/api/v1/service-records/{id}/`

Filtering:
- machine
- service_type
- status
- service_date

## Inventory
- GET `/api/v1/inventory/`
- POST `/api/v1/inventory/`
- GET `/api/v1/inventory/{id}/`
- PATCH `/api/v1/inventory/{id}/`
- POST `/api/v1/inventory/{id}/stock-in/`
- POST `/api/v1/inventory/{id}/stock-out/`
- GET `/api/v1/inventory/{id}/transactions/`

## Dashboard
- GET `/api/v1/dashboard/summary/`
- GET `/api/v1/dashboard/recent-activity/`

Summary includes:
- total_clients
- active_clients
- total_machines
- available_machines
- deployed_machines
- machines_under_service
- low_stock_items

## Analytics
- `/api/v1/analytics/machine-status/`
- `/api/v1/analytics/machines-per-client/`
- `/api/v1/analytics/service-activity/`
- `/api/v1/analytics/inventory-overview/`

Backend should perform reasonable aggregations rather than forcing Streamlit to calculate everything.

---

# 19. DRF Rules

Use `ModelSerializer` and `ModelViewSet` for:
- Clients
- Machines
- Inventory
- Service Records

Use `@action` or `APIView` for:
- Machine return
- Stock in
- Stock out
- Dashboard summaries
- Analytics

All operational APIs require `IsAuthenticated`.

---

# 20. Pagination and Filtering

Create `StandardPagination`:
- page_size = 10
- max_page_size = 100

Use:
- django-filter
- DjangoFilterBackend
- SearchFilter
- OrderingFilter

---

# 21. API Documentation

Use drf-spectacular.

Provide:
- `/api/schema/`
- `/api/docs/`

Swagger UI must work.

---

# 22. Streamlit Authentication

Use:
```python
st.session_state.is_authenticated
st.session_state.access_token
st.session_state.refresh_token
st.session_state.current_user
```

Flow:

`Username + Password -> Django Login API -> JWT -> Session State -> Application`

Logout clears all authentication state.

Protected requests must include:

`Authorization: Bearer <access_token>`

---

# 23. Streamlit Pages

## Dashboard
KPI cards:
- Total Clients
- Active Clients
- Total Machines
- Available Machines
- Deployed Machines
- Machines Under Service
- Low Stock Items

Plotly charts:
- Machine Status Distribution
- Machines Per Client
- Service Activity
- Inventory Overview

Display latest 10 activities.

## Clients
- List
- Search
- Filter
- Pagination
- Add
- Edit
- Deactivate
- View details

## Machines
- List
- Search
- Filter
- Add
- Edit
- View status
- Assignment history
- Service history

## Assignments
- Show only AVAILABLE machines for assignment.
- Show only ACTIVE clients.
- Return active assignments.
- Display assignment history.

## Service Management
- Create service record
- Update status
- Filter
- View history
- Confirm machine impact when changing to IN_PROGRESS

## Inventory
- List
- Search
- Category filter
- Add item
- Stock in
- Stock out
- Transaction history
- Highlight low stock

Low stock:
`current_quantity <= minimum_stock_level`

## Analytics
Machine:
- Status distribution
- Machines per client

Service:
- Activity over time
- Type distribution

Inventory:
- Current stock by category
- Low stock items

Use Plotly. No ML or forecasting.

## Data Management
- Excel import
- Excel export

Imports:
- Clients
- Machines
- Inventory Items

Do not initially bulk-import assignments.

---

# 24. Excel Import

### Client Columns
- client_code
- client_name
- contact_person
- phone_number
- email
- address
- city
- status

### Machine Columns
- machine_code
- machine_model
- serial_number
- purchase_date
- status

Initial import statuses allowed:
- AVAILABLE
- INACTIVE

Do not import DEPLOYED or UNDER_SERVICE.

### Inventory Columns
- item_code
- item_name
- category
- current_quantity
- unit
- minimum_stock_level

Flow:

`Upload -> Pandas -> Column Validation -> Type Validation -> Required Validation -> Duplicate Check -> Preview -> Confirmation -> Backend API -> PostgreSQL`

Backend must validate again.

---

# 25. Export

Allow export for:
- Clients
- Machines
- Assignments
- Service Records
- Inventory
- Inventory Transactions

Flow:

`Backend JSON -> Pandas DataFrame -> Excel`

Use `BytesIO`.

---

# 26. Business Logic Location

Do not put critical logic in Streamlit.

Use backend service layers:

`API -> Service Layer -> Database`

Examples:
- `machines/services.py`: assign_machine(), return_machine()
- `inventory/services.py`: record_stock_in(), record_stock_out()

---

# 27. Transaction Requirements

Use `transaction.atomic()` for:

### Machine Assignment
Create Assignment + Update Machine + Activity Log

### Machine Return
Update Assignment + Update Machine + Activity Log

### Stock In
Create Transaction + Update Quantity + Activity Log

### Stock Out
Create Transaction + Update Quantity + Activity Log

All must succeed or all must roll back.

---

# 28. Error Handling

Use meaningful API errors.

Example:
```json
{
  "detail": "Machine is not available for assignment."
}
```

Do not expose raw database exceptions.

Use correct HTTP status codes:
- 200
- 201
- 400
- 401
- 403
- 404
- 409
- 500

---

# 29. Dependencies

Backend:
- Django
- djangorestframework
- djangorestframework-simplejwt
- django-filter
- drf-spectacular
- psycopg
- python-dotenv

Frontend:
- streamlit
- requests
- pandas
- plotly
- openpyxl
- python-dotenv

Pin compatible versions.

---

# 30. Environment Variables

## Backend
```text
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
POSTGRES_DB=brewtech_db
POSTGRES_USER=brewtech_user
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

## Frontend
```text
BACKEND_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Never commit `.env`. Provide `.env.example`.

---

# 31. PostgreSQL Learning Documentation

Create:
`docs/postgresql_learning_queries.md`

Include examples for:
- JOIN
- LEFT JOIN
- GROUP BY
- HAVING
- Indexes
- EXPLAIN ANALYZE
- Transactions

Example:
```sql
SELECT
    m.machine_code,
    c.client_name,
    ma.assigned_date
FROM machines_machineassignment ma
JOIN machines_machine m
    ON ma.machine_id = m.id
JOIN clients_client c
    ON ma.client_id = c.id
WHERE ma.assignment_status = 'ACTIVE';
```

Clearly label these as learning queries.

Create:
`docs/database_indexes.md`

Explain each index and why it exists. Do not add unnecessary indexes.

---

# 32. Testing

Minimum tests:

### Clients
- Create
- Update
- Deactivate
- Duplicate code rejected

### Machines
- Create
- Duplicate code rejected

### Assignments
- Assign available machine
- Reject unavailable machine
- Reject duplicate active assignment
- Return machine
- Verify status after return

### Inventory
- Stock in
- Stock out
- Prevent negative inventory

### Authentication
- Login
- Protected endpoint
- Reject unauthenticated request

Use isolated test data.

---

# 33. Demo Data

All demo data must be:
- Synthetic
- Fictional
- Non-confidential

Generate approximately:
- 15 Clients
- 40 Machines
- 20 Active Assignments
- 10 Historical Assignments
- 25 Service Records
- 15 Inventory Items
- 50 Inventory Transactions

Create:
`python manage.py seed_demo_data`

It must:
- Avoid duplicates
- Be safe to run repeatedly
- Clearly identify demo data

---

# 34. Django Admin

Register all major models.

Add:
- list displays
- search fields
- filters

Use Django Admin for debugging and data inspection.

---

# 35. README

Include:
- Project Overview
- Architecture
- Features
- Technology Stack
- Simplified Folder Structure
- PostgreSQL Setup
- Backend Setup
- Frontend Setup
- API Documentation
- Demo Data statement
- Screenshot placeholders

Setup must cover:
- Virtual environment
- Requirements installation
- `.env`
- Migrations
- Superuser
- Demo data
- Django startup
- Streamlit startup

State clearly:

> All included data is synthetic and created for demonstration purposes.

---

# 36. Code Quality

Backend:
- PEP 8
- Clear naming
- Type hints where useful
- Small functions
- No duplicated business logic

Frontend:
- Reusable API client
- Consistent error handling
- No direct database access

---

# 37. Things Not To Do

Do not add:
- AI
- ML
- Forecasting
- Unnecessary microservices
- Redis
- Celery
- Kafka
- Kubernetes
- Complex RBAC
- Unnecessary Docker complexity

---

# 38. Final Acceptance Criteria

## Backend
- PostgreSQL works
- Migrations work
- JWT works
- Protected APIs work
- CRUD works
- Assignment logic works
- Service logic works
- Inventory transactions work
- Activity logs work
- Filtering and pagination work
- Swagger works

## Frontend
- Login works
- Dashboard works
- Management pages work
- Charts work
- Import works
- Export works
- Errors are user-friendly

## Database
- Relationships work
- Constraints work
- Indexes exist
- Transactions prevent inconsistent data

## Repository
- README complete
- `.env` excluded
- Demo data included
- Tests included
- No confidential organization data
