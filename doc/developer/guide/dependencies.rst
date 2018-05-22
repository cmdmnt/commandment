Dependencies
============

These are the dependencies for developing with commandment. You won't need all of these to actually run it.

Quick Start (Using Homebrew)
----------------------------

First clone the repository, then install dependencies::

	$ brew install python3 nodejs yarn
	$ pip install pipenv
	$ pipenv install
	$ cd ui && yarn install


The long version
----------------

Python 3.6+
^^^^^^^^^^^

Commandment is written using Python 3.6, and uses type annotations as provided by the
`typing <https://docs.python.org/3/library/typing.html>`_ module.

macOS ships with Python 2.7, so you will need to have a separate instance of Python 3.6 installed on your system.
You can use `Homebrew <https://brew.sh>`_ to install Python 3.6 alongside the system provided Python 2.7.

It's as easy as::

    $ brew install python3

You can also get an isolated environment using something such as `Anaconda <https://www.continuum.io/downloads>`_, which
is not covered here.

On Linux you should be able to install python 3 using your distributions packaging tools such as **yum** or **apt-get**.

NodeJS 7+
^^^^^^^^^

All of the front end tooling requires NodeJS. You can download and install an official package from `here <https://nodejs.org/en/>`_.
I use `nvm <https://github.com/creationix/nvm>`_ to run multiple NodeJS versions at a time, for testing purposes.
You may also run::

	$ brew install nodejs


Setting up the environment
--------------------------

This part will assume that you have now cloned the git repository somewhere on your system. Usually within your own
home folder.

Pipenv
^^^^^^

To download the Python dependencies, you first need `pipenv <https://docs.pipenv.org/>`_. You can install pipenv by
running::

	$ pip install pipenv

See the **pipenv** documentation for information about how to install it on other Linux distributions.

Python dependencies
^^^^^^^^^^^^^^^^^^^

To install python dependencies, change to the commandment directory and run::

	$ pipenv install

This should download and install all python requirements into a new virtualenv.

.. note:: This supersedes the :file:`requirements.txt` method.

Front end dependencies
----------------------

All of the front end code is contained within the **ui** subdirectory, so make that your current working directory.

First, you need to install all of the **node** dependencies. For this i recommend `yarn <https://yarnpkg.com>`_, which you
can install by running::

    $ brew install yarn

Then, to install all front end dependencies you can run::

    $ yarn install

From the ui directory.

You now have the tools to develop both the backend and front end code.
