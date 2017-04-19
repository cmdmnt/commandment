Building Commandment
====================

Install Python 3
----------------

Commandment requires python >= 3.5 for its type annotation support.
On the mac you can install python 3 via _`Homebrew <https://brew.sh>` like so::

    $ brew install python3

If you are running commandment on linux, python 3 will be available via your package manager of choice.

Create VirtualEnv
-----------------

To keep dependencies with the project, you should create a
_`VirtualEnv <https://virtualenv.pypa.io/en/stable/userguide/#usage>`.

For example, if you have the project as your current working directory, you can type::

    $ virtualenv venv

To create a VirtualEnv in the ``venv`` folder.

You will need to **activate** the virtualenv before dependencies will be installed there, like so::

    $ . ./venv/bin/activate

Install Python Dependencies
---------------------------

To install dependencies into the virtualenv, run the ``setup.py`` with develop so that commandment is linked instead of
installed::

    $ python setup.py develop




