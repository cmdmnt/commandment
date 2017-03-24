'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .mdm import mdm_app
from .admin import admin_app
from .mdmcert import admin_mdmcert_app

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    db.init_app(app)

    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_app, url_prefix='/admin')
    app.register_blueprint(admin_mdmcert_app, url_prefix='/admin/mdmcert')

    return app
