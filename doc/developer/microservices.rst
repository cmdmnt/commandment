Microservices Architecture
==========================

MDM only has certain limitations which means that microservices have only a limited range of definition in terms of where
dependent services can live.

Here's some ideas for services


DEP Scanner + Default Profiler
------------------------------

- Some process needs to scan/sync DEP
- This is a good point in time to evaluate which DEP profile should be assigned to the devices as they come in.
- If there was a rules based evaluation of DEP profile assignment, that could also happen here.
- Manual DEP assignment does NOT have to live here, because it is performed imperatively against collections of objects.
- This process can create new device records when it finds new DEP records. These can exist in a "pre-enrolled" state.


APNS Pusher
-----------

- Most MDM systems have some sort of Queue monitor/APNS push watcher.
- After a certain amount of time, devices with >0 commands to send are evaluated.
- Some commands are imperative and you would expect them to happen almost immediately (Shutdown, Restart). with exception
  to device collections larger than 100, where the push may take some time.
- Some commands are expected to happen in good time (InstallProfile, InstallApplication).


Inventory
---------

- End users expect REASONABLY recent device inventory.
- Some process needs to Queue inventory commands at a refresh interval, but not queue all devices at once.
- It must also not queue commands if they are already queued.
- It must also not queue commands for recently refreshed inventory.


Profiles
--------

- Try not to introspect profile payload structure because it can literally be anything almost.
- Examine desired profiles vs installed profiles and create a command for it.


Applications
------------

- Same theoretical application as PRofiles but with a different object type.

Calculated Groups (Classifier)
------------------------------

- Isolate a sub-population of devices by attribute predicates.
- Many cloud providers de-prioritise the calculation of these groups in order to reduce impact, but this also results in
  sluggish feedback.
- Tactics for speeding up or lessening impact of calculated groups:
  - Do not recalculate if inventory data did not change: therefore track devices which did change in the last x duration.
  - Newly created groups must force a recalculation of membership immediately to provide feedback to the user.
  - Compound predicates are the union intersection of simple predicates, so maybe this can be exploited to lower the cost
    of group calculation.
  - Consider groupable attributes for indexing
- Groups can be used to functionally identify the workflow state of a device from its pre-enrolled DEP state through
  DeviceConfigured into enrolled.
- Pre-defined groups:
  - By form factor (Desktop, Tablet, Phone, ATV)
  - Workflow state (DEP -> AwaitConfiguration -> Enrolled -> Stale -> Unenrolled)
  - OS Flavour+Major Version (becomes a derivative of form factor groups)
	- Minor Version (becomes a derivative of major version)
  - Cellular v non cellular (subset of union Tablet+Phone)
- Freestyle composite groups:
  - Nominate a pre-defined group to limit calculation results.
  - Enforce a predicate on that.


Reaper
------

- Scan age of devices and mark them as Stale if no communications recently.
- Unenroll devices once they have not communicated in a long amount of time,
