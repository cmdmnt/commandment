import os
from .app import create_app
from commandment.database import config_engine, init_db

app = create_app()
app.config.from_object('commandment.default_settings')

if os.environ.get('COMMANDMENT_SETTINGS'):
    app.config.from_envvar('COMMANDMENT_SETTINGS')

config_engine(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_DATABASE_ECHO'])
init_db()

