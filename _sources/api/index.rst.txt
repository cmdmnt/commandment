API Reference
=============

Almost all responses and requests are expected to follow the `JSON-API <http://jsonapi.org>`_ standard,
except in cases where binary or encoded data needs to be uploaded or downloaded,
*OR* the endpoint is a one-off RPC style action eg. "Erase Device".

All of the API is generated via the `flask-rest-jsonapi <http://flask-rest-jsonapi.readthedocs.io/en/latest/>`_ library.


.. toctree::
    :maxdepth: 2

    certificates
    commands
    dep
    devices
    organization
