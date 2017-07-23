"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from flask import Flask, render_template
from flask_jwt import JWT

from commandment.mdm.app import mdm_app
from .ac2.ac2_app import ac2_app
from .api.app_jsonapi import api_app
from .api.app_json import flat_api
from .apns.app import api_push_app
from .auth import authenticate, identity
from .configuration import configuration_app
from .enroll.app import enroll_app
from .models import db
from .omdm import omdm_app
from .sso.oauth import oauth_app
from .sso.saml import saml_app
from .dep.app import dep_app


def create_app() -> Flask:
    """Create the Flask Application

    Returns:
        Instance of the flask application
    """
    app = Flask(__name__)
    app.config.from_object('commandment.default_settings')
    app.config.from_envvar('COMMANDMENT_SETTINGS', True)

    db.init_app(app)
    # Use alembic to perform migrations
    # db.create_all(app=app)

    jwt = JWT(app, authenticate, identity)

    app.register_blueprint(enroll_app, url_prefix='/enroll')
    app.register_blueprint(mdm_app)
    app.register_blueprint(configuration_app, url_prefix='/api/v1/configuration')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(api_push_app, url_prefix='/api')
    app.register_blueprint(flat_api, url_prefix='/api')
    app.register_blueprint(oauth_app, url_prefix='/oauth')
    app.register_blueprint(saml_app, url_prefix='/saml')
    app.register_blueprint(omdm_app, url_prefix='/omdm')
    app.register_blueprint(ac2_app)
    app.register_blueprint(dep_app)

    # SPA Entry Point
    @app.route('/')
    def index():
        """Main entry point for the administrator web application."""
        return render_template('index.html')

    # SPA history fallback handler
    @app.errorhandler(404)
    def send_index(path: str):
        """Fallback route for HTML5 History."""
        return render_template('index.html')

    return app

