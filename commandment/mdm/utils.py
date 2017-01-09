import sys
import os
import plistlib
import xml.parsers.expat

from functools import wraps
from flask import current_app, request, g, abort, make_response, send_file
from sqlalchemy.sql.expression import true

from ..pki.x509 import Certificate
from ..database import db_session, NoResultFound, or_, and_
from ..profiles.mdm import MDMPayload
from ..mdmcmds.dep import DeviceConfigured
from ..models import App, app_group_assoc, SCEPConfig, Device, Certificate as DBCertificate, MDMGroup, MDMConfig, QueuedCommand
from ..pki.ca import get_ca, PushCertificate
from ..push import push_to_device
from ..profiles import Profile
from ..profiles.cert import PKCS12CertificatePayload, PEMCertificatePayload, SCEPPayload
from ..mdmcmds import InstallProfile, AppInstall, UpdateInventoryDevInfoCommand, find_mdm_command_class
from M2Crypto import SMIME, BIO, X509
from ..pki.ca import get_ca

def base64_to_pem(crypto_type, b64_text, width=76):
    """Convert a base64 device response to a PEM."""
    lines = ''
    for pos in xrange(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)

def verify_mdm_signature(mdm_sig, req_data):
    """Verify the client's supplied MDM signature and return the client certificate included in the signature."""

    p7_bio = BIO.MemoryBuffer(str(mdm_sig))
    pkcs7 = SMIME.load_pkcs7_bio(p7_bio)

    p7_signers = pkcs7.get0_signers(X509.X509_Stack())

    mdm_ca = get_ca()

    # can probably directly use m2 certificate here
    ca_x509_bio = BIO.MemoryBuffer(mdm_ca.get_cacert().to_pem())
    ca_x509 = X509.load_cert_bio(ca_x509_bio)

    cert_store = X509.X509_Store()
    cert_store.add_x509(ca_x509)

    signer = SMIME.SMIME()
    signer.set_x509_store(cert_store)
    signer.set_x509_stack(p7_signers)

    # NOTE: may need to do something special if we can't cleanly convert
    # to string from Unicode. must be byte-accurate as the signature won't
    # match otherwise
    data_bio = BIO.MemoryBuffer(req_data)

    # will raise an exception if verification fails
    # if no CA certificate we get an:
    #   PKCS7_Error: certificate verify error
    signer.verify(pkcs7, data_bio)

    return p7_signers[0].as_pem()

def plist_from_pkcs7(pkcs7):
    """Extract a plist from PKCS7 encoded data."""
    # DEP request

    # base64 encode the DER data, and wrap in a PEM-ish format for SMIME.load_pkcs7_bio()
    req_data = base64_to_pem('PKCS7', pkcs7)

    p7_bio = BIO.MemoryBuffer(str(req_data))
    pkcs7 = SMIME.load_pkcs7_bio(p7_bio)

    p7_signers = pkcs7.get0_signers(X509.X509_Stack())

    signer = SMIME.SMIME()
    signer.set_x509_store(X509.X509_Store())
    signer.set_x509_stack(p7_signers)

    # TODO/XXX: not verifying ANY certificates!
    #
    # spec says we should verify against the "Apple Root CA" and that this
    # CMS message contains all intermediates to do that verification.
    # M2Crypto has no way to get at all the intermediate certificates to
    # do this manually we'd need to extract all of the certificates and
    # verify the chain aginst it. Note as of 2016-03-14 on a brand new
    # iPad Apple was including an expired certificate in this chain. Note
    # also that at least one of the intermediate certificates had a
    # certificate purpose apparently not appropraite for CMS/SMIME
    # verification. For now just verify with no CA and skip any
    # verification.
    plist_text = signer.verify(pkcs7, None, flags=SMIME.PKCS7_NOVERIFY)

    plist = plistlib.readPlistFromString(plist_text)

    return plist


def parse_plist_input_data(func):
    """Parses plist data as HTTP input from request"""
    @wraps(func)
    def decorator(*args, **kwargs):
        """Decorator for parsing HTTP input into a plist"""
        try:
            g.plist_data = plistlib.readPlistFromString(request.data)
        except xml.parsers.expat.ExpatError:
            current_app.logger.info('could not parse property list input data')
            abort(400, 'invalid input data')

        return func(*args, **kwargs)
    return decorator

def get_webcrts(config):
    """Find and include all mdm.webcrt's"""

    query = db_session.query(DBCertificate).filter(DBCertificate.cert_type == 'mdm.webcrt')
    webcrt_profiles = []
    for i, cert in enumerate(query):
        new_webcrt_profile = PEMCertificatePayload(config.prefix + '.webcrt.%d' % i, str(cert.pem_certificate).strip(), PayloadDisplayName='Web Server Certificate')
        webcrt_profiles.append(new_webcrt_profile)
    return webcrt_profiles
