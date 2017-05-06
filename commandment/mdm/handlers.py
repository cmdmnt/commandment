from flask import current_app
from ..models import db, Device, InstalledApplication, InstalledCertificate, InstalledProfile
from .response_schema import InstalledApplicationListResponse
from ..profiles.models import Profile
from .commands import ProfileList, DeviceInformation, SecurityInfo, InstalledApplicationList, CertificateList
from ..mdm_app import command_router
from .util import queryresponses_to_query_set
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from binascii import hexlify

Queries = DeviceInformation.Queries


@command_router.route('DeviceInformation')
def ack_device_information(request: DeviceInformation, device: Device, response: dict):
    responses = response['QueryResponses']
    qs = queryresponses_to_query_set(responses)

    if Queries.AvailableDeviceCapacity in qs:
        device.available_device_capacity = qs[Queries.AvailableDeviceCapacity]

    if Queries.DeviceCapacity in qs:
        device.device_capacity = qs[Queries.DeviceCapacity]

    if Queries.LocalHostName in qs:
        device.local_hostname = qs[Queries.LocalHostName]

    if Queries.HostName in qs:
        device.hostname = qs[Queries.HostName]

    if Queries.BluetoothMAC in qs:
        device.bluetooth_mac = qs[Queries.BluetoothMAC]

    if Queries.WiFiMAC in qs:
        device.wifi_mac = qs[Queries.WiFiMAC]

    db.session.commit()


@command_router.route('SecurityInfo')
def ack_security_info(request: SecurityInfo, device: Device, response: dict):
    sinfo = response['SecurityInfo']
    device.passcode_present = sinfo.get('PasscodePresent', None)
    device.passcode_compliant = sinfo.get('PasscodeCompliant', None)
    device.passcode_compliant_with_profiles = sinfo.get('PasscodeCompliantWithProfiles', None)
    device.fde_enabled = sinfo.get('FDE_Enabled', None)
    device.fde_has_prk = sinfo.get('FDE_HasPersonalRecoveryKey', None)
    device.fde_has_irk = sinfo.get('FDE_HasInstitutionalRecoveryKey', None)
    device.sip_enabled = sinfo.get('SystemIntegrityProtectionEnabled', None)

    if 'FirewallSettings' in sinfo:
        fw = sinfo['FirewallSettings']
        device.firewall_enabled = fw.get('FirewallEnabled', None)
        device.block_all_incoming = fw.get('BlockAllIncoming', None)
        device.stealth_mode_enabled = fw.get('StealthMode', None)

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
    profiles = response['ProfileList']
    
    for profile in profiles:
        ip = InstalledProfile()
        ip.device = device
        ip.device_udid = device.udid

        ip.has_removal_password = profile.get('HasRemovalPasscode', None)
        ip.is_encrypted = profile.get('IsEncrypted', None)

        ip.payload_description = profile.get('PayloadDescription', None)
        ip.payload_display_name = profile.get('PayloadDisplayName', None)
        ip.payload_identifier = profile.get('PayloadIdentifier', None)
        ip.payload_organization = profile.get('PayloadOrganization', None)
        ip.payload_removal_disallowed = profile.get('PayloadRemovalDisallowed', None)
        ip.payload_uuid = profile.get('PayloadUUID', None)

        # TODO: SignerCertificates
        # TODO: Payloads
        db.session.add(ip)

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
    result = schema.load(response)

    for app in result.data['InstalledApplicationList']:
        app.device = device
        app.device_udid = device.udid
        db.session.add(app)


    # for app in applications:
    #     dba = InstalledApplication()
    #     dba.device = device
    #     dba.device_udid = device.udid
    #     dba.bundle_identifier = app.get('BundleIdentifier', None)
    #     dba.bundle_size = app.get('BundleSize', None)
    #     dba.dynamic_size = app.get('DynamicSize', None)
    #     dba.is_validated = app.get('IsValidated', None)
    #     dba.name = app.get('Name', None)
    #     dba.short_version = app.get('ShortVersion', None)
    #     dba.version = app.get('Version', None)
    #     db.session.add(dba)

    db.session.commit()

