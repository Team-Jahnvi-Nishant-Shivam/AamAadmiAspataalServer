from flask import current_app
from aam_aadmi_aspataal.api_server.errors import APIBadRequest, APIConflict, APIServiceUnavailable

def log_raise_400(msg, error=""):
    current_app.logger.error("BadRequest: %s\n Error: %s" % (msg, error))
    raise APIBadRequest(msg)

def log_raise_409(msg, error=""):
    current_app.logger.error("Conflict: %s\n Error: %s" % (msg, error))
    raise APIConflict(msg)

def log_raise_503(msg, error=""):
    current_app.logger.error("Conflict: %s\n Error: %s" % (msg, error))
    raise APIServiceUnavailable(msg)

def _validate_auth_header():
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        raise APIUnauthorized("You need to provide an Authorization header.")
    try:
        user_type = lower(auth_token.split(" ")[0])
        auth_token = auth_token.split(" ")[1]
    except IndexError:
        raise APIUnauthorized("Provided Authorization header is invalid.")
    
    if user_type not in ["doctor", "patient"]:
        raise APIBadRequest("Invalid user type supplied with token.")

    if user_type == "doctor":
        user = db_doctor.get_by_token(auth_token)
    else:
        user = db_patient.get_by_token(auth_token)

    if user is None:
        raise APIUnauthorized("Invalid authorization token.")

    return user
