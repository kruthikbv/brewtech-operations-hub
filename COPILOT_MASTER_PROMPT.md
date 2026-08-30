# GitHub Copilot Master Implementation Prompt

You are the lead software architect and senior full-stack Python developer.

Your task is to implement the complete project described in:

`PROJECT_SPECIFICATION.md`

Project name:

**BrewTech Operations Hub**

## IMPORTANT

Read `PROJECT_SPECIFICATION.md` completely before generating or modifying code.

Treat it as the single source of truth.

Do not invent alternative architectures.

Do not rename canonical models, fields, API paths, functions, folders, or variables unless technically necessary. If a change is required, keep naming consistent across the entire project.

---

## ARCHITECTURE

Frontend: Streamlit
Backend: Django
REST API: Django REST Framework
Authentication: Django Authentication + JWT using SimpleJWT
ORM: Django ORM
Database: PostgreSQL
Data Handling: Pandas
Excel: OpenPyXL
Visualization: Plotly
Filtering: django-filter
API Documentation: drf-spectacular

Architecture:

`Streamlit -> Django REST API -> Django Business Logic -> Django ORM -> PostgreSQL`

### Critical Rule
Streamlit must never directly connect to PostgreSQL.

---

## IMPLEMENTATION STRATEGY

Implement the entire repository structure.

Do not merely provide code snippets.

Create actual files with complete implementations.

Before moving to another module, ensure imports and dependencies are consistent.

At the end, perform a consistency review across:
- models
- migrations
- serializers
- views
- URLs
- service functions
- API clients
- Streamlit pages
- environment variables
- requirements

---

## BACKEND

Create the Django backend exactly as specified.

Implement applications:
- accounts
- clients
- machines
- service_records
- inventory
- activity_logs
- dashboard
- common

Use Django's built-in User model.

Do not create a custom user model.

Use PostgreSQL and environment variables.

Create `backend/.env.example`.

Never hardcode credentials.

---

## DJANGO REST FRAMEWORK

Use:
- ModelSerializer
- ModelViewSet

for standard CRUD.

Use custom actions or APIViews for business operations.

Implement:
- Authentication
- Permissions
- Pagination
- Filtering
- Search
- Ordering

All operational endpoints require `IsAuthenticated`.

Use JWT.

---

## DATABASE

Implement all models exactly according to `PROJECT_SPECIFICATION.md`.

Important models:
- Client
- Machine
- MachineAssignment
- ServiceRecord
- InventoryItem
- InventoryTransaction
- ActivityLog

Implement:
- foreign keys
- related_name values
- constraints
- indexes
- validation

Use conditional unique constraints where specified.

Use `transaction.atomic()` for operations modifying multiple records.

Use `select_for_update()` where required for inventory safety.

---

## BUSINESS LOGIC

### Machine Assignment
Only AVAILABLE machines can be assigned.

A machine can only have one ACTIVE assignment.

Assignment must:
1. Create assignment
2. Change machine status to DEPLOYED
3. Create activity log

All operations must occur atomically.

### Machine Return
Must:
1. Set returned_date
2. Set assignment status to RETURNED
3. Change machine status to AVAILABLE
4. Create activity log

All operations must occur atomically.

### Inventory

Stock in:
1. Lock inventory row
2. Increase quantity
3. Create transaction
4. Create activity log

Stock out:
1. Lock inventory row
2. Verify sufficient quantity
3. Decrease quantity
4. Create transaction
5. Create activity log

Never allow negative inventory.

---

## SERVICE MANAGEMENT

Implement `previous_machine_status` correctly.

When service becomes IN_PROGRESS:
- Set machine status to UNDER_SERVICE.
- Store previous operational machine status.

When service becomes COMPLETED:
- Restore previous machine status.

Do not corrupt assignment history.

Use transactions where required.

---

## ACTIVITY LOGGING

Automatically log important operations.

Logging must occur in the backend service layer.

Do not depend on Streamlit to create activity logs.

---

## API CONTRACT

Use API paths exactly as specified.

Base:

`/api/v1/`

Implement:
- Authentication
- Clients
- Machines
- Assignments
- Service Records
- Inventory
- Dashboard
- Analytics

Use consistent JSON field names and meaningful validation errors.

---

## STREAMLIT

Implement the complete frontend.

Use `requests` for API communication.

Create reusable API client modules.

Do not duplicate HTTP request code across pages.

Use:
```python
st.session_state.is_authenticated
st.session_state.access_token
st.session_state.refresh_token
st.session_state.current_user
```

Implement login and logout.

Protected requests must include:

`Authorization: Bearer <access_token>`

---

## STREAMLIT PAGES

Implement:
- Dashboard
- Clients
- Machines
- Assignments
- Service Management
- Inventory
- Analytics
- Data Management

Use clear forms and tables.

Validate input before API requests.

Show user-friendly success and error messages.

Do not expose raw Python tracebacks to normal users.

---

## DASHBOARD

Implement KPI cards:
- Total Clients
- Active Clients
- Total Machines
- Available Machines
- Deployed Machines
- Machines Under Service
- Low Stock Items

Implement Plotly charts:
- Machine Status Distribution
- Machines Per Client
- Service Activity
- Inventory Overview

Implement Recent Activity.

---

## EXCEL

Implement import and export.

Imports:
- Clients
- Machines
- Inventory Items

Use Pandas.

Validate:
- required columns
- data types
- required fields
- duplicate rows
- invalid values

Show preview before submission.

Backend must validate again.

Exports:
- Clients
- Machines
- Assignments
- Service Records
- Inventory
- Inventory Transactions

Generate Excel in memory using `BytesIO`.

---

## API DOCUMENTATION

Use drf-spectacular.

Implement:
- `/api/schema/`
- `/api/docs/`

Swagger must work.

---

## TESTING

Implement meaningful backend tests for:
- Authentication
- Client creation
- Duplicate clients
- Machine creation
- Machine assignment
- Duplicate assignment prevention
- Machine return
- Stock in
- Stock out
- Negative inventory prevention

Use isolated test data.

---

## DEMO DATA

Create:

`python manage.py seed_demo_data`

Generate only synthetic data.

Make it safe to run repeatedly.

Do not use real company names or confidential information.

---

## DOCUMENTATION

Create:
- `README.md`
- `docs/postgresql_learning_queries.md`
- `docs/database_indexes.md`

Document setup clearly.

---

## DEPENDENCY MANAGEMENT

Create separate requirements files for:
- backend
- frontend

Pin compatible versions.

Do not add unnecessary dependencies.

---

## FINAL REVIEW

After implementation:

1. Review all imports.
2. Review all URL paths.
3. Check serializer field names against models.
4. Check API clients against API responses.
5. Check Streamlit pages against API endpoints.
6. Check environment variable names.
7. Check requirements.
8. Check PostgreSQL configuration.
9. Check migration generation.
10. Check tests.
11. Check README setup instructions.

Fix inconsistencies before declaring implementation complete.

Do not stop after creating skeleton files.

Implement working functionality.

When an implementation detail is ambiguous, choose the simplest solution consistent with `PROJECT_SPECIFICATION.md`.

Avoid unnecessary abstractions and enterprise complexity.

The result must be a clean, understandable, portfolio-quality full-stack application.
