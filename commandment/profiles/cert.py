"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from . import Payload
import plistlib  # needed for Data() wrapper


class PEMCertificatePayload(Payload):
    """PEM-encoded certificate without private key. May contain root
    certificates.

    Payload type of "com.apple.security.pem". Further encodes cert_data as
    plistlib.Data instance (Base64 data)."""

    payload_type = 'com.apple.security.pem'

    def __init__(self, identifier, cert_data, uuid=None, **kwargs):
        kwargs['PayloadContent'] = plistlib.Data(cert_data)
        Payload.__init__(self, self.payload_type, identifier, uuid, **kwargs)


class PKCS12CertificatePayload(Payload):
    """Password-protected identity certificate. Only one certificate may be
    included.

    Payload type of "com.apple.security.pkcs12". Include a PKCS#12 (.p12)
    identity as cert_data. Further encodes cert_data as plistlib.Data instance
    (Base64 data). Include a password argument for the PKCS#12 identity."""

    payload_type = 'com.apple.security.pkcs12'

    def __init__(self, identifier, cert_data, password=None, uuid=None, **kwargs):
        kwargs['PayloadContent'] = plistlib.Data(cert_data)
        if password:
            kwargs['Password'] = password
        Payload.__init__(self, self.payload_type, identifier, uuid, **kwargs)


class SCEPPayload(Payload):
    """SCEP (Simple Certificate Enrollment Protocol) payload automates the
    request of a client certificate from an SCEP server"""

    payload_type = 'com.apple.security.scep'

    def __init__(self, identifier, url, uuid=None, **kwargs):
        # SCEP payload is an odd one. all of the keys are in the
        # PayloadContent key
        if 'PayloadContent' in kwargs:
            kwargs['PayloadContent']['URL'] = url
        else:
            kwargs['PayloadContent'] = {'URL': url}
        Payload.__init__(self, self.payload_type, identifier, uuid, **kwargs)
