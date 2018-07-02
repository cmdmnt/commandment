from binascii import hexlify
import uuid

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from flask import current_app

from commandment.mdm import commands
from commandment.mdm.app import command_router
from .commands import ProfileList, DeviceInformation, SecurityInfo, InstalledApplicationList, CertificateList, \
    InstallProfile, AvailableOSUpdates, InstallApplication
from .response_schema import InstalledApplicationListResponse, DeviceInformationResponse, AvailableOSUpdateListResponse, \
    ProfileListResponse, SecurityInfoResponse
from ..models import db, Device, Command as DBCommand
from commandment.inventory.models import InstalledCertificate, InstalledProfile, InstalledApplication

Queries = DeviceInformation.Queries


@command_router.route('DeviceInformation')
def ack_device_information(request: DeviceInformation, device: Device, response: dict):
    """Acknowledge a ``DeviceInformation`` response.

    Args:
        request (DeviceInformation): The command instance that generated this response.
        device (Device): The device responding to the command.
        response (dict): The raw response dictionary, de-serialized from plist.
    Returns:
        void: Reserved for future use

    See Also:
        - `DeviceInformation Command <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/3-MDM_Protocol/MDM_Protocol.html#//apple_ref/doc/uid/TP40017387-CH3-SW15>`_.
    """
    schema = DeviceInformationResponse()
    result = schema.load(response)
    for k, v in result.data['QueryResponses'].items():
        setattr(device, k, v)

    db.session.commit()


@command_router.route('SecurityInfo')
def ack_security_info(request: SecurityInfo, device: Device, response: dict):
    schema = SecurityInfoResponse()
    result = schema.load(response)


    db.session.commit()


@command_router.route('ProfileList')
def ack_profile_list(request: ProfileList, device: Device, response: dict):
    """Acknowledge a ``ProfileList`` response.
    
    Args:
        request (ProfileList): The command instance that generated this response.
        device (Device): The device responding to the command.
        response (dict): The raw response dictionary, de-serialized from plist.
    Returns:
          void: Reserved for future use
    """
    schema = ProfileListResponse()
    profile_list = schema.load(response)

    for pl in device.installed_payloads:
        db.session.delete(pl)

    # Impossible to calculate delta, so all profiles get wiped
    for p in device.installed_profiles:
        db.session.delete(p)

    desired_profiles = {}
    # for tag in device.tags:
    #     for p in tag.profiles:
    #         desired_profiles[p.uuid] = p

    remove_profiles = []

    for profile in profile_list.data['ProfileList']:
        profile.device = device

        # device.udid may have dashes (macOS) or not (iOS)
        profile.device_udid = device.udid

        for payload in profile.payload_content:
            payload.device = device
            payload.profile_id = profile.id

        db.session.add(profile)

        # Reconcile profiles which should be installed
        if profile.payload_uuid in desired_profiles:
            del desired_profiles[profile.payload_uuid]
        else:
            remove_profiles.append(profile)

    # Queue up some desired profiles
    for puuid, p in desired_profiles.items():
        c = commands.InstallProfile(None, profile=p)
        dbc = DBCommand.from_model(c)
        dbc.device = device
        db.session.add(dbc)

    # for remove_profile in remove_profiles:
    #     c = commands.RemoveProfile(None, Identifier=remove_profile.payload_identifier)
    #     dbc = DBCommand.from_model(c)
    #     dbc.device = device
    #     db.session.add(dbc)

    db.session.commit()


@command_router.route('CertificateList')
def ack_certificate_list(request: CertificateList, device: Device, response: dict):
    for c in device.installed_certificates:
        db.session.delete(c)

    certificates = response['CertificateList']
    current_app.logger.debug(
        'Received CertificatesList response containing {} certificate(s)'.format(len(certificates)))

    for cert in certificates:
        ic = InstalledCertificate()
        ic.device = device
        ic.device_udid = device.udid

        ic.x509_cn = cert.get('CommonName', None)
        ic.is_identity = cert.get('IsIdentity', None)

        der_data = cert['Data']
        certificate = x509.load_der_x509_certificate(der_data, default_backend())
        ic.fingerprint_sha256 = hexlify(certificate.fingerprint(hashes.SHA256()))  # TODO: hexlify?
        ic.der_data = der_data

        db.session.add(ic)

    db.session.commit()


@command_router.route('InstalledApplicationList')
def ack_installed_app_list(request: InstalledApplicationList, device: Device, response: dict):
    """Acknowledge a response to ``InstalledApplicationList``.
    
    .. note:: There is no composite key which can uniquely identify an item in the installed applications list.
        Some applications may not contain any version information at all. For this reason, the entire list of installed
        applications is cleared before inserting a new list.
        
    Args:
          request (InstalledApplicationList): An instance of the command that generated this response from the managed
            device.
          device (Device): The device responding
          response (dict): The dictionary containing the parsed plist response from the device.
    Returns:
          void: Nothing is returned but this behaviour is subject to change.
    """

    for a in device.installed_applications:
        db.session.delete(a)

    applications = response['InstalledApplicationList']
    current_app.logger.debug(
        'Received InstalledApplicationList response containing {} application(s)'.format(len(applications))
    )

    schema = InstalledApplicationListResponse()
    result, errors = schema.load(response)
    current_app.logger.debug(errors)
    current_app.logger.info(result)

    for ia in result['InstalledApplicationList']:
        if isinstance(ia, db.Model):
            ia.device = device
            ia.device_udid = device.udid
            db.session.add(ia)
        else:
            current_app.logger.debug('Not a model: %s', ia)

    db.session.commit()


@command_router.route('InstallProfile')
def ack_install_profile(request: InstallProfile, device: Device, response: dict):
    """Acknowledge a response to ``InstallProfile``."""
    if response.get('Status', None) == 'Error':
        pass


@command_router.route('AvailableOSUpdates')
def ack_available_os_updates(request: AvailableOSUpdates, device: Device, response: dict):
    """Acknowledge a response to AvailableOSUpdates"""
    for au in device.available_os_updates:
        db.session.delete(au)

    schema = AvailableOSUpdateListResponse()
    result = schema.load(response)

    for upd in result.data['AvailableOSUpdates']:
        upd.device = device
        db.session.add(upd)

    db.session.commit()


@command_router.route('InstallApplication')
def ack_install_application(request: InstallApplication, device: Device, response: dict):
    """Acknowledge a response to InstallApplication. Usually just contains Queued: True/False"""
    pass
