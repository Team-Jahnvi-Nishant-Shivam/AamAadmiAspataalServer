import os
import pprint
import sys

from time import sleep
from shutil import copyfile
from admin.flask import CustomFlask
from aam_aadmi_aspataal import config
from flask import request, url_for, redirect


def gen_app(config_path=None, debug=None):
    """ Generate a Flask app for aam_aadmi_aspataal with all configurations done and connections established.
    In the Flask app returned, blueprints are not registered.
    """
    app = CustomFlask(
        import_name=__name__,
    )
    from aam_aadmi_aspataal import db
    db.init_db_connection(config.SQLALCHEMY_DATABASE_URI)
    return app


def create_app(config_path=None, debug=None):

    app = gen_app(config_path=config_path, debug=debug)

    _register_blueprints(app)

    return app

def _register_blueprints(app):
    print("done")
    # from listenbrainz.webserver.views.index import index_bp
    # from listenbrainz.webserver.views.login import login_bp
    # from listenbrainz.webserver.views.api import api_bp
    # from listenbrainz.webserver.views.api_compat import api_bp as api_bp_compat
    # from listenbrainz.webserver.views.user import user_bp
    # from listenbrainz.webserver.views.profile import profile_bp
    # from listenbrainz.webserver.views.follow import follow_bp
    # from listenbrainz.webserver.views.follow_api import follow_api_bp
    # from listenbrainz.webserver.views.stats_api import stats_api_bp
    # from listenbrainz.webserver.views.status_api import status_api_bp
    # from listenbrainz.webserver.views.player import player_bp
    # from listenbrainz.webserver.views.feedback_api import feedback_api_bp
    # from listenbrainz.webserver.views.recommendations_cf_recording_api import recommendations_cf_recording_api_bp
    # app.register_blueprint(index_bp)
    # app.register_blueprint(login_bp, url_prefix='/login')
    # app.register_blueprint(user_bp, url_prefix='/user')
    # app.register_blueprint(profile_bp, url_prefix='/profile')
    # app.register_blueprint(follow_bp, url_prefix='/follow')
    # app.register_blueprint(player_bp, url_prefix='/player')
    # app.register_blueprint(api_bp, url_prefix=API_PREFIX)
    # app.register_blueprint(follow_api_bp, url_prefix=API_PREFIX+'/follow')
    # app.register_blueprint(stats_api_bp, url_prefix=API_PREFIX+'/stats')
    # app.register_blueprint(status_api_bp, url_prefix=API_PREFIX+'/status')
    # app.register_blueprint(feedback_api_bp, url_prefix=API_PREFIX+'/feedback')
    # app.register_blueprint(api_bp_compat)
    # app.register_blueprint(recommendations_cf_recording_api_bp, url_prefix=API_PREFIX+'/cf/recommendation')

