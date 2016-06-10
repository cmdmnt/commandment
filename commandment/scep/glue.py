'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from ctypes import *
from ctypes import CDLL
from ctypes.util import find_library
from M2Crypto import m2, BIO, X509

libcrypto_ref = None

def get_libcrypto():
    global libcrypto_ref
    return libcrypto_ref

def set_libcrypto(libcrypto):
    global libcrypto_ref
    libcrypto_ref = libcrypto

PyObject_HEAD = [
    ('ob_refcnt', c_size_t),
    ('ob_type', c_void_p),
]

# from swig source: Lib/python/pyrun.swg (~ line 371)
class SwigPyObject(Structure):
    _fields_ = PyObject_HEAD + [
        ('ptr', c_void_p), # void *
        ('ty', c_void_p), # swig_type_info *
        ('own', c_int),
        ('next', c_void_p), # PyObject *
        # inside #ifdef
        # ('dict', c_void_p), # PyObject *
    ]

def change_swig_ptr(swig_obj, ct_obj):
    '''Here be dragons. We're reaching into not only the Python object,
    but a SWIG Python object in order to change the underlying pointer to a
    provided ctypes pointer.'''

    # cast the pointer to the SWIG object to our ctypes SwigPyObject structure
    ct_swig_obj = cast(c_void_p(id(swig_obj)), POINTER(SwigPyObject))
    # change the pointer
    ct_swig_obj.contents.ptr = ct_obj

def m2_x509_from_ct_ptr(ct_x509):
    # generate and immeidately free an X509 object so that we can get a
    # reference to the underlying SwigPyObject
    m2_x509 = m2.x509_new()
    m2.x509_free(m2_x509) # even though we've free'd we still have the ref

    # replace the pointer
    change_swig_ptr(m2_x509, ct_x509)

    # return a new M2 X509 object (that references our ctypes X509 obj)
    return X509.X509(m2_x509)

def m2_MemoryBuffer_from_ct_ptr(ct_bio):
    # generate and immeidately free a BIO object so that we can get a
    # reference to the underlying SwigPyObject
    m2_buf = BIO.MemoryBuffer()
    m2.bio_free(m2_buf._ptr()) # even though we've free'd we still have the ref

    # replace the pointer
    change_swig_ptr(m2_buf._ptr(), ct_bio)

    # return the MemoryBuffer object (that references our ctypes BIO obj)
    return m2_buf

# helper for readability
class OPENSSL_STACK(c_void_p):
    pass

class PKCS7_SIGNED(Structure):
    # no fields here to support a recursive structure
    pass

class PKCS7_d(Union):
    _fields_ = [
        ('ptr', c_char_p),
        ('data', c_void_p),
        ('sign', POINTER(PKCS7_SIGNED)),
        ('enveloped', c_void_p),
        ('signed_and_enveloped', c_void_p),
        ('digest', c_void_p),
        ('encrypted', c_void_p),
        ('other', c_void_p),
    ]

class PKCS7(Structure):
    _fields_ = [
        ('asn1', c_char_p),
        ('length', c_long),
        ('state', c_int),
        ('detached', c_int),
        ('type', c_char_p), # 
        ('d', PKCS7_d),
    ]

class X509_CRL(Structure):
    _fields_ = [
        ('crl', c_void_p),
        ('sig_alg', c_void_p),
        ('signature', c_void_p),
        ('references', c_int),
    ]

# assign fields after class definition due to recursive references
PKCS7_SIGNED._fields_ = [
        ('version', c_void_p),
        ('md_algs', c_void_p),
        ('cert', c_void_p),
        ('crl', POINTER(X509_CRL)),
        ('signer_info', c_void_p),
        ('contents', POINTER(PKCS7)),
    ]

# typedef struct pkcs7_issuer_and_serial_st {
#     X509_NAME *issuer;
#     ASN1_INTEGER *serial;
# } PKCS7_ISSUER_AND_SERIAL;

