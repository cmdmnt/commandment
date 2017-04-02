# coMmanDMent Open Source MDM

Commandment is an Open Source Apple MDM server with support for managing iOS and macOS devices implemented in Python. The source code is available under an [MIT license](LICENSE.txt).

![Screenshot](http://i.imgur.com/Wfx4aaJ.png)

## Architecture

* Pure Python implementation
* Ground-up design based on Flask using an SQL backend for persistence
* Native Certificate Authority built-in to support generating and signing of unique individual device identity, development webserver, and other certificates

## Requirements

* DNS name for server
* Apple MDM Push Certificate and private key (in PEM format)
  * Obtain a free Push Certificate from [https://mdmcert.download](https://mdmcert.download)
  * Alternatively requires an Apple Enterprise Developer account (US$300/year)
* [Python](https://www.python.org/) 2.7+
* Major Python dependencies:
  * [M2Crypto](https://gitlab.com/m2crypto/m2crypto)
  * [pyOpenSSL](https://github.com/pyca/pyopenssl)
  * [Flask](http://flask.pocoo.org/)
  * [SQLAlchemy](http://www.sqlalchemy.org/)
  * [and more..](requirements.txt)
* For instructions on how to install these dependences on macOS please refer to the installation instructions

## Installation and Setup

Please read the [INSTALL file](INSTALL.md).

## Bugs, issues, etc.

Please report any issues, bugs, suggestions, feedback, etc. to the [issue tracker](https://github.com/jessepeterson/commandment/issues) of this project.

## Known issues and limitations (I.e. the TODO list)

Much of this is planned to be addressed or implemented, but noting it here so folks aren't surprised when they notice the (sometimes gaping) holes.

* No database "migrations" support. Any change to database schema (and there will be many) will likely **require deleting the database** and re-creating. This means re-enrollment of any previously enrolled devices.
* The current profile editing UI is hard-coded to, yes, one single key in one single payload in one profile. Need to massively expand support for Profile editing and profile upload.
* Support for some very basic MDM operations is simply lacking right now like locking, wiping/erasing, etc.
* Major logging improvements
* macOS MDM supports per-user management. While stub code exists to authenticate users we don't support any actual per-user MDM management yet (but intend to).
* No UI to perform MDM Vendor Signing or any Apple certificate integration.
* No profile signing (yet). Most noticeable for the initial enrollment profile. MDM-managed profiles may not need signing.
* Error handling and failures and fallbacks needs work all over the place.
* Configurable support for webserver client certificate validation
* No example WSGI setup for using another non-development web server
* Only device group modification triggers profile modification on devices currently. Profile modification, deletion, profile group addition/removal should all trigger device modification.
* Separability of runner thread in own process (may imply some form of IPC)
