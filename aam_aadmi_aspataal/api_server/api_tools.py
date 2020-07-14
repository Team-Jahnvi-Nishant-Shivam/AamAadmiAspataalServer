import aam_aadmi_aspataal.db.doctor as db_doctor
import aam_aadmi_aspataal.db.patient as db_patient

from flask import current_app, request
from aam_aadmi_aspataal.api_server.errors import APIBadRequest, APIConflict, APIServiceUnavailable, \
     APIUnauthorized

def log_raise_400(msg, error=""):
    current_app.logger.error("BadRequest: %s\n Error: %s" % (msg, error))
    raise APIBadRequest(msg)

def log_raise_409(msg, error=""):
    current_app.logger.error("Conflict: %s\n Error: %s" % (msg, error))
    raise APIConflict(msg)

def log_raise_503(msg, error=""):
    current_app.logger.error("Conflict: %s\n Error: %s" % (msg, error))
    raise APIServiceUnavailable(msg)

def _validate_doctor_auth_header():
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        raise APIUnauthorized("You need to provide an Authorization header.")
    try:
        auth_token = auth_token.split(" ")[1]
    except IndexError:
        raise APIUnauthorized("Provided Authorization header is invalid.")
    
    doctor = db_doctor.get_by_token(auth_token)

    if doctor is None:
        raise APIUnauthorized("Invalid authorization token.")

    return doctor

def _validate_patient_auth_header():
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        raise APIUnauthorized("You need to provide an Authorization header.")
    try:
        auth_token = auth_token.split(" ")[1]
    except IndexError:
        raise APIUnauthorized("Provided Authorization header is invalid.")
    
    patient = db_patient.get_by_token(auth_token)

    if patient is None:
        raise APIUnauthorized("Invalid authorization token.")

    return patient
