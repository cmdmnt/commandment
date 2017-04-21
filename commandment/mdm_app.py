"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from flask import Blueprint, make_response, abort
from flask import current_app, send_file, g
import base64
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .models import db, Device, Command as DBCommand
from .models import App, Organization, SSLCertificate
from .mdm import CommandStatus
from .mdm.commands import Command
from .decorators import device_cert_check, parse_plist_input_data
from .routers import CommandRouter, PlistRouter
from os import urandom
import plistlib
from .push import push_to_device
import os
from datetime import datetime
from .signals import device_enrolled

TRUST_DEV_PROVIDED_CERT = True

mdm_app = Blueprint('mdm_app', __name__)

plr = PlistRouter(mdm_app, '/checkin')
command_router = CommandRouter(mdm_app)
from .mdm import handlers


@plr.route('MessageType', 'Authenticate')
def authenticate(plist_data):
    """Handle the `Authenticate` message.
    
    This will be the first message sent to the MDM upon enrollment, but you cannot consider the device to be enrolled
    at this stage.
    """
    # TODO: check to make sure device == UDID == cert, etc.
    try:
        device = db.session.query(Device).filter(Device.udid == plist_data['UDID']).one()
    except NoResultFound:
        # no device found, let's make a new one!
        device = Device()
        db.session.add(device)

        device.udid = plist_data['UDID']
        device.build_version = plist_data.get('BuildVersion')
        device.device_name = plist_data.get('DeviceName')
        device.model = plist_data.get('Model')
        device.model_name = plist_data.get('ModelName')
        device.os_version = plist_data.get('OSVersion')
        device.product_name = plist_data.get('ProductName')
        device.serial_number = plist_data.get('SerialNumber')
        device.topic = plist_data.get('Topic')

    # remove the previous device token (in the case of a re-enrollment) to
    # tell the difference between a periodic TokenUpdate and the first
    # post-enrollment TokenUpdate
    device.token = None

    # TODO: we're essentially trusting the device to give the correct security infomration here
    #device.certificate = g.device_cert

    db.session.commit()

    return 'OK'


@plr.route('MessageType', 'TokenUpdate')
def token_update(plist_data):
    current_app.logger.info('TokenUpdate received')

    # TODO: a TokenUpdate can either be for a device or a user (per OS X extensions)
    if 'UserID' in plist_data:
        current_app.logger.warn('per-user TokenUpdate not yet implemented, skipping')
        return 'OK'

    # TODO: check to make sure device == UDID == cert, etc.
    device = db.session.query(Device).filter(Device.udid == plist_data['UDID']).one()

    if not device.token:
        device.is_enrolled = True
        device_enrolled.send(device)

    device.tokenupdate_at = datetime.utcnow()

    # device.certificate = g.device_cert

    if 'PushMagic' in plist_data:
        device.push_magic = plist_data['PushMagic']

    if 'Topic' in plist_data:
        device.topic = plist_data['Topic']

    if 'Token' in plist_data:
        device.token = plist_data['Token']
    else:
        current_app.logger.error('TokenUpdate message missing Token')
        abort(400, 'invalid data supplied')

    if 'UnlockToken' in plist_data:
        device.unlock_token = plist_data['UnlockToken']

    db.session.commit()
    return 'OK'


@plr.route('MessageType', 'UserAuthenticate')
def user_authenticate(plist_data):
    abort(410, 'per-user authentication not yet supported')


@plr.route('MessageType', 'CheckOut')
def check_out(plist_data):
    """Handle the `CheckOut` message.
    
    Todo:
        - Handle CheckOuts for the user channel.
    """
    device_udid = plist_data['UDID']
    try:
        d = db.session.query(Device).filter(Device.udid == device_udid).one()
    except NoResultFound:
        current_app.logger.warning('Attempted to unenroll device with UDID: {}, but none was found'.format(device_udid))
        return abort(404, 'No matching device found')

    except MultipleResultsFound:
        current_app.logger.warning(
            'Attempted to unenroll device with UDID: {}, but there were multiple, check your database'.format(device_udid))
        return abort(500, 'Too many devices matching')

    d.last_seen = datetime.utcnow()
    d.is_enrolled = False

    # Make sure we cant even accidentally push to an invalid relationship
    d.token = None
    d.push_magic = None

    db.session.commit()
    current_app.logger.debug('Device has been unenrolled, UDID: {}'.format(device_udid))

    return 'OK'


