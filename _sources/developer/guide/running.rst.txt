Running
=======

Backend
-------

Before you get started, make a copy of ``settings.cfg.example`` and name it ``settings.cfg``.

Note the settings for ``SSL_CERTIFICATE`` and ``SSL_RSA_KEY``. SSL Certificates are required to run an MDM.
You'll have to generate those yourself, and they can be self-signed as long as you install trust profiles on your test
device(s).



If you want to use Python debugging, it's a lot easier with the Flask development server. This is the recommended way
to develop commandment.

Because MDM requires an SSL connection, the ``flask run`` command won't work out of the box.

For this, We've provided a command line application which runs the development server with an SSL context.
The command line application is contained in ``commandment.cli``.

Assuming you have installed all the Pipenv dependencies, run::

	COMMANDMENT_SETTINGS=/path/to/settings.cfg pipenv run commandment

From the checked-out git repository.

This will start an SSL server on port 5443, using the private key and certificate specified in the :file:`settings.cfg`.

.. note:: The backend will assume that you are also running a webpack-dev-server [#f1]_ (front end dev server) if the
	setting ``DEBUG = True``. This is extremely useful for seeing javascript changes on the fly.

Database
--------

commandment is configured by default to use an SQLite database (commandment.db) in the same directory as the repository.

To initialise the database you should use the ``alembic`` tool, which was part of our python dependencies.

To do this, change to the commandment directory and run::

	$ pipenv run alembic upgrade head

This runs the alembic tool inside the pipenv virtual environment.

Frontend
--------

When running the backend on the dev server, front-end assets will be loaded from **localhost** on port **4000**.

To start the webpack dev server [#f1]_, run the following command inside the :file:`ui` directory::

	NODE_ENV=development npm start

You should see some output indicating that the webpack-dev-server is running on port 4000.

The webpack dev server is configured to use the same SSL certificate and private key as the Flask backend by default.
In some browsers you will have to trust BOTH the python backend on 5443 and the webpack-dev-server on port 4000.

It helps if they are using the same hostname and ssl certificates.



.. rubric:: Footnotes

.. [#f1] `webpack-dev-server <https://webpack.js.org/configuration/dev-server/>`_.