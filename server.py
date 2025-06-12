from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, abort, Blueprint
)
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.models import Patient, Staff, Appointment, Patient, Questionnaire, Question, QuestionOption, QuestionnaireResponse, Response, db
from crud.patient import search_patients, create_patient
from crud.staff import search_staff, create_staff, update_staff
from search.search import Search, GreekAwareSearch
import os
from dotenv import load_dotenv
from auth.decorators import roles_required

load_dotenv()  # Loads variables from .env or environment

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:admin1234!@localhost:5432/nia_appointment_tracker')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key-for-dev')  # fallback for dev
connect_to_db(app)  # Make sure this runs before other stuff


# Set database URI from environment variable
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:admin1234!@localhost:5432/nia_appointment_tracker')

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db.init_app(app)

# Blueprint for Staff API routes
staff_bp = Blueprint('staff_api', __name__, url_prefix='/api/staff')
# Blueprint for Questionnaire API routes
questionnaire_bp = Blueprint('questionnaire_api', __name__, url_prefix='/api/questionnaires')


# --- Authentication and Session Management ---
def load_user_permissions(staff):
    permissions = {
        "can_prescribe": False,
        "can_order_tests": False,
        "can_manage_users": False,
        "can_view_billing": False,
        "can_view_research_data": False,
        "can_schedule_appointments": False,
    }

    role_names = []
    for role in staff.roles:
        role_names.append(role.name)
        permissions["can_prescribe"] |= role.can_prescribe
        permissions["can_order_tests"] |= role.can_order_tests
        permissions["can_manage_users"] |= role.can_manage_users
        permissions["can_view_billing"] |= role.can_view_billing
        permissions["can_view_research_data"] |= role.can_view_research_data
        permissions["can_schedule_appointments"] |= role.can_schedule_appointments

    return role_names, permissions


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        staff = Staff.query.filter_by(email=email).first()
        if staff and verify_password(password, staff.password):  # your existing password check logic
            role_names, permissions = load_user_permissions(staff)
            session['user_id'] = staff.id
            session['roles'] = role_names
            session['permissions'] = permissions
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))  # or wherever

        else:
            error = 'Invalid email or password.'

    return render_template('login.html', error=error)



def verify_password(input_password, stored_password):
    # TODO: Replace this with hashed password verification
    return input_password == stored_password

@app.route('/admin')
@roles_required('admin')  # Only users with 'admin' role can access this route
def admin_panel():
    return "Welcome to Admin Panel!"


@app.route('/staff')
@roles_required('admin', 'physician', 'clinician', 'research_coordinator')  
# Users with any of these roles can access this route
def staff_page():
    return "Welcome staff!"

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403



# --- Staff API Endpoints ---

@staff_bp.route('/search', methods=['GET'])
def api_search_staff():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])  # Return empty list if no query

    results = search_staff(db.session, query)
    serialized = [
        {
            "id": s.id,
            "fname": s.fname,
            "lname": s.lname,
            "email": s.email,
            "roles": s.role.split(",") if s.role else []
        }
        for s in results
    ]
    return jsonify(serialized)


@staff_bp.route('', methods=['POST'])
def api_create_staff():
    data = request.get_json()
    if not data:
        abort(400, "Missing JSON data")

    roles = data.get("roles")
    if isinstance(roles, list):
        data["role"] = ",".join(roles)
    else:
        data["role"] = roles or ""

    new_staff = create_staff(db.session, data)
    return jsonify({
        "id": new_staff.id,
        "fname": new_staff.fname,
        "lname": new_staff.lname,
        "email": new_staff.email,
        "roles": roles
    }), 201


@staff_bp.route('/<int:staff_id>', methods=['PUT'])
def api_update_staff(staff_id):
    data = request.get_json()
    if not data:
        abort(400, "Missing JSON data")

    roles = data.get("roles")
    if isinstance(roles, list):
        data["role"] = ",".join(roles)
    else:
        data["role"] = roles or ""

    updated_staff = update_staff(db.session, staff_id, data)
    if not updated_staff:
        abort(404, "Staff member not found")

    return jsonify({
        "id": updated_staff.id,
        "fname": updated_staff.fname,
        "lname": updated_staff.lname,
        "email": updated_staff.email,
        "roles": data.get("roles", [])
    })


# Register blueprint
app.register_blueprint(staff_bp)


# --- Dashboard ---

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# --- Patient Search ---

