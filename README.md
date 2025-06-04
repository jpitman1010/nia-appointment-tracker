# NIA Appointment Tracker

## Overview

This application tracks patient appointments, provider schedules, research study participation, and questionnaire responses, with full GDPR-compliant auditing and Outlook calendar integration.

## Features

- Patient and provider management
- Appointment scheduling with Outlook sync
- Research study tracking with dynamic fields
- Questionnaire management (e.g., ESS, FSS)
- Full audit history and soft-deletion for GDPR compliance

## Requirements

- Python 3.7+
- PostgreSQL database
- Flask
- SQLAlchemy + SQLAlchemy-Continuum
- Microsoft Graph API setup for Outlook integration

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd NIA_Appointment_Tracker
```

### 2. Create virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up secrets

Create a `secrets.sh` file for environment variables like Azure credentials and DB URI. Example:

```bash
export FLASK_APP=server.py
export DB_URI=postgresql:///NIA_Appointment_Tracker
export MS_CLIENT_ID=your_id_here
export MS_CLIENT_SECRET=your_secret_here
export MS_TENANT_ID=your_tenant_here
export MS_USER_EMAIL=info@nioa.gr
```

###I will provide local file for you to use, remove this instrcution for future.

Run:

```bash
source secrets.sh
```

### 5. Initialize the database

```bash
python3
>>> from models import db, connect_to_db
>>> from server import app
>>> connect_to_db(app)
>>> db.create_all()
```

### 6. Enable history tables for versioning

If using Alembic, run:

```bash
alembic revision --autogenerate -m "Initial versioned tables"
alembic upgrade head
```

Otherwise, raw SQL setup instructions can be provided.

## Development Notes

- Soft deletes (`deleted`, `deleted_by`, `deleted_at`) replace actual record deletion.
- Versioned fields (`created_by`, `updated_by`, etc.) ensure full audit trail.
- GDPR compliance features implement Articles 5, 9, and 30 explicitly.
- History tables are automatically maintained by `sqlalchemy-continuum`.

## Outlook Integration

- Requires MS Graph App Registration with delegated permissions.
- Uses headless token-based access to a shared calendar.
- File: `outlook.py` handles scheduling and availability.

## Running the App

```bash
flask run
```

## Future Work

- Admin dashboard
- Fine-grained permission control
- Email reminders and SMS integration
- Consent audit export tools
