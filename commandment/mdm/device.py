"""mdm app module: Controller logic for MDM Blueprint"""

import sys
import os
import plistlib
import xml.parsers.expat

from functools import wraps
from M2Crypto import SMIME, BIO, X509
from flask import current_app, request, g, abort, make_response, send_file
from sqlalchemy.sql.expression import true

from . import enroll
from ..pki.x509 import Certificate
from ..database import db_session, NoResultFound, or_, and_
from ..profiles.mdm import MDMPayload
from ..models import App, app_group_assoc, SCEPConfig, Device, Certificate as DBCertificate, MDMGroup, MDMConfig, QueuedCommand, ProfileStatus
from ..mdmcmds.dep import DeviceConfigured
from ..pki.ca import PushCertificate
from ..push import push_to_device
from ..profiles import Profile
from ..profiles.cert import PKCS12CertificatePayload, PEMCertificatePayload, SCEPPayload
from ..mdmcmds import InstallProfile, AppInstall, UpdateInventoryDevInfoCommand, find_mdm_command_class
from .utils import base64_to_pem, verify_mdm_signature

def device_cert_check(no_device_okay=False):
    """Performs a set of checks on a request to make sure it came from a
    legimately enrolled device in this MDM system"""
    def decorator(func):
        """Decorator for checking certs prior to request handler."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Actual wrapper the we give to the request handler."""
            # check if valid certificate and if request data matches signature
            # TODO: implement alternate methods of getting supplied client cert
            # (e.g. request.headers['X-Ssl-Client-Cert'].replace('\n ', '\n') for 
            # nginx)
            pkcs7_pem_sig = base64_to_pem('PKCS7', request.headers['Mdm-Signature'])
            device_supplied_cert = verify_mdm_signature(pkcs7_pem_sig, request.data)

            try:
                dev_cert_fprint = Certificate.from_pem(device_supplied_cert).get_fingerprint()
                g.device_cert = db_session.query(DBCertificate).filter(DBCertificate.fingerprint == dev_cert_fprint).one()
            except NoResultFound:
                current_app.logger.info('supplied device certificate not found; returning invalid')
                abort(400, 'certificate invalid')

            # get a list of the devices that correspond to this certificate
            cert_devices = g.device_cert.devices

            if len(cert_devices) > 1:
                dev_id_list = ', '.join([i.id for i in cert_devices])
                current_app.logger.info('certificate has more than one device assigned (%s); returning invalid' % dev_id_list)
                abort(500, 'certificate configuration invalid')
            elif len(cert_devices) < 1 and no_device_okay is not True:
                current_app.logger.info('certificate has no associated device; returning invalid')
                abort(400, 'certificate invalid')

            # NOTE: we've seen on odd circumstance where the provided device UDID
            # does not match the currently enrolled certificate (and thus device
            # UDID). this appears to be some weird certificate caching problem
            # on the client side there the client tries to auth with it's
            # previously enrolled cert when one removes/re-enrolls a device
            # quickly
            if len(cert_devices) == 1:
                g.device = g.device_cert.devices[0]
            else:
                g.device = None

            return func(*args, **kwargs)
        return wrapper
    return decorator

def device_first_post_enroll(device, awaiting=False):
    """Get device information after enrolment"""
    print 'enroll:', 'UpdateInventoryDevInfoCommand'
    db_session.add(UpdateInventoryDevInfoCommand.new_queued_command(device))

    # install all group profiles
    for group in device.mdm_groups:
        for profile in group.profiles:
            if profile.status == ProfileStatus.ACTIVE:
                print "Installing profile ", profile.id
                db_session.add(InstallProfile.new_queued_command(device, {'id': profile.id}))

    if awaiting:
        # in DEP Await state, send DeviceConfigured to proceed with setup
        db_session.add(DeviceConfigured.new_queued_command(device))

    db_session.commit()

    push_to_device(device)

def device_first_user_message(device):
    """Queue the MDM commands appropriate for a first-user-message seen
    event. Currently used to inititate DEP app installations."""

    device.first_user_message_seen = True

    for group in device.mdm_groups:
        app_q = db_session.query(App).join(
            app_group_assoc,
            and_(app_group_assoc.c.mdm_group_id == group.id, app_group_assoc.c.app_id == App.id)
        ).filter(
            app_group_assoc.c.install_early == true()
        )

        for app in app_q:
            db_session.add(AppInstall.new_queued_command(device, {'id': app.id}))

    db_session.commit()

    push_to_device(device)

