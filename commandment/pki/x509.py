"""
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from time import time
from binascii import hexlify

'''As an attempt to separate the M2 APIs and this abstraction we've tried
to prepend an undersore (_) to all underlying M2 objects.'''

DEFAULT_RSA_KEYSIZE = 2048
DEFAULT_X509_SIGN_DIGEST = 'sha256'
DEFAULT_REQ_SIGN_DIGEST = 'sha256'
DEFAULT_SUBJECT_KEY_DIGEST = 'sha1'
DEFAULT_X509_FPRINT_DIGEST = 'sha256'

class ModulusMismatch(Exception):
    pass


class InvalidCertificatePolicy(Exception):
    pass

class PrivateKey(object):
    def __init__(self, keysize=None):
        self._rsa = rsa.generate_private_key(
            public_exponent=65535,
            key_size=keysize or DEFAULT_RSA_KEYSIZE,
            backend=default_backend(),
        )

    def to_pem(self):
        pem = self._rsa.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem

    def to_der(self):
        der = self._rsa.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return der

    @classmethod
    def from_pem(cls, data):
        newcls = cls.__new__(cls)
        newcls._rsa = serialization.load_pem_private_key(
            data,
            password=None,
            backend=default_backend()
        )
        return newcls


class CertificatePolicy(object):
    ca = False

    def __init__(self, cert_request):
        self.cert_request = cert_request

    def _get_subject(self):
        # generally speaking we should only issue certs with subject OIDs
        # that we can vouch for. in the default policy here we blindly trust
        # the certificate request and simply copy it's value
        return self.cert_request._get_subject()

    def is_ca(self):
        return bool(self.ca)

    def _add_x509_extensions(self, _x509):
        if hasattr(self, 'key_usage'):
            _x509.add_ext(X509.new_extension(
                'keyUsage',
                ','.join(self.key_usage),
                critical=getattr(self, 'key_usage_critical', 1)))

        if hasattr(self, 'extended_key_usage'):
            _x509.add_ext(X509.new_extension(
                'extendedKeyUsage',
                ','.join(self.extended_key_usage),
                critical=getattr(self, 'extended_key_usage_critical', 1)))

class Certificate(object):
    policy = CertificatePolicy

    def __init__(self, cert_request, private_key, ca_cert=None, days=365, serial=1, digest=None):
        if not isinstance(private_key, PrivateKey):
            raise Exception('not a valid private_key')

        if not isinstance(cert_request, CertificateRequest):
            raise Exception('not a valid cert_request')

        issuer_cert = ca_cert or self

        policy = self.policy(cert_request)

        self._x509 = X509.X509()

        self._x509.set_pubkey(cert_request._get_pubkey())

        if not issuer_cert.belongs_to_private_key(private_key):
            raise ModulusMismatch('issuer certificate does not match private_key')

        self._x509.set_serial_number(serial)
        self._x509.set_version(2) # version 3

        if not cert_request._get_subject() and policy.is_ca():
            raise InvalidCertificatePolicy('subject must not be blank for cA '
                'certificates (rfc5280#section-4.1.2.6)')

        self._x509.set_subject(policy._get_subject())

        self._make_valid_expiry(days)

        self._x509.add_ext(X509.new_extension('subjectKeyIdentifier',
            cert_request.get_pubkey_fingerprint()))

        self._x509.set_issuer(issuer_cert._get_subject())
        self._x509.add_ext(new_extension_fixed('authorityKeyIdentifier',
            'keyid,issuer:always', issuer=issuer_cert._x509))

        cavalue = 'CA:TRUE' if policy.is_ca() or not ca_cert else 'CA:FALSE'
        self._x509.add_ext(X509.new_extension(
            'basicConstraints',
            cavalue,
            critical=1))

        policy._add_x509_extensions(self._x509)

        self._x509.sign(private_key._new_evp(), digest or DEFAULT_X509_SIGN_DIGEST)

    def _make_valid_expiry(self, days=365):
        not_before = m2.x509_get_not_before(self._x509._ptr())
        not_after  = m2.x509_get_not_after(self._x509._ptr())

        m2.x509_gmtime_adj(not_before, 0)
        m2.x509_gmtime_adj(not_after, days * 24 * 60 * 60)

    def _get_subject(self):
        return self._x509.get_subject()

    def to_pem(self):
        return self._x509.as_pem()

    # def to_pem_file(self, filename):
    #     self._x509.save(filename, X509.FORMAT_PEM)

    def to_der(self):
        return self._x509.as_der()

    def __repr__(self):
        return '<%s Subject=%r Issuer=%r Ser=%r at %s>' % (
            self.__class__.__name__,
            self.get_subject_text(),
            self._x509.get_issuer().as_text(),
            self._x509.get_serial_number(),
            format(id(self), '#x'))

    def _get_pubkey(self):
        return self._x509.get_pubkey()

    def belongs_to_private_key(self, private_key):
        cert_modulus = self._get_pubkey().get_modulus()
        return cert_modulus.lower() == private_key.get_pubkey_modulus().lower()

    def get_cn(self):
        return self._get_subject().CN

    @classmethod
    def from_pem(cls, data):
        newcls = cls.__new__(cls)
        newcls._x509 = X509.load_cert_string(str(data))
        return newcls

    def get_subject_text(self):
        return self._get_subject().as_text()

    def get_fingerprint(self, digest=None):
        return self._x509.get_fingerprint(digest or DEFAULT_X509_FPRINT_DIGEST)

    def get_not_before(self):
        return self._x509.get_not_before().get_datetime()

    def get_not_after(self):
        return self._x509.get_not_after().get_datetime()

    def _m2_x509(self):
        return self._x509

class CACertificatePolicy(CertificatePolicy):
    ca = True

class CACertificate(Certificate):
    policy = CACertificatePolicy

class Identity(object):
    def __init__(self, private_key, cert, addl_certs=[]):
        if not cert.belongs_to_private_key(private_key):
            raise ModulusMismatch('certificate does not match private_key')
        self.private_key = private_key
        self.cert = cert
        self.addl_certs = addl_certs

    def get_private_key(self):
        return self.private_key

    def get_cert(self):
        return self.cert

    def to_pkcs12(self, password):
        p12 = PKCS12()

        # convert M2Crypto keys & certs into OpenSSL's format using DER
        # yes, a bit wasteful as we're going into one OpenSSL wrapper to
        # another. perhaps settle on an OpenSSL wrapper at some point.
        cert_pem = self.get_cert().to_pem()
        p12.set_certificate(load_certificate(FILETYPE_PEM, cert_pem))

        key_pem = self.get_private_key().to_pem()
        p12.set_privatekey(load_privatekey(FILETYPE_PEM, key_pem))

        cvt_cacerts = []
        for cacert in self.addl_certs:
            cvt_cacert = cacert.to_pem()
            cvt_cacerts.append(load_certificate(FILETYPE_PEM, cvt_cacert))

        return p12.export(password)

    # TODO: SMIME/CMS signing and encrypting, mostly for profile inclusion
class CAIdentity(Identity):
    def sign_cert_req(self, cert_req, cert_type=Certificate):
        return cert_type(cert_req, self.get_private_key(), serial=id(cert_req), ca_cert=self.get_cert())

class SelfSignedCAIdentity(CAIdentity):
    def __init__(self, **kwargs):
        ca_req, ca_pk = CertificateRequest.with_new_private_key(**kwargs)
        ca_crt = CACertificate(ca_req, ca_pk)

        super(SelfSignedCAIdentity, self).__init__(ca_pk, ca_crt)
