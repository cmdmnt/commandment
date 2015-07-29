'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

'''Certificate Authority for MDM using Flask contexts, Peewee, and m2certs'''

from flask import g
from ..database import db_session, NoResultFound
from ..models import Certificate as DBCertificate, PrivateKey as DBPrivateKey, certificate_private_key_assoc
from m2certs import RSAPrivateKey, Certificate, CertificateRequest, Identity, NID_userId

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
            q = db_session.query(DBCertificate, DBPrivateKey).join(DBCertificate, DBPrivateKey.certificates).filter(DBCertificate.cert_type == 'mdm.cacert')

            # TODO: support more than one CA depending on MDM context
            cert, pk = q.one()

            # TODO: consider using an Identity?
            self.ca_privkey = RSAPrivateKey.load(str(pk.pem_key))
            self.ca_cert = Certificate.load(str(cert.pem_certificate))
        except NoResultFound:
            # no cacert, let's generate and store one

            self.ca_privkey = RSAPrivateKey()

            # generate csr
            ca_csr = mdm_cacert_csr = CertificateRequest(self.ca_privkey, CN=MDM_CA_CN)

            # create (and self-sign) the CA certificate request
            self.ca_cert = Certificate.cacert_from_req(ca_csr)

            # save CA private key in DB
            db_ca_privkey = DBPrivateKey()
            db_ca_privkey.pem_key = self.ca_privkey.get_pem()

            db_session.add(db_ca_privkey)

            # save certificate
            db_ca_cert = DBCertificate()
            db_ca_cert.cert_type = 'mdm.cacert'
            db_ca_cert.pem_certificate = self.ca_cert.get_pem()

            db_session.add(db_ca_cert)

            # add certificate to private key
            db_ca_privkey.certificates.append(db_ca_cert)

            db_session.commit()

    def get_cacert(self):
        return self.ca_cert

    def gen_new_device_identity(self):
        '''Generate a new certificat and key intended for a new MDM payload

        Returns an m2certs.Identity instance.'''

        # TODO: increment CA serial

        # we don't persist the key as it should only be held and used by
        # the client device
        dev_key = RSAPrivateKey()

        dev_csr = CertificateRequest(dev_key, CN=MDM_DEVICE_CN)

        dev_crt = Certificate.cert_from_req_signed_by_cacert(dev_csr, self.ca_cert, self.ca_privkey)

        # save certificate in DB
        db_dev_crt = DBCertificate()
        db_dev_crt.cert_type = 'mdm.device'
        db_dev_crt.pem_certificate = dev_crt.get_pem()
        db_session.add(db_dev_crt)

        db_session.commit()

        return Identity(dev_key, dev_crt)

class PushCertificate(Certificate):
    def get_topic(self):
        x509_uid_name_entries = self.get_m2_cert().get_subject().get_entries_by_nid(NID_userId)

        if len(x509_uid_name_entries) != 1:
            raise Exception('No UID entry in APNs certificate subject')

        topic = x509_uid_name_entries[0].get_data().as_text()

        return topic

def get_or_generate_web_certificate(cn):
    try:
        q = db_session.query(DBCertificate, DBPrivateKey).join(DBCertificate, DBPrivateKey.certificates).filter(DBCertificate.cert_type == 'mdm.webcrt')
        res = q.first()
        if not res:
            res = q.one()
        db_web_crt, db_web_pk = res
        return (db_web_crt.pem_certificate, db_web_pk.pem_key)
    except NoResultFound:
        web_pk = RSAPrivateKey()

        # generate csr
        web_csr = CertificateRequest(web_pk, CN=cn)

        # create (and self-sign) the web certificate request
        web_crt = Certificate.cacert_from_req(web_csr)

        # save CA private key in DB
        db_web_pk = DBPrivateKey()
        db_web_pk.pem_key = web_pk.get_pem()

        db_session.add(db_web_pk)

        # save certificate
        db_web_crt = DBCertificate()
        db_web_crt.cert_type = 'mdm.webcrt'
        db_web_crt.pem_certificate = web_crt.get_pem()

        db_session.add(db_web_crt)

        # add certificate to private key
        db_web_pk.certificates.append(db_web_crt)

        db_session.commit()

        return (web_crt.get_pem(), web_pk.get_pem())
