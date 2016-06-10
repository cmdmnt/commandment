'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from M2Crypto import m2, SMIME, BIO, X509, EVP
from .glue import *
from .glue import get_libcrypto as get_lc

class SCEPMessageOIDKeyError(KeyError):
    pass

class SCEPMessageOID(object):
    @classmethod
    def get_string(self, ct_x509_attr):
        '''Return a string by unmarshalling and copying the raw value from
        a PRINTABLESTRING or OCTET_STRING ASN.1 X509_ATTRIBUTE *.'''
        assert isinstance(ct_x509_attr, POINTER(X509_ATTRIBUTE))
        ct_asn1_type_p = get_lc().sk_value(ct_x509_attr.contents.value.set, 0)
        ct_asn1_type = cast(ct_asn1_type_p, POINTER(ASN1Type))

        ct_attr_ptr = None
        if get_lc().ASN1_TYPE_get(ct_asn1_type) == V_ASN1_PRINTABLESTRING:
            ct_attr_ptr = ct_asn1_type.contents.value.asn1_string
        elif get_lc().ASN1_TYPE_get(ct_asn1_type) == V_ASN1_OCTET_STRING:
            ct_attr_ptr = ct_asn1_type.contents.value.octet_string

        if ct_attr_ptr:
            attr_len = get_lc().ASN1_STRING_length(ct_attr_ptr)
            ct_buf = create_string_buffer(attr_len)
            ct_data = get_lc().ASN1_STRING_data(ct_attr_ptr, attr_len)
            memmove(ct_buf, ct_data, attr_len)
            return ct_buf.raw

        return None

    @classmethod
    def openssl_init(cls):
        '''Create OpenSSL objects and store NIDs'''
        for scls in cls.__subclasses__():
            if not hasattr(scls, 'nid'):
                # TODO: check to see if already registered with OpenSSL
                # to avoid problem with this function getting run in
                # different threads (Flask debug environment)
                new_nid = get_lc().OBJ_create(scls.oid, scls.name, scls.name)
                scls.nid = new_nid

    @classmethod
    def ct_asn1_attribute(cls, value):
        str_value = str(value)
        ct_asn1_string = get_lc().ASN1_STRING_new()
        assert get_lc().ASN1_STRING_set(ct_asn1_string, str_value, len(str_value))
        ct_attr = get_lc().X509_ATTRIBUTE_create(cls.nid, cls.asn1_type, ct_asn1_string)
        assert ct_attr
        return ct_attr

    @classmethod
    def find_by_matching_x509_attr_asn1_obj(cls, ct_x509_attr):
        for scls in cls.__subclasses__():
            if hasattr(scls, 'nid'):
                if 0 == get_lc().OBJ_cmp(ct_x509_attr.contents.object, get_lc().OBJ_nid2obj(scls.nid)):
                    return scls

        raise SCEPMessageOIDKeyError('matching ASN1 SCEP OID object not found')

class MessageType(SCEPMessageOID):
    name = 'messageType'
    oid = '2.16.840.1.113733.1.9.2'
    asn1_type = V_ASN1_PRINTABLESTRING

PKI_STATUS_SUCCESS = '0'
PKI_STATUS_FAILURE = '2'
PKI_STATUS_PENDING = '3'

class PkiStatus(SCEPMessageOID):
    name = 'pkiStatus'
    oid = '2.16.840.1.113733.1.9.3'
    asn1_type = V_ASN1_PRINTABLESTRING

class FailInfo(SCEPMessageOID):
    name = 'failInfo'
    oid = '2.16.840.1.113733.1.9.4'
    asn1_type = V_ASN1_PRINTABLESTRING

class SenderNonce(SCEPMessageOID):
    name = 'senderNonce'
    oid = '2.16.840.1.113733.1.9.5'
    asn1_type = V_ASN1_OCTET_STRING

class RecipientNonce(SCEPMessageOID):
    name = 'recipientNonce'
    oid = '2.16.840.1.113733.1.9.6'
    asn1_type = V_ASN1_OCTET_STRING

