'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Flask
from .mdm import mdm_app
from .admin import admin_app

def create_app():
    app = Flask(__name__)

    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_app, url_prefix='/admin')

    from .database import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
