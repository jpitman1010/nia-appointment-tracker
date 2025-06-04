"""Server for Appointments at NIA."""
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from models.models import Staff, Provider, Patient, Appointment_Scheduling_and_Status, db, connect_to_db
from werkzeug.utils import secure_filename
from jinja2 import StrictUndefined
import pandas as pd

import crud
import os
import sys
import json
# from O365 import Account, MSGraphProtocol
# import win32com.client as client
# from O365 import Protocol
import datetime as dt
import xml.etree.ElementTree as ET
import csv
import xlrd

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


def schedule_appointment():
    CLIENT_ID = os.environ("CLIENT_ID")
    SECRET_ID = os.environ("SECRET_ID")
    credentials = (CLIENT_ID, SECRET_ID)
    protocol = MSGraphProtocol()
    scopes = ['Calendars.ReadWrite.Shared']
    account = Account(credentials, protocol=protocol)

    if account.authenticate(scopes=scopes):
        print("Authenticated!")

    return


@app.route('/')
def show_homepage():
    """View login page"""
    # schedule_appointment()
    return render_template('encounter_type.html')


@app.route('/staff_registration_route')
def route_to_registration_page():
    """take staff to registration page"""
    return render_template("staff_registration.html")


@app.route('/staff_registration', methods=['POST'])
def user_reg_post_intake():
    """take staff registration info and make cookies"""
    error = None
    email = request.form.get('email-input')
    password = request.form.get('password-input')
    fname = request.form.get('fname-input')
    lname = request.form.get('lname-input')
    role = request.form.get('role-input')

    print('email =', email, 'password =', password,
          'fname =', fname, 'lname = ', lname, 'role =', role)

    enabled = True

    print(email)
    email_check = crud.check_if_valid_user(email)

    if email_check:
        flash("A staff already exists with that email.  Please try a different email")
    else:
        create_staff = crud.create_staff(
            email, password, fname, lname, role, enabled)
        flash("Please log in.")
        return render_template('/login.html', create_staff=create_staff, fname=fname, email=email, lname=lname, role=role, enabled=enabled)


@app.route('/login_form', methods=['POST'])
def login_form():
    """Process login and check for staff in database"""

    email = request.form.get('email-input')
    password = request.form.get('password-input')
    session['email'] = email
    email_check = crud.check_if_valid_user(email)
    password_check = crud.password_check(email, password)
    if email == "" or password == "":
        flash("Sorry that is not a valid login email or password.")
        return redirect('/')
    elif email_check and password_check:
        return render_template("main_page.html")
    else:
        flash("Sorry that is not a valid login email or password.  Please try again, or register as a new user.")
        return redirect('/')


@app.route('/main_page_route')
def main_page_route():
    """routes to main page"""
    return render_template("main_page.html")

@app.route('/add_encounter_type_route')
def add_encounter_route():
    """routes to page to add an encounter type"""
    return render_template("encounter_type.html")

@app.route('/add_encounter_type', methods=['POST'])
def add_encounter():
    """posts form to database"""

    encounter_name = request.form.get('name_of_encounter_type')
    encounter_duration = request.form.get('duration')
    duration_metric = request.form.get('duration_metric')
    encounter_type = request.form.get('encounter_type')
    crud.create_encounter_type(encounter_name, encounter_duration, duration_metric, encounter_type)


    return render_template("main_page.html")

@app.route('/schedule_by_provider')
def apt_by_provider_route():
    """routes to scheduler for single appointment based on provider filtering"""
    return render_template("ResourceView.html")


@app.route('/schedule_by_room')
def apt_by_room_route():
    """routes to scheduler for single appointment based on room filtering"""
    return render_template("ResourceView.html")


@app.route('/to_do_scheduling')
def scheduling_by_pt_to_do_list_route():
    """routes to scheduler for single appointment based on provider filtering"""
    return render_template("ResourceView.html")