#@device_cert_check()
@mdm_app.route("/mdm", methods=['PUT'])
@parse_plist_input_data
def mdm():
    """MDM connection endpoint.

    This endpoint delivers and handles incoming command responses.
    Such as: `Idle`, `NotNow`, `Acknowledged`.

    :reqheader Content-Type: application/x-apple-aspen-mdm; charset=UTF-8
    :reqheader Mdm-Signature: BASE64-encoded CMS Detached Signature of the message. (if `SignMessage` was true)
    :resheader Content-Type: application/xml; charset=UTF-8
    :status 200: With an empty body, no commands remaining, or plist contents of next command.
    :status 400: Invalid data submitted
    :status 410: User channel capability not available.
    """
    # TODO: proper identity verification, for now just matching on UDID
    device = db.session.query(Device).filter(Device.udid == g.plist_data['UDID']).one()

    # if g.device.udid != g.plist_data['UDID']:
    #     # see note in device_cert_check() about old device cert sometimes
    #     # being provided
    #     current_app.logger.info('provided UDID does not match device UDID')
    #     abort(400, 'invalid input data')

    if 'UserID' in g.plist_data:
        # Note that with DEP this is an opportune time to queue up an 
        # application install for the /device/ despite this being a per-user
        # MDM command. this is becasue DEP appears to only allow apps to be
        # installed while a user is logged in. note also the undocumented
        # NotOnConsole key to (possibly) indicate that this is a UI login?
        current_app.logger.warn('per-user MDM command not yet supported')
        return ''

    if 'Status' not in g.plist_data:
        current_app.logger.error('invalid MDM request (no Status provided) from device id %d' % device.id)
        abort(400, 'invalid input data')
    else:
        status = g.plist_data['Status']

    current_app.logger.info('device id=%d udid=%s processing status=%s', device.id, device.udid, status)
    device.last_seen = datetime.utcnow()
    db.session.commit()

    print(g.plist_data)

    if status != 'Idle':

        if 'CommandUUID' not in g.plist_data:
            current_app.logger.error('missing CommandUUID for non-Idle status')
            abort(400, 'invalid input data')

        try:
            command = DBCommand.find_by_uuid(g.plist_data['CommandUUID'])

            # update the status of this command and commit
            if status == 'Acknowledged':
                command.status = CommandStatus.Acknowledged.value
            elif status == 'NotNow':
                command.status = CommandStatus.NotNow.value
            elif status == 'Error':
                command.status = CommandStatus.Invalid.value
            else:
                current_app.logger.warning('unrecognised command status: {}'.format(status))

            command.acknowledged_at = datetime.utcnow()
            db.session.commit()

            # Re-hydrate the command class based on the persisted model containing the request type and the parameters
            # that were given to generate the command
            cmd = Command.new_request_type(command.request_type, command.parameters, command.uuid)

            # TODO: route the response to the correct handler
            current_app.logger.debug('Routing command handler')
            command_router.handle(cmd, device, g.plist_data)

        except NoResultFound:
            current_app.logger.info('no record of command uuid=%s', g.plist_data['CommandUUID'])

    if status == 'NotNow':
        current_app.logger.warn('NotNow status received, forgoing any further commands')
        return ''

    while True:
        command = DBCommand.get_next_device_command(device)

        if not command:
            break

        # mark this command as being in process right away to (try) to avoid
        # any race conditions with mutliple MDM commands from the same device
        # at a time

        #command.set_processing()
        #db.session.commit()

        # Re-hydrate the command class based on the persisted model containing the request type and the parameters
        # that were given to generate the command
        cmd = Command.new_request_type(command.request_type, command.parameters, command.uuid)


        # get command dictionary representation (e.g. the full command to send)
        output_dict = cmd.to_dict()

        current_app.logger.info('sending %s MDM command class=%s to device=%d', cmd.request_type,
                                command.request_type, device.id)

        # convert to plist and send
        resp = make_response(plistlib.dumps(output_dict))
        resp.headers['Content-Type'] = 'application/xml'

        # finally set as sent
        command.status = CommandStatus.Sent.value
        command.sent_at = datetime.utcnow()
        db.session.commit()

        return resp

    current_app.logger.info('no further MDM commands for device=%d', device.id)
    # return empty response as we have no further work
    return ''


# @mdm_app.route("/app/<int:app_id>/manifest")
# def app_manifest(app_id: int):
#     """Retrieve an application manifest for the specified application ID."""
#     app_q = db_session.query(App).filter(App.id == app_id)
#     app = app_q.one()
#
#     config = db_session.query(MDMConfig).one()
#
#     asset = {
#         'kind': 'software-package',
#         'md5-size': app.md5_chunk_size,
#         'md5s': app.md5_chunk_hashes.split(':'),
#         'url': '%s/app/%d/download/%s' % (config.base_url(), app_id, app.filename),
#     }
#
#     metadata = {'kind': 'software', 'title': app.filename, 'sizeInBytes': app.filesize}
#
#     pkgs_ids = app.pkg_ids_json
#     pkgs_bundles = [{'bundle-identifier': i[0], 'bundle-version': i[1]} for i in pkgs_ids]
#
#     # if subtitle:
#     #     metadata['subtitle'] = subtitle
#
#     metadata.update(pkgs_bundles[0])
#
#     if len(pkgs_bundles) > 1:
#         metadata['items'] = pkgs_bundles
#
#     download = {'assets': [asset, ], 'metadata': metadata}
#
#     manifest = {'items': [download]}
#
#     resp = make_response(plistlib.writePlistToString(manifest))
#     resp.headers['Content-Type'] = 'application/xml'
#     return resp
#
#
# @mdm_app.route("/app/<int:app_id>/download/<filename>")
# def app_download(app_id: int, filename: str):
#     """Download a file corresponding to the specified application ID."""
#     app_q = db_session.query(App).filter(App.id == app_id)
#     app = app_q.one()
#
#     return send_file(os.path.join(current_app.config['APP_UPLOAD_ROOT'], app.path_format()))

#
# cr = CommandRouter(mdm_app, '/mdm')
#
# @cr.route('ProfileList')
# def profile_list(request: Command, response: dict):
#     """Acknowledge a response to a ProfileList command.
#
#     Args:
#           request (Command): The ProfileList command that was issued
#           response (dict): The parsed plist data that was returned by the mdm client.
#     """
#     pass

