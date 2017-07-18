from typing import Union, Optional
from asn1crypto.cms import CertificateSet, SignerIdentifier, Certificate


def _certificate_by_signer_identifier(certificates: CertificateSet, sid: SignerIdentifier) -> Optional[Certificate]:
    """Find a signer certificate by its SignerIdentifier.

    Args:
          certificates (CertificateSet): Set of certificates parsed by asn1crypto.
          sid (SignerIdentifier): Signer Identifier, usually IssuerAndSerialNumber.
    Returns:
          cms.Certificate or None
    """
    if sid.name != 'issuer_and_serial_number':
        return None  # Only IssuerAndSerialNumber for now

    #: IssuerAndSerialNumber
    ias = sid.chosen

    for c in certificates:
        if c.name != 'certificate':
            continue  # we only support certificate for now

        chosen = c.chosen  #: Certificate

        if chosen.serial_number != ias['serial_number'].native:
            continue

        if chosen.issuer == ias['issuer']:
            return c

    return None