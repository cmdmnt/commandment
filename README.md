# Commandment Open Source MDM

Commandment is an Open Source Apple MDM server with support for managing iOS and macOS devices implemented in Python. 
The source code is available under an [MIT license](LICENSE.txt).

## Requirements

* Apple MDM Push Certificate and private key (in PEM format)
  * Obtain a free Push Certificate from [https://mdmcert.download](https://mdmcert.download)
  * Alternatively requires an Apple Enterprise Developer account (US$300/year)
* [Python](https://www.python.org/) 3.6+
* Major Python dependencies:
  * [Flask](http://flask.pocoo.org/)
  * [SQLAlchemy](http://www.sqlalchemy.org/)
  * [and more..](requirements.txt)
* For instructions on how to install these dependences on macOS please refer to the installation instructions

## Documentation

The user, developer and API documentation is available at:

https://mosen.github.io/commandment/    

## Bugs, issues, etc.

Please report any issues, bugs, suggestions, feedback, etc. 
to the [issue tracker](https://github.com/mosen/commandment/issues) of this project.
