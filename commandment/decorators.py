from functools import wraps
from flask import request, abort, current_app, g
from cryptography import x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
import plistlib


def device_cert_check(no_device_okay=False):
    """Performs a set of checks on a request to make sure it came from a
    legitimately enrolled device in this MDM system"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # check if valid certificate and if request data matches signature
            # TODO: implement alternate methods of getting supplied client cert
            # (e.g. request.headers['X-Ssl-Client-Cert'].replace('\n ', '\n') for
            # nginx)
            # pkcs7_pem_sig = base64_to_pem('PKCS7', request.headers['Mdm-Signature'])
            # device_supplied_cert = verify_mdm_signature(pkcs7_pem_sig, request.data)
            #
            # try:
            #     dev_cert_fprint = Certificate.from_pem(device_supplied_cert).get_fingerprint()
            #     g.device_cert = db_session.query(DBCertificate).filter(DBCertificate.fingerprint == dev_cert_fprint).one()
            # except NoResultFound:
            #     current_app.logger.info('supplied device certificate not found; returning invalid')
            #     abort(400, 'certificate invalid')

            # get a list of the devices that correspond to this certificate
            cert_devices = g.device_cert.devices

            if len(cert_devices) > 1:
                dev_id_list = ', '.join([i.id for i in cert_devices])
                current_app.logger.info(
                    'certificate has more than one device assigned (%s); returning invalid' % dev_id_list)
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

            return f(*args, **kwargs)

        return wrapper

    return decorator


def parse_plist_input_data(f):
    """Parses plist data as HTTP input from request"""

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if current_app.debug:
                current_app.logger.debug(request.data)
            g.plist_data = plistlib.loads(request.data)
        except:
            current_app.logger.info('could not parse property list input data')
            abort(400, 'invalid input data')

        return f(*args, **kwargs)

    return decorator


def pem_certificate_upload(f):
    """Parse PEM formatted certificate in request data
    
    TODO: form field name option
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            certificate_data = request.files['file'].read()
            g.certificate = x509.load_pem_x509_certificate(certificate_data, backend=default_backend())
        except UnsupportedAlgorithm as e:
            current_app.logger.info('could not parse PEM certificate data')
            abort(400, 'invalid input data')

        return f(*args, **kwargs)

    return decorator

