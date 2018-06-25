# Flask Dev Server
PORT = 5443

# Flask-Alembic imports configuration from here instead of the alembic.ini
ALEMBIC = {
    'script_location': '%(here)s/alembic/versions'
}

# http://flask-sqlalchemy.pocoo.org/2.1/config/
SQLALCHEMY_DATABASE_URI = 'sqlite:///commandment/commandment.db'
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
SQLALCHEMY_TRACK_MODIFICATIONS = False


# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'

PLISTIFY_MIMETYPE = 'application/xml'


# Internal CA - Certificate X.509 Attributes
INTERNAL_CA_CN = 'COMMANDMENT-CA'
INTERNAL_CA_O = 'Commandment'


# --------------
# SCEPy Defaults
# --------------

# Directory where certs, revocation lists, serials etc will be kept
SCEPY_CA_ROOT = "CA"

# X.509 Name Attributes used to generate the CA Certificate
SCEPY_CA_X509_CN = 'SCEPY-CA'
SCEPY_CA_X509_O = 'SCEPy'
SCEPY_CA_X509_C = 'US'

# Force a single certificate to be returned as a PKCS#7 Degenerate instead of raw DER data
SCEPY_FORCE_DEGENERATE_FOR_SINGLE_CERT = False
