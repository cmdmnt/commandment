Nginx Configuration
===================

If you are using commandment behind Nginx, Nginx will be terminating the SSL connection, therefore commandment is unable
to manage the SSL certificates for you. You should always pass the client certificate back up to commandment so that
the validity of the device certificate can be determined using CA's stored in commandment.


With uWSGI
----------

Example configuration (with uWSGI)::

    server {
        listen 443 ssl;
        server_name commandment.dev;
        ssl_certificate commandment.dev.crt;
        ssl_certificate_key commandment.dev.key;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_verify_client optional_no_ca;

        root /path/to/commandment/static;
        access_log commandment-access.log;
        error_log commandment-error.log;

        location / { try_files $uri @commandment; }
        location @commandment {
            include uwsgi_params;
            uwsgi_param HTTP_X_CLIENT_CERT $ssl_client_cert;
            uwsgi_pass unix:/tmp/uwsgi.sock;
        }
    }


References:
- http://uwsgi-docs.readthedocs.io/en/latest/Nginx.html
- http://flask.pocoo.org/docs/0.12/deploying/uwsgi/

With Gunicorn
-------------


With Phusion Passenger
----------------------

Example configuration::

    server {
        listen 443 ssl;
        server_name commandment.dev;
        ssl_certificate commandment.dev.crt;
        ssl_certificate_key commandment.dev.key;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_verify_client optional_no_ca;

        root /path/to/commandment/static;
        access_log commandment-access.log;
        error_log commandment-error.log;

        passenger_enabled on;
    }


