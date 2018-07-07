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
as this is a macOS installation guide, You may also use a self-signed certificate.


.. note:: Creating SSL certificates is outside of the scope of this document.


Push Notification Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need a push certificate to tell devices when to check-in.

You have three options:

- Sign up for an Apple Enterprise Developer Account (ca. $400 USD). Enable the MDM option and sign your own Push Certificate
  request.
- Register on `mdmcert.download <https://mdmcert.download/>`_.
- Export the Push Certificate from Profile Manager (really not supported).

This guide follows the **mdmcert.download** workflow.

- First, register on `mdmcert.download <https://mdmcert.download/>`_. The e-mail address you use will be the one that
  receives all notifications and certificate signing requests.
- *TODO* visit ``/apns/mdmcert`` using the web ui to request a new CSR.
- *TODO* upload the CSR received in your e-mail to this same page.
- *TODO* download the decrypted CSR for upload to the APNS portal.
- Go to the Apple Push Certificate Portal and upload the CSR.
- Download the resulting push certificate.


.. note:: At this stage you should have an MDM Push Certificate and SSL Certificate ready so that your devices will talk
    to the MDM service. You should also decide whether to use `SCEPy <https://github.com/mosen/SCEPy>`_ for testing or
    another SCEP service such as Microsoft NDES.

Configuration
^^^^^^^^^^^^^

An example configuration file, called :file:`settings.cfg.example` is supplied with commandment.

You should copy this file to a file named :file:`settings.cfg` and make updates as needed.

Each setting is documented within the file.

