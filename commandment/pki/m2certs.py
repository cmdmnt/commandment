'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

'''M2Crypto X509 certificate and key wrappers

Wrappers to help make dealing with certificates a bit more pythonic using
M2Crypto and OpenSSL. Thanks to https://gist.github.com/eskil/2338529 for
M2Crypto CA ideas.'''

from M2Crypto import EVP, RSA, BIO, X509, ASN1, m2
from M2Crypto.X509 import X509Error
import time

from OpenSSL.crypto import PKCS12, load_certificate, load_privatekey, FILETYPE_PEM

try:
    from M2Crypto.m2 import NID_userId
except ImportError:
    # does not have an alias in M2Crypto, so just use the OpenSSL definition
    NID_userId = 458 # from OpenSSL obj_mac.h

# Ctx, fix_ctx, and new_extension are from here:
#   https://bugzilla.osafoundation.org/show_bug.cgi?id=7530#c13
# Thanks to Matt in Comment #13 for the workaround of setting the context
# issuer certificate and fixing the segfault.
import ctypes

class Ctx(ctypes.Structure):
    _fields_ = [
        ('flags', ctypes.c_int),
        ('issuer_cert', ctypes.c_void_p),
        ('subject_cert', ctypes.c_void_p),
        ('subject_req', ctypes.c_void_p),
        ('crl', ctypes.c_void_p),
        ('db_meth', ctypes.c_void_p),
        ('db', ctypes.c_void_p),
    ]

def fix_ctx(m2_ctx, issuer=None):
    ctx = Ctx.from_address(int(m2_ctx))

    ctx.flags = 0
    ctx.subject_cert = None
    ctx.subject_req = None
    ctx.crl = None
    if issuer is None:
        ctx.issuer_cert = None
    else:
        ctx.issuer_cert = int(issuer.x509)

def new_extension(name, value, critical=0, issuer=None, _pyfree = 1):
    """
    Create new X509_Extension instance.
    """
    if name == 'subjectKeyIdentifier' and \
        value.strip('0123456789abcdefABCDEF:') is not '':
        raise ValueError('value must be precomputed hash')


    lhash = m2.x509v3_lhash()
    ctx = m2.x509v3_set_conf_lhash(lhash)
    #ctx not zeroed
    fix_ctx(ctx, issuer)

    x509_ext_ptr = m2.x509v3_ext_conf(lhash, ctx, name, value)
    #ctx,lhash freed

    if x509_ext_ptr is None:
        raise Exception
    x509_ext = X509.X509_Extension(x509_ext_ptr, _pyfree)
    x509_ext.set_critical(critical)
    return x509_ext


class RSAPrivateKey(object):
    def __init__(self, rsa=None, bits=2048):
        if not rsa:
            self.rsa = RSA.gen_key(bits, 65537, lambda: None)
        else:
            self.rsa = rsa

    def get_m2_rsa(self):
        return self.rsa

    def get_pem(self):
        return self.rsa.as_pem(None)

    @classmethod
    def load(cls, rsa_bin_data):
        bio = BIO.MemoryBuffer(rsa_bin_data)
        return cls(RSA.load_key_bio(bio))

    @classmethod
    def load_file(cls, filename):
        return cls(RSA.load_key(filename))

class CertificateRequest(object):
    def __init__(self, privkey=None, md='sha256', **kwargs):
        if not privkey:
            self.privkey = RSAPrivateKey()
        else:
            self.privkey = privkey

        pk = EVP.PKey()
        pk.assign_rsa(self.privkey.get_m2_rsa(), capture=0)

        req = X509.Request()
        req.set_pubkey(pk)

        subj = req.get_subject()

        for k in kwargs.keys():
            setattr(subj, k, kwargs[k])

        req.set_subject(subj)

        req.sign(pk, md)

        self.req = req

    def get_m2_req(self):
        return self.req

    def get_privkey(self):
        return self.privkey

    def get_der(self):
        return self.req.as_der()

    @classmethod
    def load_der(cls, req_data):
        # TODO: don't need to clear privkey (nor even generate it)
        newcls = cls()
        newcls.privkey = None
        bio = BIO.MemoryBuffer(req_data)
        newcls.req = X509.load_request_bio(bio, format=X509.FORMAT_DER)
        return newcls

