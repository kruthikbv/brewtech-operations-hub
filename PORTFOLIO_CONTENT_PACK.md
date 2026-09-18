# BrewTech Operations Hub - Portfolio Content Pack

## Accuracy Note

BrewTech Operations Hub is a self-directed portfolio project built around a fictional beverage-machine operations company. Describe it as a portfolio project, case study, or simulated business solution unless BrewTech was your actual employer or client. Do not present fictional employment as real work experience.

## One-Line Summary

Designed and developed a full-stack operations management platform using Django REST Framework, PostgreSQL, JWT, and Streamlit to manage clients, machine deployments, service records, inventory, analytics, and Excel data workflows.

## Resume Project Entry

### BrewTech Operations Hub | Full-Stack Python Developer

**Technology:** Python, Django, Django REST Framework, PostgreSQL, Streamlit, Pandas, Plotly, JWT, Docker, GitHub Actions

- Architected a full-stack operations platform covering client management, a 40-machine fleet, deployment history, maintenance workflows, inventory transactions, analytics, and Excel import/export.
- Built authenticated REST APIs with Django REST Framework and SimpleJWT, including filtering, search, pagination, OpenAPI documentation, and reusable Streamlit API clients.
- Implemented atomic assignment, return, service-status, stock-in, and stock-out workflows using Django transactions, row locking, database constraints, and backend activity logging.
- Designed a normalized PostgreSQL schema with protected relationships, conditional uniqueness, nonnegative inventory checks, indexes, migrations, and repeatable fictional demo data.
- Created a responsive Streamlit operations interface with KPI dashboards, Plotly visualizations, management forms, low-stock indicators, and spreadsheet validation workflows.
- Containerized PostgreSQL, Django/Gunicorn, and Streamlit; added production security settings and PostgreSQL-backed GitHub Actions CI for migrations, tests, OpenAPI, and source validation.

**Repository:** https://github.com/kruthikbv/brewtech-operations-hub

## Compact Resume Version

- Developed a Django REST Framework, PostgreSQL, and Streamlit operations platform for machine deployments, service management, inventory, dashboards, analytics, and Excel workflows.
- Protected multi-record operations with atomic transactions, row locking, database constraints, JWT authentication, and activity logs; validated the system through automated PostgreSQL CI.
- Delivered responsive Plotly dashboards, Docker deployment images, Swagger documentation, realistic fictional demo data, and 14 automated backend tests.

## LinkedIn Project Entry

### BrewTech Operations Hub

Built a portfolio-grade operations management application for a fictional beverage-machine services company. The platform manages clients, equipment, machine assignments and returns, service history, inventory movements, dashboards, analytics, and Excel imports/exports.

I designed the backend with Django, Django REST Framework, and PostgreSQL, using JWT authentication and a service-layer architecture for critical business operations. Machine deployments, returns, service transitions, and stock movements run inside database transactions, with row locking and constraints protecting data consistency.

The Streamlit interface provides a responsive operations workspace with management forms, KPI cards, low-stock visibility, Plotly charts, and reusable API clients. I also added Swagger/OpenAPI documentation, realistic fictional Bengaluru-based demo data, Docker images for the full stack, production security configuration, and PostgreSQL-backed GitHub Actions CI.

**Technology:** Python, Django, Django REST Framework, PostgreSQL, Streamlit, Pandas, Plotly, SimpleJWT, OpenPyXL, Docker, Gunicorn, GitHub Actions

**GitHub:** https://github.com/kruthikbv/brewtech-operations-hub

## LinkedIn Post

I recently completed BrewTech Operations Hub, a full-stack Python portfolio project that simulates the operational needs of a beverage-machine services company.

The system brings together client management, machine deployments, assignment and return history, service workflows, inventory control, activity tracking, dashboards, analytics, and Excel data exchange.

Key engineering work included:

- Django REST Framework APIs secured with JWT
- PostgreSQL relationships, indexes, constraints, and migrations
- Atomic assignment and inventory workflows with row locking
- Machine-status restoration across service transitions
- Responsive Streamlit management screens and Plotly dashboards
- Pandas and OpenPyXL import/export workflows
- Dockerized PostgreSQL, Django/Gunicorn, and Streamlit services
- PostgreSQL-backed GitHub Actions CI

The project uses a fictional Bengaluru-oriented dataset covering December 2023 through October 2024.

Repository: https://github.com/kruthikbv/brewtech-operations-hub

#Python #Django #PostgreSQL #Streamlit #Docker #RESTAPI #DataEngineering #FullStackDevelopment

## Portfolio Website Case Study

### Overview

BrewTech Operations Hub is a full-stack operations platform created for a fictional company that deploys and services beverage machines across client workplaces. It replaces disconnected operational records with one authenticated system for clients, machines, deployments, service work, inventory, analytics, and spreadsheet exchange.

### Problem

