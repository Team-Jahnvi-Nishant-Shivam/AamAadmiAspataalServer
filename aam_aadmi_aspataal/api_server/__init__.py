import os
import sys

from flask import Flask
from aam_aadmi_aspataal import config


def gen_app():
    """ Generate a Flask app for aam_aadmi_aspataal with all configurations done and connections established.
    In the Flask app returned, blueprints are not registered.
    """
    app = Flask(
        import_name=__name__
        )
    from aam_aadmi_aspataal import db
    db.init_db_connection(config.SQLALCHEMY_DATABASE_URI)
    return app


def create_app(config_path=None, debug=None):

    app = gen_app()

    _register_blueprints(app)


    # Error handling
    from aam_aadmi_aspataal.api_server.errors import init_error_handlers
    init_error_handlers(app)

    return app

def _register_blueprints(app):
    from aam_aadmi_aspataal.api_server.views.doctor import doctor_bp
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
