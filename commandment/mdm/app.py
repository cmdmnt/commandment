"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from flask import Blueprint, make_response, abort, jsonify, g, current_app
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from commandment.mdm import CommandStatus
from commandment.mdm.commands import Command
from commandment.decorators import parse_plist_input_data
from commandment.cms.decorators import verify_mdm_signature
from commandment.mdm.util import queue_full_inventory
from commandment.models import DeviceUser, DeviceIdentityCertificate
from commandment.mdm.routers import CommandRouter, PlistRouter
from commandment.utils import plistify
import plistlib
from datetime import datetime
from commandment.signals import device_enrolled


mdm_app = Blueprint('mdm_app', __name__)

plr = PlistRouter(mdm_app, '/checkin')
command_router = CommandRouter(mdm_app)
from .handlers import *


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
        device.last_seen = datetime.now()

    # Authenticate message is not enough to be enrolled
    device.is_enrolled = False

    # remove the previous device token (in the case of a re-enrollment) to
    # tell the difference between a periodic TokenUpdate and the first
    # post-enrollment TokenUpdate
    device.token = None

    # TODO: Check supplied identity against identities we actually issued

    db.session.commit()

    return 'OK'


@plr.route('MessageType', 'TokenUpdate')
@verify_mdm_signature
def token_update(plist_data):
    current_app.logger.debug('TokenUpdate (UDID %s)', plist_data.get('UDID', None))
    try:
        device = db.session.query(Device).filter(Device.udid == plist_data['UDID']).one()
    except NoResultFound:
        current_app.logger.debug(
            'Device (UDID: %s) will be unenrolled because the database has no record of this device.', plist_data['UDID'])
        return abort(410)  # Ask the device to unenroll itself because we dont seem to have any records.

    # TODO: a TokenUpdate can either be for a device or a user (per OS X extensions)
    if 'UserID' in plist_data:
        device_user = DeviceUser(
            
        )
        return 'OK'

    if not device.token:  # First contact
        device.is_enrolled = True

        if hasattr(g, 'signers'):
            device_certificate = DeviceIdentityCertificate.from_crypto(g.signers[0])
            db.session.add(device_certificate)
            device.certificate = device_certificate
        else:
            pass  # TODO: if in debug mode this should not throw an exception to deal with cert troubleshooting

        device_enrolled.send(device)
        queue_full_inventory(device)

    device.tokenupdate_at = datetime.utcnow()
    device.push_magic = plist_data.get('PushMagic', None)
    device.topic = plist_data.get('Topic', None)
    device.token = plist_data.get('Token', None)
    device.unlock_token = plist_data.get('UnlockToken', None)
    device.last_seen = datetime.now()
    db.session.commit()

    # TODO: DRY
    command = DBCommand.next_command(device)

    if not command:
        current_app.logger.info('no further MDM commands for device=%d', device.id)
        return ''

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

    current_app.logger.debug(output_dict)

    command.status = CommandStatus.Sent
    command.sent_at = datetime.utcnow()
    db.session.commit()

    return plistify(output_dict)


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


@mdm_app.route("/mdm", methods=['PUT'])
@verify_mdm_signature
@parse_plist_input_data
def mdm():
    """MDM connection endpoint.

    Most MDM communication is via this URI.

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
    try:
        device = db.session.query(Device).filter(Device.udid == g.plist_data['UDID']).one()
    except NoResultFound:
        current_app.logger.info("An unmanaged device (UDID %s), tried to check in with us, rejecting.", g.plist_data['UDID'])
        return abort(410)  # Unmanage devices that we dont have a record of

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
        return abort(400, 'response does not contain Status')
    else:
        status = CommandStatus(g.plist_data['Status'])

    current_app.logger.info('device id=%d udid=%s processing status=%s', device.id, device.udid, status)
    device.last_seen = datetime.utcnow()
    db.session.commit()

    if current_app.config['DEBUG']:
        try:
            print(g.plist_data)
        except UnicodeEncodeError:
            print('Cannot DEBUG print plist request, unencodable characters')

    if status != CommandStatus.Idle:  # this device is responding to an earlier command.
        if 'CommandUUID' not in g.plist_data:
            current_app.logger.error('missing CommandUUID for non-Idle status')
            abort(400, 'response does not contain CommandUUID')
        try:
            command = DBCommand.find_by_uuid(g.plist_data['CommandUUID'])
            command.status = status
            command.acknowledged_at = datetime.utcnow()
            db.session.commit()

            # Re-hydrate the command class based on the persisted model containing the request type and the parameters
            # that were given to generate the command
            cmd = Command.new_request_type(command.request_type, command.parameters, command.uuid)

            # route the response by the handler type corresponding to that command
            command_router.handle(cmd, device, g.plist_data)

        except NoResultFound:
            current_app.logger.warning('no record of command uuid=%s', g.plist_data['CommandUUID'])

    if status == CommandStatus.NotNow:
        current_app.logger.warn('NotNow status received, forgoing any further commands')
        return ''

    command = DBCommand.next_command(device)

    if not command:
        current_app.logger.info('no further MDM commands for device=%d', device.id)
        return ''

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

    current_app.logger.debug(output_dict)

    command.status = CommandStatus.Sent
    command.sent_at = datetime.utcnow()
    db.session.commit()

    return plistify(output_dict)


