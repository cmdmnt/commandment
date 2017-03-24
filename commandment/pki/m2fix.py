'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from M2Crypto import m2
from M2Crypto.X509 import X509_Extension
from ctypes import *

class X509V3_CTX(Structure):
    _fields_ = [
        ('flags', c_int),
        ('issuer_cert', c_void_p),
        ('subject_cert', c_void_p),
        ('subject_req', c_void_p),
        ('crl', c_void_p),
        ('db_meth', c_void_p),
        ('db', c_void_p),
    ]

def fix_ctx(m2_ctx, issuer=None):
    '''Fix for setting authorityKeyIdentifier with issuer certificate.

    Workaround sourced from:
      https://bugzilla.osafoundation.org/show_bug.cgi?id=7530#c13

    Thanks to Matt in comment #13 for the workaround of setting the context
    issuer and zeroing the structure. This fixes a segfault that would
    otherwise happen when setting the extension.'''
    ctx = X509V3_CTX.from_address(int(m2_ctx))

    ctx.flags = 0
    ctx.issuer_cert = int(issuer.x509) if issuer else None
    ctx.subject_cert = None
    ctx.subject_req = None
    ctx.crl = None

def new_extension_fixed(name, value, critical=0, issuer=None, _pyfree=1):
    """
    Create new X509_Extension instance with fix for issuer setting.
    """
    if name == 'subjectKeyIdentifier' and \
        value.strip('0123456789abcdefABCDEF:') is not '':
        raise ValueError('value must be precomputed hash')
    lhash = m2.x509v3_lhash()
    ctx = m2.x509v3_set_conf_lhash(lhash)

    # zero out structure, assign issuer
    fix_ctx(ctx, issuer)

    x509_ext_ptr = m2.x509v3_ext_conf(lhash, ctx, name, value)

    if x509_ext_ptr is None:
        raise Exception

    x509_ext = X509_Extension(x509_ext_ptr, _pyfree)
    x509_ext.set_critical(critical)
    return x509_ext