class PKCS7_ISSUER_AND_SERIAL(Structure):
    _fields_ = [
        ('issuer', c_void_p), # X509_NAME *
        ('serial', c_void_p), # ASN1_INTEGER *
    ]

# typedef struct pkcs7_signer_info_st {
#     ASN1_INTEGER *version;      /* version 1 */
#     PKCS7_ISSUER_AND_SERIAL *issuer_and_serial;
#     X509_ALGOR *digest_alg;
#     STACK_OF(X509_ATTRIBUTE) *auth_attr; /* [ 0 ] */
#     X509_ALGOR *digest_enc_alg;
#     ASN1_OCTET_STRING *enc_digest;
#     STACK_OF(X509_ATTRIBUTE) *unauth_attr; /* [ 1 ] */
#     /* The private key to sign with */
#     EVP_PKEY *pkey;
# } PKCS7_SIGNER_INFO;

class PKCS7_SIGNER_INFO(Structure):
    _fields_ = [
        ('version', c_void_p), # ASN1_INTEGER *
        ('issuer_and_serial', POINTER(PKCS7_ISSUER_AND_SERIAL)),
        ('digest_alg', c_void_p), # X509_ALGOR *
        ('auth_attr', OPENSSL_STACK), # STACK_OF(X509_ATTRIBUTE) *
        ('digest_enc_alg', c_void_p), # X509_ALGOR *
        ('enc_digest', c_void_p), # ASN1_OCTET_STRING *
        ('unauth_attr', OPENSSL_STACK), # STACK_OF(X509_ATTRIBUTE) *
        ('pkey', c_void_p), # EVP_PKEY *
    ]

# constant defineds in crypto/asn1/asn1.h
V_ASN1_OCTET_STRING = 4
V_ASN1_OBJECT = 6
V_ASN1_PRINTABLESTRING = 19

NID_pkcs9_contentType = 50

class ASN1TypeValue(Union):
    _fields_ = [
        ('ptr', c_char_p),
        ('boolean', c_int),
        ('asn1_string', c_void_p), # ASN1_STRING *
        ('object', c_void_p), # ASN1_OBJECT *
        ('integer', c_void_p), # ASN1_INTEGER *          
        ('enumerated', c_void_p), # ASN1_ENUMERATED *       
        ('bit_string', c_void_p), # ASN1_BIT_STRING *       
        ('octet_string', c_void_p), # ASN1_OCTET_STRING *     
        ('printablestring', c_void_p), # ASN1_PRINTABLESTRING *  
        ('t61string', c_void_p), # ASN1_T61STRING *        
        ('ia5string', c_void_p), # ASN1_IA5STRING *        
        ('generalstring', c_void_p), # ASN1_GENERALSTRING *    
        ('bmpstring', c_void_p), # ASN1_BMPSTRING *        
        ('universalstring', c_void_p), # ASN1_UNIVERSALSTRING *  
        ('utctime', c_void_p), # ASN1_UTCTIME *          
        ('generalizedtime', c_void_p), # ASN1_GENERALIZEDTIME *  
        ('visiblestring', c_void_p), # ASN1_VISIBLESTRING *    
        ('utf8string', c_void_p), # ASN1_UTF8STRING *       
        # /* set and sequence are left complete and still
        # * contain the set or sequence bytes */
        ('set', c_void_p), # ASN1_STRING *
        ('sequence', c_void_p), # ASN1_STRING *
        ('asn1_value', c_void_p), # ASN1_VALUE  *
    ]    

class ASN1Type(Structure):
    _fields_ = [
        ('type', c_int),
        ('value', ASN1TypeValue),
    ]

# Note: X509_ATTRIBUTE has changed!
# https://mta.openssl.org/pipermail/openssl-commits/2015-March/000802.html
class X509_ATTRIBUTE_Value(Union):
    _fields_ = [
        ('ptr', c_char_p),
        ('set', OPENSSL_STACK), # STACK_OF(ASN1_TYPE) *
        ('single', POINTER(ASN1Type)),
    ]

