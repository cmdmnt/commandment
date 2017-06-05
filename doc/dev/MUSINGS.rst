# Musings #

Dynamic device groups by attribute.
Problem: too slow to resolve group membership

Possible solutions: update group membership on change?

---

Problem: storage of dynamic group predicates




---

Group predicate attributes

model
os_version
enrolled / not enrolled
check in date/delta
device capacity <>

how about IN or NOT IN

has installed application(s) =>
has installed profile(s) => identifier in



Profile Install via Tag
=======================

- Device and profile share tag: Profile should be installed.
- Queue profile when tag changes or when device checks in?
    - If tag is subsequently removed, we have to manage the queue too.
    - VS: generate install while device checks in
- What if multiple tags are assigned to the same profile and the device is too?
    - Checking the queue gets more complex.
