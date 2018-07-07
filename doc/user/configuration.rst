Configuration
=============

An example configuration `is provided <https://github.com/cmdmnt/commandment/blob/master/settings.cfg.example>`_ with
the source code.

It is recommended to copy this file to your own ``settings.cfg``, and make modifications to that file.

When commandment runs, it will expect an environment variable ``COMMANDMENT_SETTINGS``, that contains the full path
to the settings file.

Database Connection
-------------------

commandment uses SQLAlchemy as its database connection API. For more information about available configuration variables
see `Flask-SQLAlchemy Configuration <http://flask-sqlalchemy.pocoo.org/2.2/config/>`_.

For a testing setup, SQLite is more than adequate, so you will only need to add this line::

    SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/commandment/commandment.db'

To use a local SQLite database.

Self-Signed SSL Certificate
---------------------------

If your SSL certificate is self signed, or signed via an untrusted enterprise CA,
you will need to provide it as part of the configuration.

If your CA isn't already trusted throughout all of your clients (which is typically the case when you are self-signing),
you will need to provide the certificate eg::

    CA_CERTIFICATE="/path/to/CA.crt"


MDM Push Certificate
--------------------

If you have both the private and public key in **PEM** format, you can simply add a single variable pointing to that
file::

    PUSH_CERTIFICATE="/path/to/push.pem"

Otherwise, if you need to provide a **PKCS#12** ``.p12`` file, you will also need to specify a password::

    PUSH_CERTIFICATE="/path/to/push.p12"
    PUSH_CERTIFICATE_PASSWORD = "sekret"



Complete Reference
------------------

- For flask web application settings, refer to `Flask - Built In Configuration Values <http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values>`_.
- For database settings, refer to `Flask-SQLAlchemy Configuration <http://flask-sqlalchemy.pocoo.org/2.2/config/>`_.
