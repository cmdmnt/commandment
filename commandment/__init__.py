"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from flask import Flask, render_template

from .mdm_app import mdm_app
from .admin import admin_app
from .mdmcert import admin_mdmcert_app
from .api import api_app
from .api_push import api_push_app
from .api_flat import flat_api
from .enroll import enroll_app
from .ota import ota_app
from .models import db


def create_app() -> Flask:
    """Create the Flask Application

    Returns:
        Instance of the flask application
    """
    app = Flask(__name__)
    app.config.from_object('commandment.default_settings')
    app.config.from_envvar('COMMANDMENT_SETTINGS', True)

    db.init_app(app)
    db.create_all(app=app)

    app.register_blueprint(enroll_app, url_prefix='/enroll')
    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_app)
    app.register_blueprint(admin_mdmcert_app, url_prefix='/admin/mdmcert')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(api_push_app, url_prefix='/api')
    app.register_blueprint(flat_api, url_prefix='/api')
    app.register_blueprint(ota_app, url_prefix='/ota')

    # SPA history fallback handler
    @app.errorhandler(404)
    def send_index(path: str):
        return render_template('index.html')

    return app

UPLOADCERT_SUPPORTED_MIMETYPES = [
    'application/x-pem-file',
    'application/x-x509-user-cert',
    'application/x-x509-ca-cert',
    'application/x-pkcs12'
]
