# NIA Appointment Tracker

## Project Overview

This is the NIA Appointment Tracker, a comprehensive system for managing patient appointments, clinical encounters, research studies, and questionnaires. It includes GDPR-compliant audit trails, integrated Outlook calendar scheduling, and flexible questionnaire management.

Appointment scheduling integrated with Microsoft Outlook calendar

Research study management and dynamic questionnaires

Staff and provider management with access controls

Full audit trail on all sensitive data changes (versioning with SQLAlchemy-Continuum)

Usage Notes
All deletions are soft deletions with audit info for GDPR compliance.

Audit history tables must be initialized (see Alembic migration instructions).

Outlook integration uses Microsoft Graph API for calendar events.

Front-end assets are in static/ and templates/.

Utility functions are in utils/.

Contribution Guidelines
Follow PEP8 and project style.

Document any database schema changes.

Write tests for new features.

Use feature branches and pull requests.

License
MIT License

Contact
For questions or support, please contact Julie Pitman via GitHub.

---

## Project Structure

```
.
├── .gitignore
├── .vscode
│   └── settings.json
├── calendar
│   ├── auth.py
│   └── outlook.py
├── crud
│   ├── init.py
│   ├── appointment.py
│   ├── clinician.py
│   ├── encounter.py
│   ├── generic.py
│   ├── patient.py
│   ├── research.py
│   └── staff.py
├── crud.py
├── main.py
├── models
│   └── models.py
├── README.md
├── requirements.txt
├── search
│   └── search.py
├── secrets.sh
├── seed.py
├── server.py
├── server2.py
├── static
│   ├── css
│   ├── images
│   └── js
├── templates
├── uploads
└── utils
├── fuzzy_search_utils.py
└── utility.py
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Virtual environment recommended

### Installation

1. Clone the repository:

````bash
git clone https://github.com/jpitman1010/nia-appointment-tracker.git
cd nia-appointment-tracker
Create and activate a virtual environment:

```bash
python3 -m venv venv
````

```bash
source venv/bin/activate  # macOS/Linux
```

```bash
venv\Scripts\activate     # Windows
```

## Install dependencies:

```bash
pip install -r requirements.txt
```


### Database Setup
Setup database URI in your environment or config file.

Before running migrations or starting the app, ensure your PostgreSQL server is running and execute:

```bash
python setup_database.py
```
This script will create the PostgreSQL user and database if they do not already exist.

---

### Start the Flask app:

```bash
flask run
```

Features
Patient demographic management with GDPR audit and soft-deletion

### Setup Database

from the root directory run bash:

```bash
./setup.sh
```

Make sure setup.sh has execute permission:

```bash
chmod +x setup.sh
```

### Notes:

1. Adjust the connection user in psycopg2.connect() if your local superuser is different from postgres.
2. This script creates a database named nia_appointment_tracker and a user admin with password admin1234! The password can be changed later for security purposes, this will just be used with initial setup.

## Managing Dependencies (`requirements.txt`)

Over time, your project may accumulate unnecessary or missing packages in the `requirements.txt`. To keep dependencies clean and accurate:

## Using `prune_requirements.py` Script

Run the script to analyze:

```bash
python prune_requirements.py --project-dir=. --requirements=requirements.txt
```

---

## Database Migrations with Alembic

To manage database schema changes safely and consistently, this project uses **Alembic**, a lightweight database migration tool for SQLAlchemy.

### Installation

Add Alembic to your environment if not already installed:

```bash
pip install alembic
```

#Initializing Alembic
#Initialize Alembic in your project root (run once):

```bash
alembic init alembic
```

This creates an alembic folder with configuration files and a versions directory for migration scripts.

### Configure alembic.ini and alembic/env.py:

Update the sqlalchemy.url in alembic.ini with your database connection string (e.g., postgresql://user:password@localhost/dbname).

Modify env.py to import your db metadata for autogeneration (example):

python:
from models.models import db
target_metadata = db.metadata
Creating Migrations
When you update your models:

```bash
alembic revision --autogenerate -m "Describe your changes"
```

### Alembic will generate a migration script in alembic/versions/.

Apply the migration to your database:

```bash
alembic upgrade head
```
