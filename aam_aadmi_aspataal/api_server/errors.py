from flask import jsonify, request, current_app
from aam_aadmi_aspataal.api_server.decorators import crossdomain

class APIError(Exception):
    def __init__(self, message, status_code, payload=None):
        super(APIError, self).__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.status_code
        rv['error'] = self.message
        return rv

    def __str__(self):
        return self.message


class APINoContent(APIError):
    def __init__(self, message, payload=None):
        super(APINoContent, self).__init__(message, 204, payload)


class APINotFound(APIError):
    def __init__(self, message, payload=None):
        super(APINotFound, self).__init__(message, 404, payload)


class APIUnauthorized(APIError):
    def __init__(self, message, payload=None):
        super(APIUnauthorized, self).__init__(message, 401, payload)


class APIBadRequest(APIError):
    def __init__(self, message, payload=None):
        super(APIBadRequest, self).__init__(message, 400, payload)


class APIConflict(APIError):
    def __init__(self, message, payload=None):
        super(APIConflict, self).__init__(message, 409, payload)

class APIInternalServerError(APIError):
    def __init__(self, message, payload=None):
        super(APIInternalServerError, self).__init__(message, 500, payload)


class APIServiceUnavailable(APIError):
    def __init__(self, message, payload=None):
        super(APIServiceUnavailable, self).__init__(message, 503, payload)


class APIForbidden(APIError):
    def __init__(self, message, payload=None):
        super(APIForbidden, self).__init__(message, 403, payload)



def init_error_handlers(app):
    def handle_error(error, code):
        """ Returns appropriate error message on HTTP exceptions

            error (werkzeug.exceptions.HTTPException): The exception that needs to be handled
            code (int): the HTTP error code that should be returned

            Returns:
                A Response which will be a json error if request was made to the LB api and an html page
                otherwise
        """
        return jsonify({'code': code, 'error': error.description}), code

    @app.errorhandler(400)
    def no_content(error):
        return handle_error(error, 204)

    @app.errorhandler(400)
    def bad_request(error):
        return handle_error(error, 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return handle_error(error, 401)

    @app.errorhandler(403)
    def forbidden(error):
        return handle_error(error, 403)

    @app.errorhandler(404)
    def not_found(error):
        return handle_error(error, 404)

    @app.errorhandler(409)
    def conflict(error):
        return handle_error(error, 409)

    @app.errorhandler(500)
    def internal_server_error(error):
        return handle_error(error, 500)

    @app.errorhandler(503)
    def service_unavailable(error):
        return handle_error(error, 503)

    @app.errorhandler(APIError)
    @crossdomain()
    def api_error(error):
        return jsonify(error.to_dict()), error.status_code
