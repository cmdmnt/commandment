'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import os
from rq import Queue
from flask import Flask
from .mdm_app import mdm_app
from .admin import admin_app
from .mdmcert import admin_mdmcert_app
from .api import create_api


def create_app(debug, redis_store, configuration=None):
    """Factory for Flask app object"""
    app = Flask(__name__)
    api_app = create_api(debug)

    if configuration:
        app.config.from_object('commandment.default_settings')

        if os.environ.get('COMMANDMENT_SETTINGS'):
            app.config.from_envvar('COMMANDMENT_SETTINGS')

        app.config['REDIS_URL'] = "redis://{password}@{host}:{port}/{database}".format(
            host=configuration['redis']['host'],
            port=configuration['redis']['port'],
            password=configuration['redis']['pass'],
            database=configuration['redis']['database']
        )

    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_app, url_prefix='/admin')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(admin_mdmcert_app, url_prefix='/admin/mdmcert')

    print "REDIS: ", app.config.get('REDIS_URL')
    redis_store.init_app(app)
    app.redis_store = redis_store
    app.redis_queue = Queue(connection=redis_store._redis_client)
    app.redis_queue.enqueue('commandment.tasks.process_profile_deployment_change')

    from .database import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Shutdown routine"""
        if exception:
            print "Exception reached shutdown: " + repr(exception)
        db_session.remove()

    return app
