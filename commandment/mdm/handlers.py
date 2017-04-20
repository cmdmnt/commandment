from flask import current_app
from ..models import db, Device, InstalledApplication, InstalledCertificate
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
    responses = response['SecurityInfo']
    

@command_router.route('ProfileList')
def ack_profile_list(request: ProfileList, device: Device, response: dict):
    responses = response['ProfileList']
    # for profile in responses:
    #     p =


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
    for a in device.installed_applications:
        db.session.delete(a)

    applications = response['InstalledApplicationList']
    current_app.logger.debug(
        'Received InstalledApplicationList response containing {} application(s)'.format(len(applications))
    )

    for app in applications:
        dba = InstalledApplication()
        dba.device = device
        dba.device_udid = device.udid
        dba.bundle_identifier = app.get('BundleIdentifier', None)
        dba.bundle_size = app.get('BundleSize', None)
        dba.dynamic_size = app.get('DynamicSize', None)
        dba.is_validated = app.get('IsValidated', None)
        dba.name = app.get('Name', None)
        dba.short_version = app.get('ShortVersion', None)
        dba.version = app.get('Version', None)
        db.session.add(dba)

    db.session.commit()