@app.route('/search', methods=['GET'])
def search_patient():
    # Extract search parameters from query string
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    dob = request.args.get('dob')
    mrn = request.args.get('mrn')
    phone = request.args.get('phone')
    email = request.args.get('email')

    patients = search_patients(
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        mrn=mrn,
        phone=phone,
        email=email
    )

    return render_template('search.html', patients=patients)


# --- Helper: Generate MRN ---

def generate_mrn(db_session):
    today_str = datetime.utcnow().strftime('%Y%m%d')
    count_today = db_session.query(func.count(Patient.id)) \
        .filter(Patient.created_date >= datetime.utcnow().date()) \
        .scalar() or 0
    return f"{today_str}{count_today + 1:02d}"


# --- Patient Duplication Check ---

@app.route('/check_patient_duplicate', methods=['POST'])
def check_patient_duplicate():
    data = request.json or {}
    mrn = data.get('mrn', '')
    dob = data.get('dob', '')
    fname = data.get('fname', '')
    lname = data.get('lname', '')
    greek_fname = data.get('greek_fname', '')
    greek_lname = data.get('greek_lname', '')
    phone = data.get('phone', '')
    email = data.get('email', '')

    search_query = ' '.join(filter(None, [mrn, dob, fname, lname, greek_fname, greek_lname, phone, email]))

    session: Session = db.session

    duplicates = (
        session.query(Patient),
        Patient,
        query==search_query,
        fields==["mrn", "dob", "fname", "lname", "greek_fname", "greek_lname", "phone", "email"]
    )

    if duplicates:
        results = [{
            'id': p.id,
            'mrn': p.mrn,
            'fname': p.fname,
            'lname': p.lname,
            'dob': p.dob.strftime('%Y-%m-%d') if p.dob else None,
            'greek_fname': p.greek_fname,
            'greek_lname': p.greek_lname,
            'phone': p.phone,
            'email': p.email
        } for p in duplicates]

        return jsonify({'duplicates': results})

    return jsonify({'duplicates': []})


# --- Add Patient ---

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        data = request.form

        required_fields = ['lname', 'greek_fname', 'greek_lname', 'dob', 'fathers_name', 'phone', 'email']
        for field in required_fields:
            if not data.get(field):
                flash(f"Field {field} is required.")
                return redirect(url_for('add_patient'))

        email = data.get('email') or 'info@nioa.gr'  # default email if none given

        mrn = generate_mrn(db.session)

        patient = create_patient(
            mrn=mrn,
            fname=data.get('fname'),
            lname=data.get('lname'),
            greek_fname=data.get('greek_fname'),
            greek_lname=data.get('greek_lname'),
            dob=data.get('dob'),
            place_of_birth=data.get('place_of_birth'),
            sex=data.get('sex'),
            handedness=data.get('handedness'),
            race=data.get('race'),
            race_subtype=data.get('race_subtype'),
            fathers_name=data.get('fathers_name'),
            mothers_name=data.get('mothers_name'),
            phone=data.get('phone'),
            surrogate_phone=data.get('surrogate_phone'),
            surrogate_relationship=data.get('surrogate_relationship'),
            address=data.get('address'),
            email=email,
            amka=data.get('amka'),
            created_by='current_user',  # TODO: replace with real logged-in user
            updated_by='current_user'
        )

        flash(f"Patient {patient.fname or ''} {patient.lname} added successfully with MRN {mrn}.")
        return redirect(url_for('search_patient'))

    return render_template('add_patient.html')

@app.route('/api/providers', methods=['GET'])
def get_providers():
    providers = Provider.query.all()
    result = [
        {
            "id": p.id,
            "fname": p.fname,
            "lname": p.lname
        }
        for p in providers
    ]
    return jsonify(result)

# ---Calendar: --- 

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    provider_ids = request.args.getlist('provider_ids[]')  # Array of IDs from query param
    if not provider_ids:
        return jsonify([])  # no providers selected, return empty list

    # Convert provider_ids to integers safely
    try:
        provider_ids = list(map(int, provider_ids))
    except ValueError:
        return jsonify([])

    # Query appointments for selected providers that are not deleted
    appointments = Appointment.query.filter(
        Appointment.provider_id.in_(provider_ids),
        Appointment.deleted == False
    ).all()

    events = []
    for appt in appointments:
        patient = Patient.query.get(appt.patient_id)
        provider = Provider.query.get(appt.provider_id)
        events.append({
            "id": appt.id,
            "title": f"{patient.fname} {patient.lname} ({provider.fname} {provider.lname})",
            "start": appt.scheduled_start.isoformat(),
            "end": appt.scheduled_end.isoformat(),
            "providerId": appt.provider_id,
            "color": None  # We'll assign color on frontend per provider
        })

    return jsonify(events)

