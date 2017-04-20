Devices
=======

.. http:get:: /api/v1/devices

   Get information about a device

   :reqheader Accept: application/vnd.api+json
   :resheader Content-Type: application/vnd.api+json

.. http:post:: /api/v1/devices

   Create a new enrolled device

.. http:patch:: /api/v1/devices/(int:device_id)

   Update an enrolled device

.. http:delete:: /api/v1/devices/(int:device_id)

   Delete an enrolled device

.. http:get:: /api/v1/devices/(int:device_id)/commands

   Get MDM commands associated with this device.
