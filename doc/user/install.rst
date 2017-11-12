Installation
============

macOS
-----

Manual Installation
^^^^^^^^^^^^^^^^^^^

- Install `Homebrew <https://brew.sh/>`_.
- Install Python 3 from Homebrew by typing::

    $ brew install python3

  At a Terminal command prompt.

.. note:: You can check the version that was installed by running ``python3 --version``. It should be 3.6 or greater.

- Clone commandment down from the github repository::

    $ git clone https://github.com/cmdmnt/commandment.git

- Create a VirtualEnv just for commandment using python3, and activate it. In the git cloned directory::

    $ virtualenv -p python3.6 venv
    $ . ./venv/bin/activate

- Install commandment and its python dependencies by running **setup.py** like so::

    $ python setup.py develop

- Copy the example settings, ``settings.cfg.example`` to ``settings.cfg`` and modify to suit your environment.

.. note:: At this stage you should have an MDM Push Certificate and SSL Certificate ready so that your devices will talk
    to the MDM service. You should also decide whether to use `SCEPy <https://github.com/mosen/SCEPy>`_ for testing or
    another SCEP service such as Microsoft NDES.
