Developer Guide
===============

This guide explains how to get commandment set up for development.
The guide only covers macOS at this point in time.

Installing dependencies
-----------------------

Python 3.5+
^^^^^^^^^^^

Commandment is written using Python 3.5, and its supported `typing <https://docs.python.org/3/library/typing.html>`_
type annotations.

macOS ships with Python 2.7, so you will need to have a separate instance of Python 3.5 installed on your system.
You can use `Homebrew <https://brew.sh>`_ to install Python 3.5 along side the system provided Python 2.7.

It's as easy as::

    $ brew install python3

You can also get an isolated environment using something such as `Anaconda <https://www.continuum.io/downloads>`_, which
is not covered here.

NodeJS 7+
^^^^^^^^^

All of the front end tooling requires NodeJS. You can download and install an official package from `here <https://nodejs.org/en/>`_.