# Note: X509_ATTRIBUTE has changed!
# https://mta.openssl.org/pipermail/openssl-commits/2015-March/000802.html
class X509_ATTRIBUTE(Structure): # x509_attributes_st
    _fields_ = [
        ('object', c_void_p), # ASN1_OBJECT *
        # Note: X509_ATTRIBUTE has changed!
        # https://mta.openssl.org/pipermail/openssl-commits/2015-March/000802.html
        ('single', c_int),
        ('value', X509_ATTRIBUTE_Value),
        # If newer then only other field from 'object' is
        # ('set', OPENSSL_STACK), # STACK_OF(ASN1_TYPE) *
    ]

def init_libcrypto_prototypes(libcrypto):
    libcrypto.SSLeay.argtypes = []
    libcrypto.SSLeay.restype = c_ulong

    libcrypto.sk_num.argtypes = [OPENSSL_STACK]
    libcrypto.sk_num.restype = c_uint

    libcrypto.sk_value.argtypes = [OPENSSL_STACK, c_int]
    libcrypto.sk_value.restype = c_void_p

    libcrypto.sk_new_null.argtypes = []
    libcrypto.sk_new_null.restype = OPENSSL_STACK

    libcrypto.sk_push.argtypes = [OPENSSL_STACK, c_void_p]
    libcrypto.sk_push.restype = c_int

    libcrypto.X509_CRL_new.argtypes = []
    libcrypto.X509_CRL_new.restype = POINTER(X509_CRL)

    libcrypto.X509_dup.argtypes = [c_void_p]
    libcrypto.X509_dup.restype = c_void_p

    libcrypto.PKCS7_get_signer_info.argtypes = [POINTER(PKCS7)]
    libcrypto.PKCS7_get_signer_info.restype = OPENSSL_STACK # STACK_OF(PKCS7_SIGNER_INFO) *

    libcrypto.PKCS7_signatureVerify.argtypes = [c_void_p, POINTER(PKCS7), POINTER(PKCS7_SIGNER_INFO), c_void_p]
    libcrypto.PKCS7_signatureVerify.restype = c_int

    libcrypto.PKCS7_get_signed_attribute.argtypes = [POINTER(PKCS7_SIGNER_INFO), c_int]
    libcrypto.PKCS7_get_signed_attribute.restype = c_void_p

    libcrypto.X509_find_by_issuer_and_serial.argtypes = [c_void_p, c_void_p, c_void_p]
    libcrypto.X509_find_by_issuer_and_serial.restype = c_void_p

    libcrypto.OBJ_create.argtypes = [c_char_p, c_char_p, c_char_p]
    libcrypto.OBJ_create.restype = c_int

    libcrypto.OBJ_sn2nid.argtypes = [c_char_p]
    libcrypto.OBJ_sn2nid.restype = c_int

    libcrypto.OBJ_nid2obj.argtypes = [c_int]
    libcrypto.OBJ_nid2obj.restype = c_void_p # ASN1_OBJECT *

    libcrypto.OBJ_cmp.argtypes = [c_void_p, c_void_p]
    libcrypto.OBJ_cmp.restype = c_int

    libcrypto.X509_ATTRIBUTE_create.argtypes = [c_int, c_int, c_void_p]
    libcrypto.X509_ATTRIBUTE_create.restype = POINTER(X509_ATTRIBUTE)

    libcrypto.ASN1_TYPE_get.argtypes = [POINTER(ASN1Type)]
    libcrypto.ASN1_TYPE_get.restype = c_int

    libcrypto.ASN1_STRING_length.argtypes = [c_void_p] # ASN1_STRING *
    libcrypto.ASN1_STRING_length.restype = c_int

    libcrypto.ASN1_STRING_data.argtypes = [c_void_p, c_int]
    libcrypto.ASN1_STRING_data.restype = c_void_p

    libcrypto.ASN1_STRING_new.argtypes = []
    libcrypto.ASN1_STRING_new.restype = c_void_p # ASN1_STRING *

    # int ASN1_STRING_set(ASN1_STRING *str, const void *data, int len);
    # note the second arg is technically a c_void_p but for automagic string
    # conversion we're using a c_char_p
    libcrypto.ASN1_STRING_set.argtypes = [c_void_p, c_char_p, c_int]
    libcrypto.ASN1_STRING_set.restype = c_int

    libcrypto.PKCS7_dataInit.argtypes = [POINTER(PKCS7), c_void_p] # , BIO *
    libcrypto.PKCS7_dataInit.restype = c_void_p # BIO *

    libcrypto.PKCS7_new.argtypes = []
    libcrypto.PKCS7_new.restype = POINTER(PKCS7)

    libcrypto.i2d_PKCS7_bio.argtypes = [c_void_p, POINTER(PKCS7)]
    libcrypto.i2d_PKCS7_bio.restype = c_int

    libcrypto.d2i_PKCS7_bio.argtypes = [c_void_p, POINTER(POINTER(PKCS7))]
    libcrypto.d2i_PKCS7_bio.restype = POINTER(PKCS7)

    libcrypto.PKCS7_set_type.argtypes = [POINTER(PKCS7), c_int]
    libcrypto.PKCS7_set_type.restype = c_int

    libcrypto.PKCS7_content_new.argtypes = [POINTER(PKCS7), c_int]
    libcrypto.PKCS7_content_new.restype = c_int

    libcrypto.PKCS7_add_signature.argtypes = [
        POINTER(PKCS7),
        c_void_p, # X509 *
        c_void_p, # EVP_PKEY *
        c_void_p, # const EVP_MD *
        ]
    libcrypto.PKCS7_add_signature.restype = POINTER(PKCS7_SIGNER_INFO)

    #int PKCS7_set_signed_attributes(PKCS7_SIGNER_INFO *p7si,
    #               STACK_OF(X509_ATTRIBUTE) *sk);
    libcrypto.PKCS7_set_signed_attributes.argtypes = [POINTER(PKCS7_SIGNER_INFO), OPENSSL_STACK]
    libcrypto.PKCS7_set_signed_attributes.restype = c_int

    # int PKCS7_add_signed_attribute(PKCS7_SIGNER_INFO *p7si,int nid,int type,
    #   void *data);
    libcrypto.PKCS7_add_signed_attribute.argtypes = [POINTER(PKCS7_SIGNER_INFO), c_int, c_int, c_void_p]
    libcrypto.PKCS7_add_signed_attribute.restype = c_int

    # int PKCS7_dataFinal(PKCS7 *p7, BIO *bio);
    libcrypto.PKCS7_dataFinal.argtypes = [POINTER(PKCS7), c_void_p]
    libcrypto.PKCS7_dataFinal.restype = c_int

    # int PKCS7_add_certificate(PKCS7 *p7, X509 *x509);
    libcrypto.PKCS7_add_certificate.argtypes = [POINTER(PKCS7), c_void_p]
    libcrypto.PKCS7_add_certificate.restype = c_int

    libcrypto.PKCS7_decrypt.argtypes = [
        POINTER(PKCS7),
        c_void_p, # EVP_PKEY *
        c_void_p, # X509 *
        c_void_p, # BIO *
        c_int]
    libcrypto.PKCS7_decrypt.restype = c_int

def init_libcrypto(lib_path=None):
    if not lib_path:
        lib_path = find_library('crypto')

    libcrypto = CDLL(lib_path)

    set_libcrypto(libcrypto)

    init_libcrypto_prototypes(libcrypto)

    ct_ver_mask = libcrypto.SSLeay() & 0xffff000
    m2_ver_mask = m2.OPENSSL_VERSION_NUMBER & 0xffff000

    # In some cases the ctypes dynamically-loaded OpenSSL library may be
    # different than the version M2Crypto is compiled against. They need to
    # be very similar as they share data structures between the two.
    assert ct_ver_mask == m2_ver_mask, 'ctypes and M2Crypto OpenSSL libraries must closely match'
