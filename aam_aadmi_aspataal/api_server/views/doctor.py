import psycopg2
import sqlalchemy
import aam_aadmi_aspataal.db.doctor as db_doctor
import aam_aadmi_aspataal.db.appointment as db_appointment
import aam_aadmi_aspataal.db.prescription as db_prescription

from datetime import datetime, timedelta
from aam_aadmi_aspataal import api_server
from flask import Blueprint, request, current_app, jsonify
from aam_aadmi_aspataal.api_server.decorators import crossdomain
from aam_aadmi_aspataal.api_server.api_tools import log_raise_400, log_raise_409, \
     log_raise_503, _validate_doctor_auth_header

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/signup', methods=['POST'])
def signup():
    firebase_id = request.args.get('firebase_id')
    if firebase_id is None:
        log_raise_400('firebase_id missing.')
    try:
        db_doctor.create(firebase_id=firebase_id)
    except sqlalchemy.exc.IntegrityError as e:
        log_raise_409('A doctor with firebase_id %s is already registered.' % str(firebase_id), str(e))
    except Exception as e:
        log_raise_503("Couldn't insert record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok'
        }
    )

@crossdomain(headers='Authorization, Content-Type')
@doctor_bp.route('/get-details', methods=['POST'])
def get_details():
    doctor = _validate_doctor_auth_header()

    del doctor['id']

    return jsonify(
        {
            'doctor': doctor
        }
    )

@crossdomain(headers='Authorization, Content-Type')
@doctor_bp.route('/update-details', methods=['POST'])
def update_details():
    doctor = _validate_doctor_auth_header()
    
    name = request.args.get('name')
    email_id = request.args.get('email_id')
    specialisation = request.args.get('specialisation')
    registration_no = request.args.get('registration_no')

    try:
        db_doctor.update_record(id=doctor['id'], name=name, email_id=email_id,
                                specialisation=specialisation, registration_no=registration_no)
    except Exception as e:
        log_raise_503("Couldn't update record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok'
        }
    )


@crossdomain(headers='Authorization, Content-Type')
@doctor_bp.route('/get-appointments-for-today', methods=['POST'])
def get_appointments_for_today():
    doctor = _validate_doctor_auth_header()

    time_now = datetime.now()
    start_time = time_now.replace(hour=10, second=0, minute=0, microsecond=0)
    end_time = time_now.replace(hour=17, second=0, minute=0, microsecond=0)

    try:
        appointments = db_appointment.get_appointments_for_today_for_doctor(doctor_id=doctor['id'],
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
@doctor_bp.route('/get-past-appointments', methods=['POST'])
def get_past_appointments():
    doctor = _validate_doctor_auth_header()

    end_time = datetime.now()

    try:
        appointments = db_appointment.get_past_appointments_for_doctor(doctor_id=doctor['id'],
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
@doctor_bp.route('/get-all-appointments', methods=['POST'])
def getall_appointments():
    doctor = _validate_doctor_auth_header()

    end_time = datetime.now()

    try:
        appointments = db_appointment.get_all_appointments_for_doctor(doctor_id=doctor['id'])
    except Exception as e:
        log_raise_503("Couldn't fetch records. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok',
        'all_appointments': appointments
        }
    )

@crossdomain(headers='Authorization, Content-Type')
@doctor_bp.route('/upload-prescription', methods=['POST'])
def upload_prescription():
    doctor = _validate_doctor_auth_header()
    
    appointment_id = request.args.get('appointment_id')
    prescription_details = request.args.get('prescription_details')

    if appointment_id is None:
        log_raise_400('Appointment ID missing.')
    if prescription_details is None:
        log_raise_400('Prescription Details missing.')
    if prescription_details == '':
        log_raise_400('Empty prescription submitted.')

    appointment = db_appointment.get_appointment_by_id(appointment_id=appointment_id)

    if appointment is None:
        log_raise_400("Invalid Appointment ID submitted.")

    if appointment['prescription_details'] is not None:
        log_raise_409('A prescription for given appointment is already uploaded.')
      
    try:
        db_prescription.create(appointment_id=appointment_id, prescription_details=prescription_details)
    except Exception as e:
        log_raise_503("Couldn't create record. Please try again later.", str(e))

    return jsonify(
        {
        'status': 'ok'
        }
    )

