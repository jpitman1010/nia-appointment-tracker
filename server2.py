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
    return render_template('add_research_protocol.html')


@app.route('/add_research_protocol_route')
def research_protocol_route():
    """route to page to add new research protocol/psql table"""
    return render_template('add_research_protocol.html')


@app.route('/add_research_protocol', methods=["GET", "POST"])
def add_research_protocol():
    """add table with columns for required appts, labs, tests, paperwork, bio-samples"""

    coordinator_name = request.form.get('coordinator')
    pi_name = request.form.get('p_i')
    study_start_date = request.form.get('start_of_study_date')
    end_start_date = request.form.get('end_of_study_date')
    research_protocol_name = request.form.get('name_of_study')

    crud.add_research_study_to_Research_Study_table(
        research_protocol_name, pi_name, coordinator_name, 'need to set this up', study_start_date, end_start_date)
    crud.create_table(research_protocol_name)

    uplaoded_file = request.files['file']
    print('this is the uplaoded file', uplaoded_file)
    UPLOAD_FOLDER = './uploads'
    ALLOWED_EXTENSIONS = {'xml', 'csv', 'xls', 'xlsx'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print('type(attachment)', type(uplaoded_file))

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print('there was no file attached so it should go back to request.url')
            return redirect(request.url)

        if uplaoded_file.filename == '':
            flash('No selected file')
            print('there was no file name so it should go back to request.url')
            return redirect(request.url)

        if uplaoded_file and allowed_file(uplaoded_file.filename):
            # uplaoded_file.save(os.path.join(
            # UPLOAD_FOLDER, uplaoded_file.filename))
            uplaoded_file.save(os.path.join(
                UPLOAD_FOLDER, uplaoded_file.filename))

            print('file has been recognized, filename = ', uplaoded_file.filename)
            columns = []
            # print('file name ===', uplaoded_file.filename)

            if uplaoded_file.filename[-3:] == 'xls':
                # data_xls = pd.read_excel(
                #     UPLOAD_FOLDER + '/' + uplaoded_file.filename)
                # print(data_xls)
                workbook = xlrd.open_workbook(
                    UPLOAD_FOLDER + '/' + uplaoded_file.filename)
                sheet = workbook.sheet_by_index(0)
                # Assuming that the first row of the XLS file contains column names
                first_row = sheet.row_values(0)
                second_row = sheet.row_values(1)
                columns = first_row

            else:
                flash('Sorry this is not an accepted file type.')
                return redirect(url_for('add_research_protocol'))

            kwargs_for_table = {}

    column_headers = ""
    i = 0
    for header in columns:
        column_headers += "<th>" + header + "</th>"
        kwargs_for_table[header] = second_row[i]

        i += 1
    crud.add_columns_to_table(research_protocol_name, kwargs_for_table)

    print('kwargs to make model table = ', kwargs_for_table)

    return f'''
    <!doctype html>
    <title>Protocol</title>
    <link rel="stylesheet" href="../static/css/add_research_protocol.css">
    <h1>Verify that each part of the protocol is in order in the columns on the table.</h1>
    <table id="session-table">
        <thead>
          <tr>
           {column_headers}
          </tr>
        </thead>
        <tbody>
        </tbody>
      </table>
    '''


def create_reports():
    """running reports"""

    report_type = request.form.get('report_type')
    tables_in_database = crud.get_report_types()
    print(tables_in_database)

    if report_type == "":
        pass

    return render_template('calendar.html')


if __name__ == '__main__':

    connect_to_db(app)

    # app.run(host='127.0.0.1', debug=False, use_reloader=True)
    app.run('localhost', 8080, debug=True)
