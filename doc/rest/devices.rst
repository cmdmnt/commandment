Devices
=======

.. autoflask:: commandment:create_app()
    :blueprints: api_app

.. http:get:: /api/v1/devices

   Get a list of devices

   :reqheader Accept: application/vnd.api+json
   :resheader Content-Type: application/vnd.api+json

.. http:get:: /api/v1/devices/(int:device_id)

   Get information about a specific device.

.. http:post:: /api/v1/devices

   Create a new enrolled device

.. http:patch:: /api/v1/devices/(int:device_id)

   Update an enrolled device

.. http:delete:: /api/v1/devices/(int:device_id)

   Delete an enrolled device

.. http:get:: /api/v1/devices/(int:device_id)/commands

   Get MDM commands associated with this device.

.. http:get:: /api/v1/devices/(int:device_id)/tags

   Get tags associated with this device.