class Certificate(object):
    def __init__(self, cert=None, serial=1, version=2):
        if cert:
            # if cert is specified (i.e. already loaded from file or memory)
            self.cert = cert
            return

        self.cert = X509.X509()

        self.cert.set_serial_number(serial)
        self.cert.set_version(version)

    def get_m2_cert(self):
        return self.cert

    def get_pem(self):
        return self.cert.as_pem()

    def get_der(self):
        return self.cert.as_der()

    def make_valid(self, days_valid=365):
        t = long(time.time())
        now = ASN1.ASN1_UTCTIME()
        now.set_time(t)
        expire = ASN1.ASN1_UTCTIME()
        expire.set_time(t + days_valid * 24 * 60 * 60)
        self.cert.set_not_before(now)
        self.cert.set_not_after(expire)

    def subject_from_req(self, req):
        self.cert.set_subject(req.get_m2_req().get_subject())

    def pubkey_from_req(self, req):
        self.cert.set_pubkey(req.get_m2_req().get_pubkey())

    def set_issuer(self, cert):
        self.cert.set_issuer(cert.get_m2_cert().get_subject())

    def set_ca_extn(self):
        self.cert.add_ext(X509.new_extension('basicConstraints', 'CA:TRUE'))

    def set_ski_extn(self):
        self.cert.add_ext(X509.new_extension('subjectKeyIdentifier', self.cert.get_fingerprint()))

    def set_aki_extn(self, cert):
        self.cert.add_ext(new_extension('authorityKeyIdentifier', 'keyid,issuer:always', issuer=cert.get_m2_cert()))

    def sign_with_m2_privkey(self, privkey, md='sha256'):
        self.cert.sign(privkey, md)

    def get_subject_as_text(self):
        return self.cert.get_subject().as_text()

    def get_not_before(self):
        return self.cert.get_not_before().get_datetime()

    def get_not_after(self):
        return self.cert.get_not_after().get_datetime()

    @classmethod
    def cacert_from_req(cls, req):
        cacert = cls()

        cacert.subject_from_req(req)
        cacert.pubkey_from_req(req)
        cacert.make_valid()
        cacert.set_ski_extn()

        cacert.set_ca_extn()
        cacert.set_issuer(cacert)
        cacert.set_aki_extn(cacert)

        ca_pk = EVP.PKey()
        ca_pk.assign_rsa(req.get_privkey().get_m2_rsa(), capture=0)

        cacert.sign_with_m2_privkey(ca_pk)

        return cacert

    @classmethod
    def cert_from_req_signed_by_cacert(cls, req, cacert, ca_privkey, serial=2, md='sha256'):
        cert = cls(serial=serial)

        cert.subject_from_req(req)
        cert.pubkey_from_req(req)
        cert.make_valid()
        cert.set_ski_extn()

        cert.set_issuer(cacert)
        cert.set_aki_extn(cacert)

        ca_pk = EVP.PKey()
        ca_pk.assign_rsa(ca_privkey.get_m2_rsa(), capture=0)

        cert.sign_with_m2_privkey(ca_pk)

        return cert

    @classmethod
    def load(cls, cert_data):
        bio = BIO.MemoryBuffer(cert_data)
        return cls(X509.load_cert_bio(bio))

    @classmethod
    def load_file(cls, filename):
        return cls(X509.load_cert(filename))

    def write_pem_file(self, filename):
        with open(filename, 'wb') as cert_file:
            cert_file.write(self.cert.as_pem())

    def belongs_to_key(self, pkey):
        # get the underlying M2Crypto cert
        m2_cert = self.get_m2_cert()
        # get the public key
        cert_pk = m2_cert.get_pubkey()
        # get the modulus (as a string of hex digits)
        cert_modulus = cert_pk.get_modulus().upper()

        # get the underlying M2Crypto key
        m2_key = pkey.get_m2_rsa()
        # get the modulus (as a tuple of (exponent, modulus) bytes)
        key_e, key_n = m2_key.pub()
        # for some reason the modulus has an extra few bytes. strip it,
        # make it hex, and uppercase (to be compared against cert. mod.)
        key_modulus = key_n[5:].encode('hex').upper()

        return cert_modulus == key_modulus

class Identity(object):
    def __init__(self, privkey, cert, addl_certs=[]):
        self.privkey = privkey
        self.cert = cert
        self.addl_certs = addl_certs

    def gen_pkcs12(self, password):
        p12 = PKCS12()

        # convert M2Crypto keys & certs into OpenSSL's format using DER
        # yes, a bit wasteful as we're going into one OpenSSL wrapper to
        # another. perhaps settle on an OpenSSL wrapper at some point.
        cert_pem = self.cert.get_m2_cert().as_pem()
        p12.set_certificate(load_certificate(FILETYPE_PEM, cert_pem))

        key_pkey = self.privkey.get_m2_rsa()
        key_pem = key_pkey.as_pem(None)
        p12.set_privatekey(load_privatekey(FILETYPE_PEM, key_pem))

        cvt_cacerts = []
        for cacert in self.addl_certs:
            cvt_cacert = cacert.get_m2_cert().as_pem()
            cvt_cacerts.append(load_certificate(FILETYPE_PEM, cvt_cacert))

        return p12.export(password)

    # TODO: SMIME/CMS signing and encrypting, mostly for profile inclusion
