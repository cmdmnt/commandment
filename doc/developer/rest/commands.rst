Commands
========

Summary
-------



Detail
------

.. autoflask:: commandment:create_app()
    :blueprints: api_app

.. http:get:: /api/v1/commands

   Get all commands

   :reqheader Accept: application/vnd.api+json
   :resheader Content-Type: application/vnd.api+json

.. http:post:: /api/v1/commands

   Create a command

.. http:patch:: /api/v1/commands/(int:command_id)

   Update a command

.. http:delete:: /api/v1/commands/(int:command_id)

   Delete a command

.. http:get:: /api/v1/devices/(int:device_id)/commands

   Get MDM commands associated with the device specified by **device_id**

.. http:all:: /api/v1/devices/(int:device_id)/relationships/commands

   Attach/Detach command relationships to specific devices

