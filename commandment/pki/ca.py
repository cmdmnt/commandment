'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

'''Commandment MDM Certificate Authority'''

from flask import g
from ..database import db_session, NoResultFound
from ..models import (Certificate as DBCertificate,
                      PrivateKey as DBPrivateKey,
                      InternalCA)
from .x509 import *

try:
    from M2Crypto.m2 import NID_userId
except ImportError:
    # does not have an alias in M2Crypto, so just use the OpenSSL definition
    NID_userId = 458 # from OpenSSL obj_mac.h

MDM_CA_CN = 'MDM CA'
MDM_DEVICE_CN = 'MDM Device'

def get_ca():
    ca = getattr(g, '_mdm_ca', None)
    if ca is None:
        ca = g._mdm_ca = CA()
    return ca

class CA(object):
    def __init__(self):
        try:
            db_cert, db_pk = db_session.query(DBCertificate, DBPrivateKey)\
                .join(DBCertificate, DBPrivateKey.certificates)\
                .filter(DBCertificate.cert_type == 'mdm.cacert')\
                .one()
            self.ca_identity = CAIdentity(db_pk.to_x509(), db_cert.to_x509(cert_type=CACertificate))
        except NoResultFound:
            self.ca_identity = SelfSignedCAIdentity(CN=MDM_CA_CN)

            db_cert = DBCertificate.from_x509(self.ca_identity.get_cert(), 'mdm.cacert')
            db_pk = DBPrivateKey.from_x509(self.ca_identity.get_private_key())

            db_pk.certificates.append(db_cert)

            db_session.add(db_cert)
            db_session.add(db_pk)

            db_session.commit()

    def get_cacert(self):
        return self.ca_identity.get_cert()

    def get_private_key(self):
        return self.ca_identity.get_private_key()

    def sign_new_device_req(self, csr):
        '''Sign and persist a new device certificate request'''

        dev_signed_cert = self.ca_identity.sign_cert_req(csr)

        db_dev_crt = self.save_new_device_cert(dev_signed_cert)

        return dev_signed_cert, db_dev_crt

    def save_new_device_cert(self, cert):
        # cert should be of type Certificate
        db_dev_crt = DBCertificate.from_x509(cert, 'mdm.device')
        db_session.add(db_dev_crt)
        db_session.commit()

        return db_dev_crt

    def gen_new_device_identity(self):
        # we don't persist the key as it should only be held and used by
        # the client device
        dev_csr, dev_key = CertificateRequest.with_new_private_key(CN=MDM_DEVICE_CN)

        dev_crt, db_dev_crt = self.sign_new_device_req(dev_csr)

        return (Identity(dev_key, dev_crt), db_dev_crt)

class WebCertificate(Certificate):
    def get_cn(self):
        return self.get_m2_cert().get_subject().CN

class PushCertificate(Certificate):
    def get_topic(self):
        x509_uid_name_entries = self._x509.get_subject().get_entries_by_nid(NID_userId)

        if len(x509_uid_name_entries) != 1:
            raise AttributeError('No UID entry in APNS Push certificate subject')

        topic = x509_uid_name_entries[0].get_data().as_text()

        return topic

def get_or_generate_web_certificate(cn):
    mdm_ca = CA()
    try:
        q = db_session.query(DBCertificate, DBPrivateKey)\
            .join(DBCertificate, DBPrivateKey.certificates)\
            .filter(DBCertificate.cert_type == 'mdm.webcrt')
        result = q.first()
        if not result:
            q.one()
        else:
            db_cert, db_pk = result
        # TODO: return chain!
        return (db_cert.pem_certificate, db_pk.pem_key, mdm_ca.get_cacert().to_pem())
    except NoResultFound:
        web_req, web_pk = CertificateRequest.with_new_private_key(CN=cn)

        web_crt = mdm_ca.ca_identity.sign_cert_req(web_req)

        db_cert = DBCertificate.from_x509(web_crt, 'mdm.webcrt')
        db_pk = DBPrivateKey.from_x509(web_pk)

        db_session.add(db_cert)
        db_session.add(db_pk)

        db_pk.certificates.append(db_cert)

        db_session.commit()

        return (db_cert.pem_certificate, db_pk.pem_key, mdm_ca.get_cacert().to_pem())
