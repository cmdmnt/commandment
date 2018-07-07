from typing import Tuple
import logging
import threading
from datetime import datetime
import dateutil.parser
from flask import Flask
import ssl

from commandment.mdm import CommandStatus
from commandment.models import db, Device, Command
from commandment.apns.push import push_to_device
import sqlalchemy.orm.exc
from sqlalchemy import func

push_thread = None
push_start = 2
push_time = 90
push_thread_stopped = threading.Event()

logger = logging.getLogger('push thread')


def start(app: Flask):
    """Start the APNS Pusher thread"""

    logger.info('PUSH thread will start in %d second(s). polling at intervals of %d second(s).', push_start, push_time)
    push_thread = threading.Timer(push_start, push_thread_callback, [app])
    push_thread.daemon = True
    push_thread.start()


def stop():
    """Stop the APNS Pusher thread"""
    logger.info('PUSH thread will stop')
    push_thread_stopped.set()

    global push_thread
    if push_thread is threading.Timer:
        push_thread.cancel()


def push_thread_callback(app: Flask):
    """Process outstanding MDM commands by issuing a push to device(s).

    TODO: A push with no response needs an exponential backoff time.

    Commands that are ready to send must satisfy these criteria:

    - Command is in Queued state.
    - Command.after is null.
    - Command.ttl is not zero.
    - Device is enrolled (is_enrolled)
    """
    while not push_thread_stopped.wait(push_time):
        app.logger.info('Push Thread checking for outstanding commands...')
        with app.app_context():
            pending: Tuple[Device, int] = db.session.query(Device, func.Count(Command.id)).\
                filter(Device.id == Command.device_id).\
                filter(Command.status == CommandStatus.Queued).\
                filter(Command.ttl > 0).\
                filter(Command.after == None).\
                filter(Device.is_enrolled == True).\
                group_by(Device.id).\
                all()

            for d, c in pending:
                app.logger.info('PENDING: %d command(s) for device UDID %s', c, d.udid)

                if d.token is None or d.push_magic is None:
                    app.logger.warn('Cannot request push on a device that has no device token or push magic')
                    continue

                try:
                    response = push_to_device(d)
                except ssl.SSLError:
                    return stop()

                app.logger.info("[APNS2 Response] Status: %d, Reason: %s, APNS ID: %s, Timestamp",
                                        response.status_code, response.reason, response.apns_id.decode('utf-8'))
                d.last_push_at = datetime.utcnow()
                if response.status_code == 200:
                    d.last_apns_id = response.apns_id

            db.session.commit()
