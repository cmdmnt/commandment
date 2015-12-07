# coMmanDMent Open Source MDM

Commandment is an Open Source Apple MDM server with support for managing iOS and OS X devices implemented in Python. The source code is available under an [MIT license](LICENSE.txt).

## Architecture

* Entirely Python implementation
* Ground-up design based on Flask using an SQL backend for persistence
* Native Certificate Authority built-in to support generating and signing of unique individual device identity, development webserver, and other certificates

## Requirements

* DNS name for server
* Apple MDM Push Certificate and private key (in PEM format)
  * Requires an Apple Enterprise Developer account (US$300/year)
* [Python](https://www.python.org/) 2.7+, [M2Crypto](http://chandlerproject.org/Projects/MeTooCrypto), [pyOpenSSL](https://github.com/pyca/pyopenssl), [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), and [SQLite](https://www.sqlite.org/) (default database)
* For instructions on how to install these dependences on OS X please refer to the installation instructions

## Installation and Setup

Please read the [INSTALL file](INSTALL.md).

## Bugs, issues, etc.

Please report any issues, bugs, suggestions, feedback, etc. to the [issue tracker](../../issues) of this project.

## Known issues and limitations

Much of this is planned to be addressed or implemented, but noting it here so folks aren't surprised when they notice the (sometimes gaping) holes.

* Holy *moly* what a crappy looking UI. Hand-edited raw HTML without CSS *ftw!* To integrate Bootstrap or something soon.
* No authentication for the admin pages (yet)
* No database "migrations" support. Any change to database schema (and there will be many) will likely **require deleting the database** and re-creating. This means re-enrollment of any previously enrolled devices.
* The current profile editing UI is hard-coded to, yes, one single key in one single payload in one profile. Need to massively expand support for Profile editing and profile upload.
* Support for some very basic MDM operations is simply lacking right now like locking, wiping/erasing, etc.
* OS X MDM supports per-user management. While stub code exists to authenticate users we don't support any actual per-user MDM management yet (but intend to).
* No UI to perform MDM Vendor Signing or any Apple certificate integration.
* No profile signing (yet). Most noticeable for the initial enrollment profile. MDM-managed profiles may not need signing.
* Push notifications are currently set to immediately expire for testing (no retries on failure). Need to perform testing and possibly implement MDM push timeout/re-send logic.
* Error handling and failures and fallbacks needs work all over the place.
* While support for client-supplied certificate validation is straigt-forward to add it will only work with a web server that supports it. Our architecture is such that administrator web end-points *and* MDM commands flow through the same webserver instance. This means if we had a webserver that requested client certificates then the admin pages would (annoyingly) ask the administrator for a client certificate. We're currently using MDM HTTP request signing transmitted via HTTP headers which unfortauntely increase each MDM request size by ~ 2 KB
* No example WSGI setup for using another non-development web server
* No support for SCEP enrollment
* Only device group modification triggers profile modification on devices currently. Profile modification, deletion, profile group addition/removal should all trigger device modification.