@app.route('/add_patient_route')
def route_to_add_patient_page():
    """take staff to registration page"""
    return render_template("add_patient.html")


@app.route('/add_patient', methods=["POST"])
def add_patient_to_database():
    """add patient to the database"""

    mrn = request.form.get("mrn")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    Greek_fname = request.form.get('Greek_fname')
    Greek_lname = request.form.get('Greek_lname')
    dob = request.form.get("dob")
    place_of_birth = request.form.get('place_of_birth')
    sex = request.form.get('sex')
    handedness = request.form.get('handedness')
    race = request.form.get('race')
    race_subtype = request.form.get('race_subtype')
    fathers_name = request.form.get('fathers_name')
    mothers_name = request.form.get('mothers_name')
    phone = request.form.get("phone")
    surrogate_phone = request.form.get('surrogate_phone')
    surrogate_relationship = request.form.get('surrogate_relationship')
    address = request.form.get('address')
    email = request.form.get("email")
    amka = request.form.get('amka')

    duplicate_check = crud.check_if_patient_exists(lname, dob, mrn)

    if not duplicate_check:
        crud.create_patient(mrn, fname, lname, Greek_fname, Greek_lname, dob, place_of_birth, sex, handedness, race,
                            race_subtype, fathers_name, mothers_name, phone, surrogate_phone, surrogate_relationship, address, email, amka)
        return render_template("patient_options.html")
    else:
        flash("Sorry this patient is already in the database.")
        return redirect('add_patient.html')


@app.route('/search_page_route', methods=["GET"])
def search_page_route():
    patient_list = crud.get_all_pateints()
    print(patient_list)

    return render_template('search.html')


@app.route('/search', methods=["POST", "GET"])
def search_results():
    """display patient chart based on selection from search"""
    mrn = request.form.get('mrn')
    # mrn = request.get['mrn']
    session['mrn'] = mrn
    print(mrn)
    return render_template("patient_chart.html")


@app.route('/add_research_protocol_route')
def research_protocol_route():
    """route to page to add new research protocol/psql table"""
    return render_template('add_research_protocol.html')


@app.route('/pre_to_add_protocol', methods=["POST"])
def information_needed_to_start_adding_new_protocol():
    coordinator_name = request.form.get('coordinator')
    pi_name = request.form.get('p_i')
    study_start_date = request.form.get('start_of_study_date')
    end_start_date = request.form.get('end_of_study_date')
    research_protocol_name = request.form.get('name_of_study')

    crud.add_research_study_to_Research_Study_table(
        research_protocol_name, pi_name, coordinator_name, 'need to set this up', study_start_date, end_start_date)
    crud.create_table(research_protocol_name)


    # return render_template('add_research_protocol.html')
    return render_template('add_research_protocol.html')

