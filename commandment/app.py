'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Flask
from .mdm import mdm_app
from .admin import admin_app
from .mdmcert import admin_mdmcert_app
from .api import create_api

def create_app(debug=False):
    app = Flask(__name__)
    api_app = create_api(debug)

    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_app, url_prefix='/admin')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(admin_mdmcert_app, url_prefix='/admin/mdmcert')

    from .database import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
