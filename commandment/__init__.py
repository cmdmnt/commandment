"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from typing import Union, Optional
from pathlib import PurePath
from flask import Flask, render_template

from commandment.mdm.app import mdm_app
from .ac2.ac2_app import ac2_app
from .api.app_jsonapi import api_app, api
from .api.app_json import flat_api
from .apns.app import api_push_app
from .auth.app import oauth_app
from .auth import oauth2
from .api.configuration import configuration_app
from .enroll.app import enroll_app
from .models import db
from .omdm import omdm_app
from .dep.app import dep_app
from .vpp.app import vpp_app
from .profiles.api import profiles_api_app
from .inventory.api import api_app as inventory_api
from .mdm.api import api_app as mdm_api
from .apps.app_jsonapi import api_app as applications_api

from .threads import startup_thread
from .dep import threads as dep_threads
from .apns import threads as push_threads


def create_app(config_file: Optional[Union[str, PurePath]] = None) -> Flask:
    """Create the Flask Application.

    Configuration is looked up the following order:

    - default_settings.py in the commandment package.
    - config_file parameter passed to this factory method.
    - environment variable ``COMMANDMENT_SETTINGS`` pointing to a .cfg file.

    Args:
        config_file (Union[str, PurePath]): Path to configuration file.

    Returns:
        Instance of the flask application
    """
    app = Flask(__name__)
    app.config.from_object('commandment.default_settings')
    if config_file is not None:
        app.config.from_pyfile(config_file)
    else:
        app.config.from_envvar('COMMANDMENT_SETTINGS')

    db.init_app(app)
    oauth2.init_app(app)

    app.register_blueprint(oauth_app, url_prefix='/oauth')
    app.register_blueprint(enroll_app, url_prefix='/enroll')
    app.register_blueprint(mdm_app)
    app.register_blueprint(configuration_app, url_prefix='/api/v1/configuration')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(api_push_app, url_prefix='/api')
    app.register_blueprint(flat_api, url_prefix='/api')
    app.register_blueprint(profiles_api_app, url_prefix='/api')
    app.register_blueprint(applications_api, url_prefix='/api')
    app.register_blueprint(omdm_app, url_prefix='/omdm')
    app.register_blueprint(ac2_app)
    app.register_blueprint(dep_app)
    app.register_blueprint(vpp_app)

    try:
        from scepy.blueprint import scep_app
        app.register_blueprint(scep_app, url_prefix='/scep')
        app.logger.info('Registered SCEPy service at /scep')
    except ImportError:
        app.logger.warning("SCEP will not be available, cannot load SCEPy")

    # Threads
    startup_thread.start(app)
    # dep_threads.start(app)
    # push_threads.start(app)

    # SPA Entry Point (when not behind nginx or apache)
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