@app.route('/add_research_protocol', methods=["GET", "POST"])
def add_research_protocol():
    """add rows to protocol table that will allow for selections/input that will clearly define the protocol"""




    # uplaoded_file = request.files['file']
    # print('this is the uplaoded file', uplaoded_file)
    # UPLOAD_FOLDER = './uploads'
    # ALLOWED_EXTENSIONS = {'xml', 'csv', 'xls', 'xlsx'}
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # print('type(attachment)', type(uplaoded_file))

    # def allowed_file(filename):
    #     return '.' in filename and \
    #         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     # uplaoded_file.save(secure_filename(uplaoded_file.filename))
    #     uplaoded_file.save(os.path.join(
    #         UPLOAD_FOLDER, uplaoded_file.filename))
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         print('there was no file attached so it should go back to request.url')
    #         return redirect(request.url)
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    #     if uplaoded_file.filename == '':
    #         flash('No selected file')
    #         print('there was no file name so it should go back to request.url')
    #         return redirect(request.url)
    #     if uplaoded_file and allowed_file(uplaoded_file.filename):
    #         uplaoded_file.save(os.path.join(
    #             UPLOAD_FOLDER, uplaoded_file.filename))

    #         print('file has been recognized, filename = ', uplaoded_file.filename)
    #         columns = []
    #         # print('file name ===', uplaoded_file.filename)

    #         if uplaoded_file.filename[-3:] == 'xml':
    #             tree = ET.parse(uplaoded_file)
    #             root = tree.getroot()
    #             # Assuming that the first row of the XML file contains tag names
    #             first_row = root[0]
    #             columns = [elem.tag for elem in first_row]
    #         elif uplaoded_file.filename[-3:] == 'csv':
    #             with open(uplaoded_file.filename) as csvfile:
    #                 reader = csv.reader(csvfile)
    #                 first_row = next(reader)
    #                 columns = first_row
    #         elif uplaoded_file.filename[-3:] == 'xls':
    #             data_xls = pd.read_excel(uplaoded_file)
    #             print(data_xls)
    #             workbook = xlrd.open_workbook(
    #                 UPLOAD_FOLDER + '/' + uplaoded_file.filename)
    #             sheet = workbook.sheet_by_index(0)
    #             # Assuming that the first row of the XLS file contains column names
    #             first_row = sheet.row_values(0)
    #             columns = first_row
    #         else:
    #             flash('Sorry this is not an accepted file type.')
    #             return redirect(url_for('add_research_protocol'))

    # # @app.route('/columns')
    # # def sessions():
    # #     columns = columns
    # #     return jsonify(columns)

    # # encounters_selection = request.form.get('encounters_selection')
    # # protocol_requirements = request.form.getlist('protocol_requirements')
    # # print("I just successfully got the add_research_protocol.html's encounter_selection input ==",
    # #       encounters_selection, " and the protocol_requirements checkboxes ===", protocol_requirements)

    # return '''
    # <!doctype html>
    # <title>Protocol</title>
    # <h1>Verify that each part of the protocol is in order in the columns on the table.</h1>
    # <table id="session-table">
    #     <thead>
    #       <tr>
    #         <th>Session ID</th>
    #         <th>Session Name</th>
    #         <th>Session Date</th>
    #         ...
    #       </tr>
    #     </thead>
    #     <tbody>
    #     </tbody>
    #   </table>
    # '''

    return render_template('main_page.html')


# @app.route('/schedule_appointment_route/<patient_id>')
@app.route('/schedule_appointment_route')
def schedule_appointment_route():

    #     """render template for scheduling appointments"""
    return render_template('calendar.html')


@app.route('/schedule_appointment', methods=["POST"])
def schedule_appointment():
    """schedule appointment for clinic or research"""

    mrn = request.form.get('mrn')
    provider = request.form.get('provider')
    appointment_scheduled_date = request.form.get('date')
    start_hour = request.form.get('start_time_hours')
    print('start_hour =', start_hour)
    start_minute = request.form.get('start_time_minutes')
    print('start_minute =', start_minute)
    end_hour = request.form.get('end_time_hours')
    print('end_hour =', end_hour)
    end_minute = request.form.get('end_time_minutes')
    print('end_minute =', end_minute)

    research_protocol = request.form.get('research_protocol')

    print(start_hour, ":", start_minute)

    start_time = start_hour + ":" + start_minute
    end_time = end_hour + ":" + end_minute

    # email = session['email']
    email = 'jpitman1010@gmail.com'

    scheduled_by = crud.get_staff_name(email)

    print('start time == ', start_time)
    print('end time == ', end_time)
    print('mrn == ', mrn)
    print('this is what the date looks like when querying for the date',
          appointment_scheduled_date)

    appointment_scheduled_start = appointment_scheduled_date[-4:] + "-" + \
        appointment_scheduled_date[0:2] + "-" + \
        appointment_scheduled_date[2:5] + " " + start_time
    appointment_scheduled_end = appointment_scheduled_date[-4:] + "-" + \
        appointment_scheduled_date[0:2] + "-" + \
        appointment_scheduled_date[2:5] + " " + end_time

    print('appointment_scheduled_date_start', appointment_scheduled_start,
          'appointment_scheduled_end', appointment_scheduled_end)

    schedule_appointment = crud.schedule_appointment(
        mrn, provider, appointment_scheduled_start, appointment_scheduled_end, research_protocol, scheduled_by)

    list_of_research_studies = crud.find_all_research_projects()

    for study in list_of_research_studies:
        session['study'] = study

    return redirect('calendar.html')


