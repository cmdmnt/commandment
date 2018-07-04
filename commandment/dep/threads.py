# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Jesse Peterson, 2018 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.

Attributes:
    dep_thread (threading.Timer):
    dep_start (int): In seconds, time of first run
    dep_time (int): In seconds, time of subsequent runs

Todo:
    * Currently we start this thread after the database context and
      configuration has already been. We envision a day when this runner runs
      standalone and thus we'll need to sort out separate configuration routines etc.
"""
import logging
import threading
import datetime
import dateutil.parser
from flask import Flask
from commandment.models import db, Device
from commandment.dep.models import DEPAccount
from commandment.dep.dep import DEP
from commandment.dep import DEPOrgType, DEPOrgVersion
import sqlalchemy.orm.exc

dep_thread = None
dep_start = 5
dep_time = 90

logger = logging.getLogger('dep thread')


def start(app: Flask):
    """Start the StartUp thread"""
    logger.info('DEP thread will run in 5 seconds')
    dep_thread = threading.Timer(dep_start, dep_thread_callback, [app])
    dep_thread.daemon = True
    dep_thread.start()


def stop():
    """Stop the runner thread"""
    logger.info('DEP thread will stop')
    global dep_thread
    if dep_thread is threading.Timer:
        dep_thread.cancel()


def dep_sync_organization(app: Flask, dep: DEP):
    """Synchronise information from the DEP service to the local database.
    """
    with app.app_context():
        try:
            app.logger.debug('Querying for DEP Account information from the database')
            dep_account: DEPAccount = db.session.query(DEPAccount).one()

            # Refresh organisation information if there is none
            if dep_account.server_name is None or dep_account.server_uuid is None:
                app.logger.debug('Refreshing information about organization from the DEP service')
                account = dep.account()

                if account is not None:
                    dep_account.server_uuid = account.get('server_uuid', None)
                    dep_account.server_name = account.get('server_name', None)
                    dep_account.facilitator_id = account.get('facilitator_id', None)
                    dep_account.admin_id = account.get('admin_id', None)
                    dep_account.org_name = account.get('org_name', None)
                    dep_account.org_email = account.get('org_email', None)
                    dep_account.org_phone = account.get('org_phone', None)
                    dep_account.org_address = account.get('org_address', None)
                    dep_account.org_id = account.get('org_id', None)
                    dep_account.org_id_hash = account.get('org_id_hash', None)
                    if 'org_type' in account:
                        dep_account.org_type = DEPOrgType(account['org_type'])

                    if 'org_version' in account:
                        dep_account.org_version = DEPOrgVersion(account['org_version'])

                    db.session.commit()
                    app.logger.info('Successfully fetched DEP Organization: %s', dep_account.org_name)
                else:
                    app.logger.warn('Failed to fetch DEP Organization')
            else:
                app.logger.info('DEP Organization already fetched: %s', dep_account.org_name)

        except sqlalchemy.orm.exc.NoResultFound:
            app.logger.info('Not attempting to fetch DEP account information. No DEP account is configured.')


def dep_fetch_devices(app: Flask, dep: DEP, dep_account: DEPAccount):
    """Perform fetch or sync of devices."""
    app.logger.info('Fetching using previous cursor: %s', dep_account.cursor)

    # TODO: if fetched_until is quite recent, there's no reason to fetch again

    for device_page in dep.devices(dep_account.cursor):
        print(device_page)
        dep_account.cursor = device_page.get('cursor', None)
        dep_account.more_to_follow = device_page.get('more_to_follow', None)
        dep_account.fetched_until = dateutil.parser.parse(device_page['fetched_until'])
        db.session.commit()


def dep_thread_callback(app: Flask):
    """Runner thread main procedure

    Todo:
        * Catch everything so we don't interrupt the thread (and it never reschedules)
        * Certificate expiration warnings/emails
    """
    threadlocals = threading.local()

    with app.app_context():
        try:
            dep_account: DEPAccount = db.session.query(DEPAccount).one()
            app.logger.info('Checking DEP state')

            dep = DEP(
                consumer_key=dep_account.consumer_key,
                consumer_secret=dep_account.consumer_secret,
                access_token=dep_account.access_token,
                access_secret=dep_account.access_secret,
            )

            dep_sync_organization(app, dep)
            dep_fetch_devices(app, dep, dep_account)

        except sqlalchemy.orm.exc.NoResultFound:
            app.logger.info('Not attempting a DEP sync, no account configured.')

