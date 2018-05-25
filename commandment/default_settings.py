# http://flask-sqlalchemy.pocoo.org/2.1/config/
SQLALCHEMY_DATABASE_URI = 'sqlite:///commandment/commandment.db'
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
SQLALCHEMY_TRACK_MODIFICATIONS = False
PORT = 5443

# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'

PLISTIFY_MIMETYPE = 'application/xml'

