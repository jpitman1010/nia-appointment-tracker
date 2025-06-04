# NIA Appointment Tracker

## Project Overview

This is the NIA Appointment Tracker, a comprehensive system for managing patient appointments, clinical encounters, research studies, and questionnaires. It includes GDPR-compliant audit trails, integrated Outlook calendar scheduling, and flexible questionnaire management.

---

## Project Structure

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

yaml
Copy

---

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Virtual environment recommended

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jpitman1010/nia-appointment-tracker.git
cd nia-appointment-tracker
Create and activate a virtual environment:

bash
Copy
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

Install dependencies:

bash
Copy
pip install -r requirements.txt
Setup database URI in your environment or config file.

Run database migrations and seed initial data (instructions coming soon).

Start the Flask app:

bash
Copy
flask run
Features
Patient demographic management with GDPR audit and soft-deletion

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
```
