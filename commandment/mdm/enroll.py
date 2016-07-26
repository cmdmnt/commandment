"""mdm app module: Controller logic for MDM Blueprint"""

from flask import current_app
import json
from ..database import db_session, NoResultFound, or_
from ..models import Device

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

def enroll_from_plist(plist):
    """Use a registration plist to enroll a device."""

    try:
        device = db_session.query(Device).filter(or_(Device.serial_number == plist['SERIAL'], Device.udid == plist['UDID'])).one()
        # assign in case absent (UDID present only - not likely due to spec)
        device.serial_number = plist['SERIAL']
        # assign in case different (e.g. changing serial UDIDs i.e. VM testing)
        device.udid = plist['UDID']
    except NoResultFound:
        # should never get here, we could take benefit of the doubt and
        # allow the enrollment anyway, though..?
        current_app.logger.warn('DEP enrollment attempt but no serial number nor UDID found!')

        device = Device()
        device.serial_number = plist['SERIAL']
        device.udid = plist['UDID']
        # TODO: do we care about PRODUCT, VERSION, or LANGUAGE here?

        db_session.add(device)
        db_session.commit()
    # TODO: except too many results (e.g. perhaps both a UDID and a SERIAL found?)

    notify_enrolled(device.udid)
    notify_serial_first_received(device.udid, device.serial_number)

    return device

def notify_enrolled(udid):
    """Raise an event in Redis channel for first UDID receipt"""

    current_app.logger.info("Publish Redis commandment.enroll for %s" % udid)
    current_app.redis_store.publish('commandment.enroll', json.dumps({
        'udid': udid
    }))

def notify_serial_first_received(udid, serial_number):
    """Raise an event in Redis channel for first receipt of a serial number"""

    current_app.logger.info("Publish Redis commandment.serial for %s :: %s" % (udid, serial_number))
    current_app.redis_store.publish('commandment.serial', json.dumps({
        'udid': udid,
        'serial_number': serial_number
    }))