@app.route('/patient_options_route/<patient_id>')
def patient_options_route(patient_id):
    """render template for patient to do list"""

    research_protocols_by_mrn = crud.get_protocol_title_by_patient_id(
        patient_id)

    for study in research_protocols_by_mrn:

        task_list = crud.get_task_list(study)

        research_protocol_id = crud.get_research_protocol_id(study)

        session['research_protocol_title'] = study
        session['research_protocol_id'] = research_protocol_id
        session['task_list'] = task_list

    return render_template('patient_options.html')


@app.route('/patient_options', methods=["POST"])
def patient_options():
    """patient to do list - ability to go into scheduling, change apt status, update data inputs for research protocol"""

    return render_template("patient_options.html ")


@app.route('/reports', methods=["POST"])
def create_reports():
    """running reports"""

    report_type = request.form.get('report_type')
    tables_in_database = crud.get_report_types()
    print(tables_in_database)

    if report_type == "":
        pass

    return render_template('calendar.html')


@app.route('/fosq-10', methods=["POST"])
def functional_outcomes_sleep_questionnaire():
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))
    q8 = int(request.form.get('q8'))
    q9 = int(request.form.get('q9'))
    q10 = int(request.form.get('q10'))
    score = q1+q2+q3+q4+q5+q6+q7+q8+q9+q10

    # create crud function to commit answers to questionnaire to database

    return


@app.route('/ess', methods=["POST"])
def epworth_sleepiness_scale_questionnaire():
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))
    q8 = int(request.form.get('q8'))

    score = q1+q2+q3+q4+q5+q6+q7+q8

    # create crud function to commit answers to questionnaire to database

    return


@app.route('/fss', methods=["POST"])
def fatigue_sleepiness_scale_questionnaire():
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))
    q8 = int(request.form.get('q8'))
    q9 = int(request.form.get('q8'))

    score = q1+q2+q3+q4+q5+q6+q7+q8

    # create crud function to commit answers to questionnaire to database

    return


@app.route('/gad7', methods=["POST"])
def gad_7():
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))

    score = q1+q2+q3+q4+q5+q6+q7

    # create crud function to commit answers to questionnaire to database

    return


@app.route('/isi', methods=["POST"])
def isi():
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))

    score = q1+q2+q3+q4+q5+q6+q7

    if score >= 0 and score < 8:
        interpretation = "No clinically significant insomnia"
    elif score > 7 and score < 15:
        interpretation = "Subthreshold insomnia"
    elif score > 14 and score < 22:
        interpretation = "Clinical insomnia (moderate severity)"
    else:
        interpretation = "Clinical insomnia (severe)"

    # create crud function to commit answers to questionnaire to database

    return


