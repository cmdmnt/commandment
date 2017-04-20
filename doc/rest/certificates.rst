Certificates
============

JSON-API Endpoints
------------------

.. http:get:: /api/v1/certificates/

    Retrieve a list of all metadata about certificates stored in the system.

    :query page[size]: The number of items to return for each page
    :query page[number]: The page to fetch
    :query filter[]: An array of filtering rules
    :query sort: A list of fields (separated by comma) to sort ascending.
                 Mark with a **-** minus to denote descending sort.
    :reqheader Accept: application/vnd.api+json
    :resheader Content-Type: application/vnd.api+json

.. http:post:: /api/v1/certificates/

    Add a new certificate to the system.

.. http:get:: /api/v1/certificates/(int:certificate_id)

    Retrieve metadata about the certificate (`certificate_id`)

    **Example request**:

    .. sourcecode:: http

        GET /api/v1/certificates/1 HTTP/1.1
        Accept: application/vnd.api+json

    **Example response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/vnd.api+json

        {
            "data": [{
                "type": "certificates",
                "attributes": {
                    "not_after": "2018-03-26T23:42:09+00:00",
                    "pem_certificate": "-----BEGIN CERTIFICATE----ABCDEF==\n-----END CERTIFICATE-----\n",
                    "subject": "commandment.dev",
                    "purpose": "mdm.cacert",
                    "not_before": "2017-03-26T23:42:09+00:00"
                },
                "id": 1,
                "links": {
                    "self": "/api/v1/certificates/1"
                }
            }],
            "meta": {"count": 1},
            "jsonapi": {"version": "1.0"}
        }

    :reqheader Accept: application/vnd.api+json
    :resheader Content-Type: application/vnd.api+json
    :statuscode 200:
    :statuscode 404:



Other Endpoints
---------------

.. autoflask:: commandment:create_app()
    :blueprints: api_app