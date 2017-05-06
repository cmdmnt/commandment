from flask.testing import FlaskClient


class MDMClient(FlaskClient):
    """MDMClient is a superset of the flask testing client meant to perform higher level operations similar to the
    native mdmclient binary.
    
    Attributes:
          _private_key (rsa.RSAPrivateKey): RSA Private Key for the simulated client.
          _certificate (x509.Certificate): X.509 Certificate for the simulated client.
    """
    
    def __init__(self, *args, **kwargs):
        self._private_key = kwargs.get('private_key', None)
        self._certificate = kwargs.get('certificate', None)
        
        super(MDMClient, self).__init__(*args, **kwargs)
