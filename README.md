# NIA Appointment Tracker

## Project Overview

NIA Appointment Tracker is a system for managing patient appointments, clinical encounters, research studies, questionnaires, and staff/provider access. Features include:

- Appointment scheduling integrated with Microsoft Outlook calendar (via Microsoft Graph API)
- Research study management with dynamic questionnaires
- Staff and provider role management with access controls
- GDPR-compliant audit trails with SQLAlchemy-Continuum versioning
- Front-end assets in `static/` and `templates/`
- Utility functions in `utils/`

---

## Project Structure

.
├── .gitignore
├── .vscode
│ └── settings.json
├── calendar
│ ├── auth.py
│ └── outlook.py
├── crud
│ ├── init.py
│ ├── appointment.py
│ ├── clinician.py
│ ├── encounter.py
│ ├── generic.py
│ ├── patient.py
│ ├── research.py
│ └── staff.py
├── crud.py
├── main.py
├── models
│ └── models.py
├── README.md
├── requirements.txt
├── search
│ └── search.py
├── secrets.sh
├── seed.py
├── server.py
├── server2.py
├── static
│ ├── css
│ ├── images
│ └── js
├── templates
├── uploads
└── utils
├── fuzzy_search_utils.py
└── utility.py

yaml
Copy

---

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- Git
- Virtual environment tool (venv recommended)

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/jpitman1010/nia-appointment-tracker.git
cd nia-appointment-tracker
2. Install PostgreSQL
Install PostgreSQL server appropriate for your OS:

macOS (Homebrew):

bash
Copy
brew install postgresql
brew services start postgresql
Ubuntu/Debian:

bash
Copy
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
Windows:

Download and install from PostgreSQL official page, then start PostgreSQL service from Services manager or pgAdmin.

3. Create PostgreSQL superuser
You need a superuser account (admin) for your setup script to create the application database and user.

macOS/Linux terminal:

bash
Copy
sudo -u postgres createuser --superuser admin
sudo -u postgres psql -c "ALTER ROLE admin WITH PASSWORD 'admin1234!';"
sudo -u postgres psql -c "ALTER ROLE admin WITH SUPERUSER CREATEDB CREATEROLE;"
Windows:

Use pgAdmin or psql shell to create a superuser named admin with password admin1234! and grant all privileges.

4. Configure .env
Create a .env file in the project root with the following variables (do not commit this file):

ini
Copy
DATABASE_URL=postgresql://admin:admin1234!@localhost:5432/nia_appointment_tracker
TEST_DATABASE_URL=postgresql://admin:admin1234!@localhost:5432/nia_appointment_tracker_test

PG_SUPERUSER=admin
PG_SUPERUSER_PASSWORD=admin1234!
DB_NAME=nia_appointment_tracker
DB_USER=admin
DB_PASSWORD=admin1234!
DB_HOST=localhost
DB_PORT=5432

FLASK_SECRET_KEY=fill_in_your_secret_flask_key_here
5. Create and activate Python virtual environment
macOS/Linux:

bash
Copy
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
Windows (PowerShell):

powershell
Copy
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
6. Install dependencies
bash
Copy
pip install -r requirements.txt
7. Run the database setup script
Make sure PostgreSQL service is running. Then:

bash
Copy
python setup_db.py
This creates the database and admin user automatically.

If you encounter permission errors, verify your PostgreSQL superuser exists and has proper privileges.

If errors say tables already exist, either drop the database manually or run Alembic migration stamp (see below).

8. Database migrations with Alembic
Alembic manages schema migrations.

Install Alembic (if not installed):

bash
Copy
pip install alembic
Initialize Alembic (one-time only):

bash
Copy
python -m alembic init alembic
Configure Alembic

Edit alembic.ini, set sqlalchemy.url to your DATABASE_URL.

Edit alembic/env.py to import your SQLAlchemy metadata:

python
Copy
from models.models import db
target_metadata = db.metadata
Run migrations:

To apply migrations to your database:

bash
Copy
python -m alembic upgrade head
If migrations fail due to existing tables:

You can stamp the current revision without running migrations:

bash
Copy
python -m alembic stamp head
9. Running the Flask app
Make sure your venv is activated, then:

bash
Copy
flask run
Or

bash
Copy
python server.py
Additional Notes
Use python -m alembic to run Alembic commands inside your venv to avoid conflicts with global installs.

When adding new Python packages, update requirements.txt:

bash
Copy
pip freeze > requirements.txt
Use the prune_requirements.py script to keep dependencies clean:

bash
Copy
python prune_requirements.py --project-dir=. --requirements=requirements.txt
Ensure PostgreSQL server is running before running setup scripts or migrations.

