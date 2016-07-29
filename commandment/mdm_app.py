'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import base64
from .push import push_to_device
from .mdm.actions import do_mdm_payload, do_checkin, do_mdm, do_send_dev_info, do_app_manifest, do_app_download, do_enroll
from .mdm.utils import parse_plist_input_data
from .mdm.device import device_cert_check
from .models import Device
from .database import db_session
from flask import Blueprint, render_template, request, current_app

mdm_app = Blueprint('mdm_app', __name__)

@mdm_app.route('/')
def index():
    """Show enrolment page"""
    return render_template('enroll.html')

@mdm_app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    """Accept request from device to enroll it"""
    if request.method == 'POST' and \
            request.headers.get('Content-type', '').lower() == \
                'application/pkcs7-signature':

        do_enroll(base64.b64encode(request.data))

    return do_mdm_payload()

@mdm_app.route('/send_mdm/<int:dev_id>')
def send_mdm(dev_id):
    """Send a push notification"""
    device = db_session.query(Device).filter(Device.id == dev_id).one()
    push_to_device(device)
    return 'Sent Push Notification'

@mdm_app.route("/checkin", methods=['PUT'])
@device_cert_check(no_device_okay=True)
@parse_plist_input_data
def checkin():
    """Check in from device"""
    return do_checkin()

@mdm_app.route("/mdm", methods=['PUT'])
@device_cert_check()
@parse_plist_input_data
def mdm():
    """Perform MDM actions"""
    return do_mdm()

@mdm_app.route('/send_dev_info/<int:dev_id>')
def send_dev_info(dev_id):
    """Request device info from device"""
    return do_send_dev_info(dev_id)

@mdm_app.route("/app/<int:app_id>/manifest")
def app_manifest(app_id):
    """Get manifest for an app"""
    return do_app_manifest(app_id)

@mdm_app.route("/app/<int:app_id>/download/<filename>")
def app_download(app_id, filename):
    """Instruct the device to download an app"""
    return do_app_download(app_id, filename)