Machine operations involve linked processes: only available equipment should be assigned, each machine can have only one active deployment, service activity must preserve its previous operating state, and inventory must never become negative. These rules need enforcement at the backend and database layers rather than only in the user interface.

### Solution

I built a Django REST Framework backend backed by PostgreSQL and exposed it to a Streamlit operations interface through JWT-protected REST APIs. Critical workflows use a dedicated service layer, atomic transactions, row-level locks, conditional uniqueness, check constraints, and activity logs.

The interface supports daily operational work through searchable tables, forms, status filters, machine and service history, inventory movements, KPI cards, Plotly analytics, and validated Excel imports and exports.

### Key Engineering Decisions

- Kept Streamlit fully separated from PostgreSQL through a REST API boundary.
- Located critical business rules in backend service functions instead of UI code.
- Used `transaction.atomic()` and `select_for_update()` for concurrent stock and machine operations.
- Added database constraints as a final defense for active assignments and nonnegative inventory.
- Preserved a machine's previous state during service so completion or cancellation restores it correctly.
- Used backend aggregations for dashboard and analytics responses.
- Created deterministic, repeatable fictional demo data for portfolio demonstrations.
- Added Docker images and hosted CI to verify production configuration against PostgreSQL.

### Outcome

The result is a working portfolio application with authenticated management workflows, transactional data integrity, responsive operational dashboards, documented APIs, Docker deployment support, and automated CI validation.

## Interview Walkthrough

### 30-Second Version

I built BrewTech Operations Hub to demonstrate full-stack Python engineering around a realistic operations domain. Django REST Framework and PostgreSQL enforce the business rules, while Streamlit provides the management UI. The most important part was protecting linked workflows such as machine assignment, service-state changes, and stock movement with transactions, locks, and database constraints. I then containerized the stack and added PostgreSQL-backed CI.

### Two-Minute Version

The application models clients, machines, machine assignments, service records, inventory items, inventory transactions, users, and activity logs. The frontend never accesses PostgreSQL directly; every interaction goes through JWT-authenticated REST APIs.

For assignments, the service layer locks the machine, verifies that it is available and the client is active, creates the assignment, updates the machine to deployed, and records an activity log in one transaction. Returns reverse that workflow atomically. Inventory uses row locking to prevent concurrent stock-outs from creating negative balances. Service records preserve the previous machine state and restore it when work is completed or cancelled.

The Streamlit UI provides operational forms, filtering, history views, inventory alerts, Excel workflows, and Plotly dashboards. The repository includes migrations, Swagger documentation, Docker images, production security settings, realistic fictional demo data, and GitHub Actions that tests against PostgreSQL.

## STAR Story

**Situation:** A machine-service operation needs consistent records across clients, deployed equipment, maintenance, and warehouse stock. Spreadsheet-only tracking makes linked status changes and inventory consistency difficult to protect.

**Task:** Design a portfolio-quality full-stack system that centralizes these workflows and demonstrates reliable backend engineering, database design, analytics, and deployment practices.

**Action:** I modeled the domain in Django and PostgreSQL, built JWT-protected REST APIs, separated business rules into transactional service functions, added row locks and database constraints, and developed a responsive Streamlit interface with analytics and Excel exchange. I also containerized the stack and created PostgreSQL-backed CI.

**Result:** Delivered a reproducible operations platform with working management workflows, protected data integrity, documented APIs, realistic demonstration data, automated tests, Docker deployment support, and a public GitHub release.

## Technical Highlights

- **Architecture:** Streamlit -> REST API -> Django service layer -> Django ORM -> PostgreSQL
- **Authentication:** Django users and SimpleJWT access/refresh tokens
- **Data integrity:** Atomic transactions, row-level locking, protected foreign keys, unique and check constraints
- **API:** ViewSets, serializers, filtering, search, ordering, pagination, custom actions, Swagger/OpenAPI
- **Analytics:** Backend aggregations visualized with Plotly
- **Data exchange:** Pandas validation and OpenPyXL Excel generation
- **Delivery:** Docker Compose, Gunicorn, WhiteNoise, GitHub Actions, release tagging
- **Quality:** 14 backend tests plus migration, OpenAPI, production configuration, and compilation checks

## Suggested Portfolio Metadata

**Project type:** Full-stack operations management application

**Role:** Full-Stack Python Developer / Software Engineer

**Duration:** Use the actual period during which you built the project. Do not use the fictional demo-data dates as employment dates.

**Skills:** Python, Django, Django REST Framework, PostgreSQL, SQL, Streamlit, Pandas, Plotly, REST APIs, JWT, Docker, GitHub Actions, Database Design, Transaction Management, Excel Automation

## Recruiter-Friendly Description

Built a production-oriented Python operations platform with Django REST Framework, PostgreSQL, and Streamlit. Demonstrates API design, relational modeling, transactional business logic, authentication, analytics, Excel automation, Docker, CI, and responsive frontend delivery through a realistic fictional business case.
