# http://flask-sqlalchemy.pocoo.org/2.1/config/
SQLALCHEMY_DATABASE_URI = 'sqlite:///mdm.db'
SQLALCHEMY_DATABASE_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

# If commandment is running in development mode you should specify your public facing hostname here.
SSL_COMMON_NAME = 'localhost'

APP_UPLOAD_ROOT = 'apps'

SCEP_PORT = 5080
PORT = 5443

PUSH_CERTIFICATE = 'push.pem'

# If commandment is running in development mode, specify the path to the certificate and private key.
# These can also be generated
SSL_CERTIFICATE = '../commandment.crt'
SSL_RSA_KEY = '../commandment.key'