class TransactionId(SCEPMessageOID):
    name = 'transactionID'
    oid = '2.16.840.1.113733.1.9.7'
    asn1_type = V_ASN1_PRINTABLESTRING

class SCEPMessageKeyError(KeyError):
    pass

class SCEPMessage(object):
    @classmethod
    def find_by_message_type(cls, message_type):
        for scls in cls.__subclasses__():
            if int(scls.message_type) == int(message_type):
                return scls

        raise SCEPMessageKeyError('matching message type not found')

    def get_signed_content(self):
        return self.signedcontent

    def to_pkcs7_der(self, digest_algo='sha256'):
        m2_p7 = SMIME.PKCS7()
        ct_p7 = cast(c_void_p(long(m2_p7._ptr())), POINTER(PKCS7))

        assert get_lc().PKCS7_set_type(ct_p7, m2.PKCS7_SIGNED)
        assert get_lc().PKCS7_content_new(ct_p7, m2.PKCS7_DATA)

        ct_signing_cert = c_void_p(long(self.signing_cert._ptr()))

        assert get_lc().PKCS7_add_certificate(ct_p7, ct_signing_cert)

        m2_digest = getattr(m2, digest_algo)
        ct_evp_md = c_void_p(long(m2_digest()))

        ct_si = get_lc().PKCS7_add_signature(
            ct_p7,
            ct_signing_cert,
            c_void_p(long(self.signing_pkey._ptr())),
            ct_evp_md)

        assert ct_si

        ct_attr_sk = get_lc().sk_new_null()
        assert ct_attr_sk

        assert get_lc().sk_push(ct_attr_sk, MessageType.ct_asn1_attribute(self.message_type))

        for a in self._get_attrs():
            get_lc().sk_push(ct_attr_sk, a)

        assert get_lc().PKCS7_set_signed_attributes(ct_si, ct_attr_sk)

        assert get_lc().PKCS7_add_signed_attribute(
            ct_si,
            NID_pkcs9_contentType,
            V_ASN1_OBJECT,
            get_lc().OBJ_nid2obj(m2.PKCS7_DATA))

        ct_p7bio = get_lc().PKCS7_dataInit(ct_p7, None)
        assert ct_p7bio

        m2_p7bio = m2_MemoryBuffer_from_ct_ptr(ct_p7bio)
        m2_p7bio.write(self.get_signed_content())

        assert get_lc().PKCS7_dataFinal(ct_p7, ct_p7bio)

        m2_bio_der = BIO.MemoryBuffer()
        m2_p7.write_der(m2_bio_der)

        return m2_bio_der.read()

    def _set_attrs(self, attrs):
        for obj, value in attrs:
            if issubclass(obj, TransactionId):
                self.transaction_id = value
            if issubclass(obj, PkiStatus):
                self.pki_status = value
            if issubclass(obj, SenderNonce):
                self.sender_nonce = value
            if issubclass(obj, RecipientNonce):
                self.recipient_nonce = value

    def _get_attrs(self):
        attrs = []
        if hasattr(self, 'transaction_id'):
            attrs.append(TransactionId.ct_asn1_attribute(self.transaction_id))
        if hasattr(self, 'pki_status'):
            attrs.append(PkiStatus.ct_asn1_attribute(self.pki_status))
        if hasattr(self, 'sender_nonce'):
            attrs.append(SenderNonce.ct_asn1_attribute(self.pki_status))
        if hasattr(self, 'recipient_nonce'):
            attrs.append(RecipientNonce.ct_asn1_attribute(self.pki_status))
        return attrs

    @classmethod
    def from_pkcs7_der(cls, pkcs7_der):
        m2_p7_bio = BIO.MemoryBuffer(pkcs7_der)
        m2_p7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(m2_p7_bio._ptr()), 1)
        ct_p7 = cast(c_void_p(long(m2_p7._ptr())), POINTER(PKCS7))

        ct_sis = get_lc().PKCS7_get_signer_info(ct_p7)
        assert get_lc().sk_num(ct_sis) == 1

        ct_si = cast(c_void_p(get_lc().sk_value(ct_sis, 0)), POINTER(PKCS7_SIGNER_INFO))

        ct_x509 = get_lc().X509_find_by_issuer_and_serial(
            ct_p7.contents.d.sign.contents.cert,
            ct_si.contents.issuer_and_serial.contents.issuer,
            ct_si.contents.issuer_and_serial.contents.serial)

        signing_cert = m2_x509_from_ct_ptr(ct_x509)

        m2_p7buf = BIO.MemoryBuffer()
        ct_p7buf = c_void_p(long(m2_p7buf._ptr()))

        assert get_lc().PKCS7_signatureVerify(ct_p7buf, ct_p7, ct_si, ct_x509) >= 0

        assert ct_si.contents.auth_attr
        assert get_lc().sk_num(ct_si.contents.auth_attr)

        attrs = []

        for i in xrange(0, get_lc().sk_num(ct_si.contents.auth_attr)):
            # loop through the signed attributes

            ct_x509_attr_p = get_lc().sk_value(ct_si.contents.auth_attr, i)
            assert ct_x509_attr_p
            ct_x509_attr = cast(ct_x509_attr_p, POINTER(X509_ATTRIBUTE))

            try:
                # try to find a matching OID attribute that we handle
                oid_obj = SCEPMessageOID.find_by_matching_x509_attr_asn1_obj(ct_x509_attr)
            except SCEPMessageOIDKeyError:
                continue

            attrs.append((oid_obj, oid_obj.get_string(ct_x509_attr)))

        message_types = [attr for attr in attrs if issubclass(attr[0], MessageType)]
        assert message_types
        message_type = message_types[0]
        attrs.remove(message_types[0])

        ct_p7bio = get_lc().PKCS7_dataInit(ct_p7, None)
        assert ct_p7bio

        m2_p7bio = m2_MemoryBuffer_from_ct_ptr(ct_p7bio)

        ncls = SCEPMessage.find_by_message_type(message_type[1])()

        ncls.signing_cert = signing_cert
        ncls.signedcontent = m2_p7bio.read()
        ncls._set_attrs(attrs)

        return ncls