@app.route('/q-cbs', methods=["POST"])
def nia_q_cbs():
    q1 = request.form.get('q1')
    q1_dur = request.form.get('q1_dur')
    q2 = request.form.get('q2')
    q2_dur = request.form.get('q2_dur')
    q3 = request.form.get('q3')
    q3_dur = request.form.get('q3_dur')
    q4 = request.form.get('q4')
    q4_dur = request.form.get('q4_dur')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')
    q7 = request.form.get('q7')
    q7_dur = request.form.get('q7_dur')
    q8 = request.form.get('q8')
    q8_dur = request.form.get('q8_dur')
    q9 = request.form.get('q9')
    q9_dur = request.form.get('q9_dur')
    q10 = request.form.get('q10')
    q10_dur = request.form.get('q10_dur')
    q11 = request.form.get('q11')
    q11_dur = request.form.get('q11_dur')
    q12 = request.form.get('q12')
    q12_dur = request.form.get('q12_dur')
    q13 = request.form.get('q13')
    q13_dur = request.form.get('q13_dur')
    q14 = request.form.get('q14')
    q14_dur = request.form.get('q14_dur')
    q15 = request.form.get('q15')
    q15_dur = request.form.get('q15_dur')
    q16 = request.form.get('q16')
    q16_dur = request.form.get('q16_dur')
    q17 = request.form.get('q17')
    q17_dur = request.form.get('q17_dur')
    q18 = request.form.get('q18')
    q18_dur = request.form.get('q18_dur')
    q19 = request.form.get('q19')
    q19_dur = request.form.get('q19_dur')
    q20 = request.form.get('q20')
    q20_dur = request.form.get('q20_dur')
    q21 = request.form.get('q21')
    q21_dur = request.form.get('q21_dur')
    q22 = request.form.get('q22')
    q22_dur = request.form.get('q22_dur')
    q23 = request.form.get('q23')
    q23_dur = request.form.get('q23_dur')
    q24 = request.form.get('q24')
    q24_dur = request.form.get('q24_dur')
    q25 = request.form.get('q25')
    q25_dur = request.form.get('q25_dur')
    q26 = request.form.get('q26')
    q26_dur = request.form.get('q26_dur')
    q27 = request.form.get('q27')
    q27_dur = request.form.get('q27_dur')
    q28 = request.form.get('q28')
    q28_dur = request.form.get('q28_dur')
    q29 = request.form.get('q29')
    q29_dur = request.form.get('q29_dur')
    q30 = request.form.get('q30')
    q30_dur = request.form.get('q30_dur')
    q31 = request.form.get('q31')
    q31_dur = request.form.get('q31_dur')
    q32 = request.form.get('q32')
    q32_dur = request.form.get('q32_dur')
    q33 = request.form.get('q33')
    q33_dur = request.form.get('q33_dur')
    q34 = request.form.get('q34')
    q34_dur = request.form.get('q34_dur')
    q35 = request.form.get('q35')
    q35_dur = request.form.get('q35_dur')
    q36 = request.form.get('q36')
    q36_dur = request.form.get('q36_dur')
    q37 = request.form.get('q37')
    q37_dur = request.form.get('q37_dur')
    q38 = request.form.get('q38')
    q38_dur = request.form.get('q38_dur')
    q39 = request.form.get('q39')
    q39_dur = request.form.get('q39_dur')
    q40 = request.form.get('q40')
    q40_dur = request.form.get('q40_dur')
    q41 = request.form.get('q41')
    q41_dur = request.form.get('q41_dur')
    q42 = request.form.get('q42')
    q42_dur = request.form.get('q42_dur')
    q43 = request.form.get('q43')
    q43_dur = request.form.get('q43_dur')
    q44 = request.form.get('q44')
    q44_dur = request.form.get('q44_dur')
    q45 = request.form.get('q45')
    q45_dur = request.form.get('q45_dur')
    q46 = request.form.get('q46')
    q46_dur = request.form.get('q46_dur')
    q47 = request.form.get('q47')
    q47_dur = request.form.get('q47_dur')
    q48 = request.form.get('q48')
    q48_dur = request.form.get('q48_dur')
    q49 = request.form.get('q49')
    q49_dur = request.form.get('q49_dur')
    q50 = request.form.get('q50')
    q50_dur = request.form.get('q50_dur')
    q51 = request.form.get('q51')
    q51_dur = request.form.get('q51_dur')
    which_symptom_started_first = request.form.get('starting_symptom')
    when = request.form.get('when')
    # create crud function to commit answers to questionnaire to database
    return


if __name__ == '__main__':

    connect_to_db(app)

    # app.run(host='127.0.0.1', debug=False, use_reloader=True)
    app.run('localhost', 8080, debug=True)
