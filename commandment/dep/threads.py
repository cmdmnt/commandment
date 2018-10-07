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

# Necessary because SQLAlchemy isn't threadsafe by default
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from commandment.dep.errors import DEPServiceError
from commandment.models import db, Device
from commandment.dep.models import DEPAccount
from commandment.dep.dep import DEP
from commandment.dep import DEPOrgType, DEPOrgVersion, DEPOperationType
import sqlalchemy.orm.exc
import sqlalchemy.exc

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


def dep_fetch_devices(app: Flask, dep: DEP, dep_account_id: int):
    """Perform fetch or sync of devices.

    TODO: If default DEP Profile is nominated, it is queued for assignment here. But may want to check `profile_status`
        to see whether only devices with the `removed` status are considered unassigned.

    See:
        https://docs.sqlalchemy.org/en/latest/orm/contextual.html
    """
    thread_session = db.create_scoped_session()

    dep_account: DEPAccount = thread_session.query(DEPAccount).one()

    if dep_account.cursor is not None:
        app.logger.info('Syncing using previous cursor: %s', dep_account.cursor)
    else:
        app.logger.info('No DEP cursor found, performing a full fetch')

    # TODO: if fetched_until is quite recent, there's no reason to fetch again
    for device_page in dep.devices(dep_account.cursor):
        print(device_page)
        for device in device_page['devices']:
            if 'op_type' in device:  # its a sync, not a fetch
                optype = DEPOperationType(device['op_type'])

                if optype == DEPOperationType.Added:
                    app.logger.debug('DEP Added: %s', device['serial_number'])
                elif optype == DEPOperationType.Modified:
                    app.logger.debug('DEP Modified: %s', device['serial_number'])
                elif optype == DEPOperationType.Deleted:
                    app.logger.debug('DEP Deleted: %s', device['serial_number'])
                else:
                    app.logger.error('DEP op_type not recognised (%s), skipping', device['op_type'])
                    continue
            else:
                pass

            try:
                d: Device = thread_session.query(Device).filter(Device.serial_number == device['serial_number']).one()
                d.description = device['description']
                d.model = device['model']
                d.os = device['os']
                d.device_family = device['device_family']
                d.color = device['color']
                d.profile_status = device['profile_status']
                if device['profile_status'] != 'empty':
                    d.profile_uuid = device.get('profile_uuid', None)  # Only exists in DEP Sync not Fetch?
                    d.profile_assign_time = dateutil.parser.parse(device['profile_assign_time'])

                d.device_assigned_by = device['device_assigned_by']
                d.device_assigned_date = dateutil.parser.parse(device['device_assigned_date'])
                d.is_dep = True

            except sqlalchemy.orm.exc.NoResultFound:
                app.logger.debug('No existing device record for serial: %s', device['serial_number'])

                if device['profile_status'] != 'empty':
                    device['profile_assign_time'] = dateutil.parser.parse(device['profile_assign_time'])

                device['device_assigned_date'] = dateutil.parser.parse(device['device_assigned_date'])

                if 'op_type' in device:
                    del device['op_type']
                    del device['op_date']
                    del device['profile_assign_time']
                    del device['device_assigned_date']

                d = Device(**device)
                d.is_dep = True
                thread_session.add(d)

            except sqlalchemy.exc.StatementError as e:
                app.logger.error('Got a statement error trying to insert a DEP device: {}'.format(e))

        app.logger.debug('Last DEP Cursor was: %s', device_page['cursor'])
        dep_account.cursor = device_page.get('cursor', None)
        dep_account.more_to_follow = device_page.get('more_to_follow', None)
        dep_account.fetched_until = dateutil.parser.parse(device_page['fetched_until'])
        thread_session.commit()


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

            try:
                dep_fetch_devices(app, dep, dep_account.id)
            except DEPServiceError as dse:
                print(dse)
                if dse.text == 'EXPIRED_CURSOR':
                    app.logger.info("Sync cursor had expired, clearing for next run...")
                    dep_account.cursor = None
                    db.session.add(dep_account)
                    db.session.commit()

        except sqlalchemy.orm.exc.NoResultFound:
            app.logger.info('Not attempting a DEP sync, no account configured.')

