Dependencies
============


Installing backend dependencies
-------------------------------

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

NodeJS 7+
^^^^^^^^^

All of the front end tooling requires NodeJS. You can download and install an official package from `here <https://nodejs.org/en/>`_.
I use `nvm <https://github.com/creationix/nvm>`_ to run multiple NodeJS versions at a time, for testing purposes.

Setting up the environment
--------------------------

This part will assume that you have now cloned the git repository somewhere on your system. Usually within your own
home folder.

Virtualenv
^^^^^^^^^^

Because we want to keep all the dependency versions tied to the project and not mixed in with other python projects on
your system, we use `virtualenv <https://virtualenv.pypa.io/en/stable/>`_.

If you don't have virtualenv for some reason, you can run::

    $ pip3 install virtualenv

To install it for use with python 3.

To create a new virtualenv, called **venv**, run this in the cloned repository location::

    $ virtualenv -p python3.6 venv

This will create a new virtualenv specifically for Python 3.6, inside the **venv** directory.

Before we can install all of the commandment dependencies, we need to activate the virtual environment. This is so the
dependencies are installed into **venv** and not **/usr/local** somewhere.

To activate the virtualenv run::

    $ . ./venv/activate

Your prompt should then change to ``(venv) hostname:dir $``.

Python dependencies
^^^^^^^^^^^^^^^^^^^

Now that the virtualenv is active, we can install all of the Python dependencies, using the **requirements.txt** in the
repository.

.. note:: In a normal setup, the dependencies listed in setup.py would be used instead.

Run this command to fetch all of the Python dependencies::

    $ pip install -r ./requirements.txt

Now you're done with all the backend, you can move on to the front end build process.

Front end dependencies
----------------------

All of the front end code is contained within the **ui** subdirectory, so make that your current working directory.

.. note:: The Python virtualenv has zero impact on the front end build

First, you need to install all of the **node** dependencies. For this i recommend `yarn <https://yarnpkg.com>`_, which you
can install by running::

    $ brew install yarn

Then, to install all front end dependencies you can run::

    $ yarn install

From the ui directory.

You now have the tools to develop both the backend and front end code.


