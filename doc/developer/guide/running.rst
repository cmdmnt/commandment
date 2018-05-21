Running
=======

Backend
-------

If you want to use Python debugging, it's a lot easier with the Flask development server.

Because MDM requires an SSL connection, the ``flask run`` command won't work out of the box.

For this, We've provided a command line application which runs the development server with an SSL context.
The command line application is contained in ``commandment.cli``.

Assuming you have installed all the Pipenv dependencies, run::

	COMMANDMENT_SETTINGS=/path/to/settings.cfg pipenv run commandment

From the checked-out git repository.

This will start an SSL server on port 5443, using the private key and certificate specified in the :file:`settings.cfg`
as ``SSL_CERTIFICATE`` and ``SSL_RSA_KEY``. You'll have to generate those yourself, and they can be self-signed as long
as you install trust profiles on your device(s).

.. note:: The backend will assume that you are also running a webpack-dev-server (front end dev server) to dynamically
	reload any javascript assets on change.

Frontend
--------

When running the backend on the dev server, front-end assets will be loaded from **localhost** on port **4000**.

To start the webpack dev server [#f1]_, run the following command inside the :file:`ui` directory::

	NODE_ENV=development npm start

You should see some output indicating that the webpack-dev-server is running on port 4000.

The webpack dev server is configured to use the same SSL certificate and private key as the Flask backend by default.



.. rubric:: Footnotes

.. [#f1] `webpack-dev-server <https://webpack.js.org/configuration/dev-server/>`_.