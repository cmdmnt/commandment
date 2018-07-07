Installation
============

macOS
-----

.. note:: macOS is not a recommended platform for hosting an MDM. However, you can use it to test commandment.

Manual Installation
^^^^^^^^^^^^^^^^^^^

- Install `Homebrew <https://brew.sh/>`_.
- Install Pre-requisites::

    $ brew install python3
    $ brew install uwsgi --with-python --with-python3
    $ brew install nginx

- *TODO: upload release tarball. For now you will need to git clone* Unpack commandment to :file:`/usr/local/commandment`.
- Use this example NGiNX configuration (:download:`download </_static/config/nginx-commandment.conf>`).
  Copy the downloaded file to :file:`/usr/local/etc/nginx/servers/commandment.conf`.
- Use this example uWSGI configuration (:download:`download </_static/config/uwsgi-commandment.ini>`).
  Copy the downloaded file to :file:`/usr/local/etc/uwsgi/apps-enabled/uwsgi-commandment.ini`.

SSL
^^^

MDM more or less requires an SSL certificate. The example NGiNX configuration file above expects a private key, located
at :file:`/usr/local/commandment/server.key` and a certificate, located at :file:`/usr/local/commandment/server.crt`.

For a production instance, you will require an SSL certificate issued by a 3rd party for the chosen domain. However,
as this is a macOS installation guide, I'm assuming that this is only a sandbox.

**To generate a self-signed certificate using OpenSSL**:

Some browsers now require a SubjectAltName attribute, so you won't be able to do this whole certificate in one command.

- Create a file called :file:`req.conf` to use with OpenSSL, with the following contents::

    [req]
    distinguished_name = req_distinguished_name
    x509_extensions = v3_req
    prompt = no
    [req_distinguished_name]
    C = US
    ST = VA
    L = SomeCity
    O = MyCompany
    OU = MyDivision
    CN = www.company.com
    [v3_req]
    keyUsage = keyEncipherment, dataEncipherment
    extendedKeyUsage = serverAuth
    subjectAltName = @alt_names
    [alt_names]
    DNS.1 = www.company.net
    DNS.2 = company.com
    DNS.3 = company.net

- Remove or replace DNS.2, DNS.3 if you only have a single hostname for this MDM.
- Alter **DNS.1** so that it matches the hostname that your browser and MDM devices would connect to. If you are only
  testing within a small LAN you can even use the bonjour name **computername.local**.
- If you care for accuracy you can fill out OU, O, L, ST, C to match your information.
- The **CN** should also match your hostname as this can also be used to evaluate trust.
- TODO: need more detail here.
- Create the RSA key/CSR::

    openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout cert.pem -out cert.pem -config req.conf -extensions 'v3_req'


Push Notification Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO



.. note:: At this stage you should have an MDM Push Certificate and SSL Certificate ready so that your devices will talk
    to the MDM service. You should also decide whether to use `SCEPy <https://github.com/mosen/SCEPy>`_ for testing or
    another SCEP service such as Microsoft NDES.
