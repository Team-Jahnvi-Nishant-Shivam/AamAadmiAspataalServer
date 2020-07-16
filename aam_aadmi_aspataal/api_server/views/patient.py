import psycopg2
import sqlalchemy
import aam_aadmi_aspataal.db.doctor as db_doctor
import aam_aadmi_aspataal.db.report as db_report
import aam_aadmi_aspataal.db.patient as db_patient
import aam_aadmi_aspataal.db.appointment as db_appointment

from datetime import datetime, timedelta
from aam_aadmi_aspataal import api_server
from flask import Blueprint, request, current_app, jsonify
from aam_aadmi_aspataal.api_server.decorators import crossdomain
from aam_aadmi_aspataal.api_server.api_tools import log_raise_400, log_raise_409, \
     log_raise_503, _validate_patient_auth_header

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/signup', methods=['POST'])
def signup():
    firebase_id = request.args.get('firebase_id')
    if firebase_id is None:
        log_raise_400('firebase_id missing.')
    try:
        db_patient.create(firebase_id=firebase_id)
    except sqlalchemy.exc.IntegrityError as e:
        log_raise_409('A patient with firebase_id %s is already registered.' % str(firebase_id), str(e))
    except Exception as e:
        log_raise_503("Couldn't insert record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok'
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/get-details')
def get_details():
    patient = _validate_patient_auth_header()

    del patient['id']

    return jsonify(
        {
            'patient': patient
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/update-details', methods=['POST'])
def update_details():
    patient = _validate_patient_auth_header()
    
    name = request.args.get('name')
    phone_no = request.args.get('phone_no')

    try:
        db_patient.update_record(id=patient['id'], name=name, phone_no=phone_no)
    except Exception as e:
        log_raise_503("Couldn't update record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok'
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/upload-report', methods=['POST'])
def upload_report():
    patient = _validate_patient_auth_header()
    
    image_url = request.args.get('image_url')
    report_details = request.args.get('report_details')

    if image_url is None:
        log_raise_400('Image URL missing.')

    try:
        db_report.create(patient_id=patient['id'], image_url=image_url, report_details=report_details)
    except sqlalchemy.exc.IntegrityError as e:
        log_raise_409('A report with image_url %s is already uploaded.' % str(image_url), str(e))
    except Exception as e:
        log_raise_503("Couldn't create record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok'
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/get-reports')
def get_reports():
    patient = _validate_patient_auth_header()
    
    try:
        reports = db_report.get_by_patient_id(patient_id=patient['id'])
    except Exception as e:
        log_raise_503("Couldn't create record. Please try again later.", str(e))

    return jsonify(
        {
        'reports': reports
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/book-appointment', methods=['POST'])
def book_appointment():
    patient = _validate_patient_auth_header()
    
    doctor_firebase_id = request.args.get('doctor_id')
    problem_description = request.args.get('problem_description')

    if doctor_firebase_id is None:
        log_raise_400('Doctor ID missing.')

    doctor = db_doctor.get_by_token(firebase_id=doctor_firebase_id)

    time_now = datetime.now()

    # Check if appointment is already scheduled
    next_appointment_time = db_appointment.get_next_appointment_for_doctor_and_patient(doctor_id=doctor['id'], 
                                                                                       patient_id=patient['id'],
                                                                                       time=time_now)

    if next_appointment_time:
        log_raise_409("Your appointment is already scheduled at: %s" %next_appointment_time)

    # Get doctor's latest appointment time
    latest_appointment_time = db_appointment.get_latest_appointment_time_for_doctor_or_patient(doctor_id=doctor['id'],
                                                                                               patient_id=patient['id'])

    if latest_appointment_time is None or latest_appointment_time - time_now < timedelta(minutes=30):  
        # Add 1 hour 30 minutes and then round off so that there is sufficient time to appointment
        appointment_time = time_now + timedelta(hours=1, minutes=30)
        appointment_time = appointment_time.replace(second=0, minute=0)
    else:
        appointment_time = time_now + timedelta(minutes=30)

    # 1:00 PM to 2:00 PM --> Lunch Break
    if appointment_time.hour == 13:
        appointment_time = appointment_time.replace(second=0, minute=0, hour=14)

    # 10:00 AM to 5:00 PM --> Duty Hours
    # If appointment goes beyond 5:00 schedule it at 10:00PM next day
    while True:
        if appointment_time.hour >= 17 or appointment_time.hour < 10:
            if latest_appointment_time and latest_appointment_time.day >= appointment_time.day + 1:
                appointment_time = latest_appointment_time + timedelta(minutes=30)
            else:
                appointment_time = appointment_time.replace(second=0, minute=0, hour=10, day=appointment_time.day + 1)
    
            if appointment_time.hour == 13:
                appointment_time = appointment_time.replace(second=0, minute=0, hour=14)

        else: 
            break

    try:
        db_appointment.create(doctor_id=doctor['id'], patient_id=patient['id'], time=appointment_time,
                              problem_description=problem_description)
    except Exception as e:
        log_raise_503("Couldn't create record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok',
        'appointment_time': appointment_time
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/get-appointments-for-today')
def get_appointments_for_today():
    patient = _validate_patient_auth_header()

    time_now = datetime.now()
    start_time = time_now.replace(hour=10, second=0, minute=0, microsecond=0)
    end_time = time_now.replace(hour=17, second=0, minute=0, microsecond=0)

    try:
        appointments = db_appointment.get_appointments_for_today_for_patient(patient_id=patient['id'],
                                                                             start_time=start_time,
                                                                             end_time=end_time)
    except Exception as e:
        log_raise_503("Couldn't fetch records. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok',
        'appointments_for_today': appointments
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/get-past-appointments')
def get_past_appointments():
    patient = _validate_patient_auth_header()

    end_time = datetime.now()

    try:
        appointments = db_appointment.get_past_appointments_for_patient(patient_id=patient['id'],
                                                                        end_time=end_time)
    except Exception as e:
        log_raise_503("Couldn't fetch records. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok',
        'past_appointments': appointments
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@patient_bp.route('/get-all-appointments')
def getall_appointments():
    patient = _validate_patient_auth_header()

    end_time = datetime.now()

    try:
        appointments = db_appointment.get_all_appointments_for_patient(patient_id=patient['id'])
    except Exception as e:
        log_raise_503("Couldn't fetch records. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok',
        'all_appointments': appointments
        }
    )
