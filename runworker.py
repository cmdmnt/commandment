#!/usr/bin/env python
'''
Copyright (c) 2015 Jesse Peterson, Phil Weir
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import os
import pkg_resources
import json
import redis
from rq import Worker, Queue, Connection
from commandment import default_settings
from commandment.database import config_engine, init_db
import logging
from commandment.push import push_init

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    """Work through job queue"""

    configuration = {
        'debug': False
    }

    configuration_file = pkg_resources.resource_filename(
        pkg_resources.Requirement.parse('commandment'),
        'config/config.json'
    )

    if os.path.exists(configuration_file):
        with open(configuration_file, 'r') as configuration_fh:
            loaded_configuration = json.load(configuration_fh)
        configuration.update(loaded_configuration)

    for key in ('host', 'port', 'pass', 'database'):
        keyu = key.upper()
        if os.environ.get('REDIS_%s' % keyu):
            configuration['redis'][key] = os.environ.get('REDIS_%s' % keyu)

    connection = redis.StrictRedis(
        host=configuration['redis']['host'],
        port=configuration['redis']['port'],
        db=configuration['redis']['database']
    )
    # Default docker image seems not to use password=configuration['redis']['pass']

    from commandment.database import db_session

    if 'database' not in configuration:
        configuration['database'] = {
            'uri': default_settings.DATABASE_URI,
            'echo': default_settings.DATABASE_ECHO
        }

    config_engine(configuration['database']['uri'], configuration['database']['echo'])

    try:
        init_db()
        push_init()

        with Connection(connection):
            worker = Worker('default')
            worker.work()

    finally:
        db_session.remove()


if __name__ == '__main__':
    run()