Adjust setup_db.py if your PostgreSQL superuser differs.

Never commit .env or sensitive credentials to Git.

Contact
For help or questions, please contact Julie Pitman via GitHub.




<!-- # NIA Appointment Tracker

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

````

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Virtual environment recommended

## Installation

PostgreSQL Setup (One-time, required before running setup script)
To ensure the database setup script works correctly, you need to install and configure PostgreSQL server and create a superuser. This is a one-time manual step on any new machine.

### 1. Install PostgreSQL

Follow the official instructions for your platform:

#### macOS (with Homebrew):

```bash
brew install postgresql
````

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Windows:

Download and install from https://www.postgresql.org/download/windows/

### 2. Start PostgreSQL server

Make sure the PostgreSQL service is running.

#### macOS (Homebrew):

```bash
brew services start postgresql
```

#### Ubuntu/Debian:

```bash
sudo systemctl start postgresql
```

#### Windows:

Start the PostgreSQL service from Services manager or use pgAdmin.

### 3. Create PostgreSQL superuser (once)

You need a PostgreSQL superuser account for your setup script to create the application database and user.

#### Run these commands in your terminal (macOS/Linux):

```bash
sudo -u postgres createuser --superuser admin
sudo -u postgres psql -c "ALTER ROLE admin WITH PASSWORD 'admin1234!';"
sudo -u postgres psql -c "ALTER ROLE admin WITH SUPERUSER CREATEDB CREATEROLE;"

```

#### On Windows, use pgAdmin or psql to create a superuser named admin with the password admin1234!.

### . Configure .env file

Set the superuser credentials in your .env file so setup_db.py can connect (be sure to add .env to your .gitignore file so that your secrets stay safe):

#database
DATABASE_URL=postgresql://admin:admin1234!@localhost:5432/nia_appointment_tracker

#testing database (copy of original database for pytests)
TEST_DATABASE_URL=postgresql://admin:admin1234!@localhost:5432/nia_appointment_tracker_test

FLASK_SECRET_KEY=fill_in_your_secret_flask_key_here

PG_SUPERUSER=admin
PG_SUPERUSER_PASSWORD=admin1234!
DB_NAME=nia_appointment_tracker
DB_USER=admin
DB_PASSWORD=admin1234!
DB_HOST=localhost
DB_PORT=5432

### 1. Clone the repository:

````bash
git clone https://github.com/jpitman1010/nia-appointment-tracker.git
cd nia-appointment-tracker
Create and activate a virtual environment:

```bash
#python3 -m venv venv
python3.13 -m venv venv

````

```bash
source venv/bin/activate  # macOS/Linux
```

```bash
venv\Scripts\activate     # Windows
```

```bash
pip install --upgrade pip
```

## Install dependencies:

```bash
pip install -r requirements.txt
```

### Database Setup

Setup database URI in your environment or config file.

Before running migrations or starting the app, ensure your PostgreSQL server is running and execute:

```bash
python setup_db.py
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
source ./setup.sh
```

Make sure setup.sh has execute permission:

```bash
chmod +x setup.sh
```

### Notes:

1. Adjust the connection user in psycopg.connect() if your local superuser is different from postgres.
2. This script creates a database named nia_appointment_tracker and a user admin with password admin1234! The password can be changed later for security purposes, this will just be used with initial setup.

## Managing Dependencies (`requirements.txt`)

Over time, your project may accumulate unnecessary or missing packages in the `requirements.txt`. To keep dependencies clean and accurate:

## Using `prune_requirements.py` Script

Run the script to analyze:

```bash
python prune_requirements.py --project-dir=. --requirements=requirements.txt
```

When you add packages/libraries to your venv, if you need them to run in the future, ensure you use the following command to add them to the requirements.txt:

```bash
pip freeze > requirements.txt
```

---

## Database Migrations with Alembic

To manage database schema changes safely and consistently, this project uses **Alembic**, a lightweight database migration tool for SQLAlchemy.

### Installation

Add Alembic to your environment if not already installed (if you used pip install requirements.txt you should already have it installed):

```bash
pip install alembic
```

#Initializing Alembic
#Initialize Alembic in your project root (run once):

```bash
alembic init alembic
```

This creates an alembic folder with configuration files and a versions directory for migration scripts.

Troubleshoot alembic after install if tables are not populating:

````bash
python -m alembic revision --autogenerate -m "Initial migration"
python -m alembic upgrade head
```

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
````

### Alembic will generate a migration script in alembic/versions/.

Apply the migration to your database:

````bash
alembic upgrade head
``` -->
````