# ---Emailing Questionnaires ---


# ---Dynamic Questinnaire Route: ---
@questionnaire_bp.route('/<int:questionnaire_id>/questions', methods=['GET'])
def get_questionnaire_questions(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        abort(404, description="Questionnaire not found")

    questions_data = []
    for q in sorted(questionnaire.questions, key=lambda x: x.order or 0):
        question_dict = {
            'id': q.id,
            'question_code': q.question_code,
            'display_text': q.display_text,
            'order': q.order,
            'field_type': q.field_type,
            'options': [{'id': o.id, 'option_text': o.option_text, 'option_value': o.option_value} for o in q.options]
        }
        questions_data.append(question_dict)

    return jsonify({
        'questionnaire_id': questionnaire.id,
        'questionnaire_name': questionnaire.name,
        'questions': questions_data
    })


@app.route('/questionnaire/<questionnaire_name>/<mrn>', methods=['GET'])
def serve_questionnaire(questionnaire_name, mrn):
    # Find questionnaire by name (case-insensitive)
    questionnaire = Questionnaire.query.filter(
        func.lower(Questionnaire.name) == questionnaire_name.lower()
    ).first()
    if not questionnaire:
        abort(404, description=f"Questionnaire '{questionnaire_name}' not found.")

    # Fetch ordered questions for the questionnaire
    questions = Question.query.filter_by(questionnaire_id=questionnaire.id).order_by(Question.order).all()

    # Map questionnaire names to their specific templates
    template_map = {
        'ESS': 'ess.html',
        'FOSQ-10': 'fosq10.html',
        'FSS': 'fss.html',
        'GAD7': 'gad7.html',
        'ISI': 'isi.html',
        'intake_questionnaire': 'intake_questionnaire.html',
        'combined_questionnaires': 'combined_questionnaires.html',
    }

    # Default to generic template if no specific one found
    template_name = template_map.get(questionnaire.name, 'generic_questionnaire.html')

    return render_template(template_name, mrn=mrn, questionnaire=questionnaire, questions=questions)


# --- Dynamic Submit Questionnaire Route ---
@app.route('/questionnaire/<int:questionnaire_id>', methods=['GET', 'POST'])
def submit_questionnaire(questionnaire_id):
    if request.method == 'POST':
        mrn = request.form.get('mrn')  # assuming patient mrn is submitted or session user
        filled_out_by = 'current_user'  # update as per auth

        q_response = QuestionnaireResponse(
            mrn=mrn,
            questionnaire_id=questionnaire_id,
            filled_out_by=filled_out_by,
            created_by=filled_out_by,
            updated_by=filled_out_by
        )
        db.session.add(q_response)
        db.session.flush()  # get q_response.id before commit

        for key, value in request.form.items():
            if key.startswith('q_'):
                question_id = int(key.split('_')[1])
                # For checkboxes multiple values come as comma separated, handle accordingly
                if isinstance(value, list):
                    for v in value:
                        resp = Response(response_set_id=q_response.id, question_id=question_id, answer=v)
                        db.session.add(resp)
                else:
                    resp = Response(response_set_id=q_response.id, question_id=question_id, answer=value)
                    db.session.add(resp)

        db.session.commit()
        flash("Questionnaire submitted successfully.")
        return redirect(url_for('dashboard'))

    # GET method to render template with questions and options fetched from DB
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        abort(404)

    questions = sorted(questionnaire.questions, key=lambda q: q.order or 0)
    return render_template('questionnaire.html', questionnaire_name=questionnaire.name, questionnaire_id=questionnaire.id, questions=questions)


#Dynamic Questionnaire Review Route
@app.route('/questionnaire/<int:response_id>/review')
def review_questionnaire_response(response_id):
    response = QuestionnaireResponse.query.get_or_404(response_id)
    answers = {ans.question_id: ans.answer for ans in response.answers}
    questions = Question.query.filter_by(questionnaire_id=response.questionnaire_id).order_by(Question.order).all()
    return render_template('questionnaire_review.html', response=response, answers=answers, questions=questions)




if __name__ == '__main__':
    app.run(debug=True)