class CertRep(SCEPMessage):
    message_type = 3

class RenewalReq(SCEPMessage):
    message_type = 17

class UpdateReq(SCEPMessage):
    message_type = 18

class PKCSReq(SCEPMessage):
    message_type = 19

class CertPoll(SCEPMessage):
    message_type = 20

class GetCert(SCEPMessage):
    message_type = 21

class GetCRL(SCEPMessage):
    message_type = 22

def degenerate_pkcs7_der(m2_x509s):
    ct_p7 = get_lc().PKCS7_new()

    assert get_lc().PKCS7_set_type(ct_p7, m2.PKCS7_SIGNED)
    assert get_lc().PKCS7_content_new(ct_p7, m2.PKCS7_DATA)

    ct_x509_sk = get_lc().sk_new_null()

    for m2_x509 in m2_x509s:
        # duplicate the provided X509 certificate (as it will get free'd)
        # when we free our PKCS7 structure
        m2_x509_dup = m2.x509_dup(m2_x509._ptr())
        ct_x509_dup = c_void_p(long(m2_x509_dup))

        get_lc().sk_push(ct_x509_sk, ct_x509_dup)

    ct_p7.contents.d.sign.contents.crl = None
    ct_p7.contents.d.sign.contents.cert = ct_x509_sk

    m2_p7bio = BIO.MemoryBuffer()
    ct_p7bio = c_void_p(long(m2_p7bio._ptr()))

    assert get_lc().i2d_PKCS7_bio(ct_p7bio, ct_p7)

    pkcs7_der = m2_p7bio.read()

    get_lc().PKCS7_free(ct_p7)

    return pkcs7_der
