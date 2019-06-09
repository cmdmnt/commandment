Installation on Ubuntu
======================

This guide was written using Ubuntu Server 19.04. Amendments are welcome for different versions.
This guide assumes you are a regular user who is part of the sudoers group.

1. Dependencies
---------------

Install packages::

	sudo apt-get update
	sudo apt install -y python3 python3-venv nginx uwsgi uwsgi-plugin-python3 nodejs npm pipenv

Clone the project into /var/www::

	sudo git clone https://github.com/cmdmnt/commandment.git /var/www/commandment

Install backend dependencies::

	$ cd /var/www/commandment
	$ sudo python3 -m venv virtualenv
	$ . ./virtualenv/bin/activate
	(virtualenv)$ sudo -E pipenv --python /usr/bin/python3 install

Install frontend dependencies::

	$ cd /var/www/commandment/ui
	$ sudo npm install

2. Backend
----------

2.1 uWSGI
^^^^^^^^^

uWSGI runs multiple copies of the backend to service requests.

Create a new uWSGI configuration in /etc/uwsgi/apps-available/commandment.ini

If you are following this guide use the template below, which you can adjust later if you want to move locations of
various components::

	cat <<EOF |sudo tee /etc/uwsgi/apps-available/commandment.ini

		[uwsgi]
		base = /var/www/commandment
		pythonpath = %(base)
		module = commandment:create_app()

		home = /var/www/commandment/virtualenv
		plugins = python3

		env = COMMANDMENT_SETTINGS=/var/www/commandment/settings.cfg
		master = true
		processes = 4
		enable-threads = true

		socket = /var/run/uwsgi-commandment.sock
		chmod-socket = 660

		die-on-term = true

		# Use this log to debug startup or app failures
		logto = /var/log/uwsgi/app/commandment.log
	EOF


Symlink to **apps-enabled**::

	sudo ln -s /etc/uwsgi/apps-available/commandment.ini /etc/uwsgi/apps-enabled/commandment.ini

Verify that the backend actually starts::

	$ sudo systemctl restart uwsgi
	$ sudo tail -f /var/log/uwsgi/app/commandment.log

You will see errors about the settings file missing, because we haven't configured commandment yet!
You should at least see something like::

	Sun Jun  9 12:55:41 2019 - spawned uWSGI master process (pid: 13435)
	Sun Jun  9 12:55:41 2019 - spawned uWSGI worker 1 (pid: 13442, cores: 1)


2.2 NGiNX
^^^^^^^^^

Configure NGiNX to pass requests to uWSGI (if backend is required), or static assets (for frontend).

Decide on a DNS name for your installation. This will later require certificates, and your devices cannot be moved without
re-enrollment. So it's going to be a pain to change. For a sandbox LAN install you might even choose a bonjour name

Generate a self-signed or properly signed SSL certificate for your fqdn.

Add an NGiNX configuration accordingly to /etc/nginx/sites-available/commandment.conf, using the following as a guide::

	cat <<"EOF" |sudo tee /etc/nginx/sites-available/commandment.conf
		server {
		  listen 443 ssl;
		  ssl_certificate /etc/ssl/certs/commandment.crt;
		  ssl_certificate_key /etc/ssl/private/commandment.key;
		  ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

		  root /var/www/commandment/commandment/static;
		  index index.html;

		  access_log /var/log/nginx/commandment-access.log;
		  error_log /var/log/nginx/commandment-error.log;

		  location /api {
			include uwsgi_params;
			uwsgi_param HTTP_X_CLIENT_CERT $ssl_client_cert;
			uwsgi_pass unix:/var/run/uwsgi-commandment.sock;
		  }

		  location /enroll {
			include uwsgi_params;
			uwsgi_param HTTP_X_CLIENT_CERT $ssl_client_cert;
			uwsgi_pass unix:/var/run/uwsgi-commandment.sock;
		  }

		  location /checkin {
			include uwsgi_params;
			uwsgi_param HTTP_X_CLIENT_CERT $ssl_client_cert;
			uwsgi_pass unix:/var/run/uwsgi-commandment.sock;
		  }

		  location /mdm {
			include uwsgi_params;
			uwsgi_param HTTP_X_CLIENT_CERT $ssl_client_cert;
			uwsgi_pass unix:/var/run/uwsgi-commandment.sock;
		  }

		  location /scep {
			include uwsgi_params;
			uwsgi_param HTTP_X_CLIENT_CERT $ssl_client_cert;
			uwsgi_pass unix:/var/run/uwsgi-commandment.sock;
		  }

		  location / {
			try_files $uri /index.html;
		  }

		  location /static {
			alias /var/www/commandment/commandment/static;
		  }
		}
	EOF

Symlink to **sites-enabled**::

	sudo ln -s /etc/nginx/sites-available/commandment.conf /etc/nginx/sites-enabled/commandment.conf

2.3 SSL Certificate(s)
^^^^^^^^^^^^^^^^^^^^^^

NGiNX will fail to start until we actually create an SSL certificate for this site.

If this is a non-public, development, sandbox environment you can use a self-signed certificate. If you ever intend to
make it public (internet) facing, you need to sort out SSL certificates, maybe with LetsEncrypt.


To use self-signed certificates, first check that your hostname will be the fqdn that devices can access your machine with::

	$ hostnamectl

If the **Static hostname:** can't be resolved from another computer or device, the SSL cert generated in the next section
won't work.

Generate self-signed certificates::

	$ sudo apt install ssl-cert
	$ sudo make-ssl-cert generate-default-snakeoil --force-overwrite

This will generate a cert/key pair in /etc/ssl/certs/ssl-cert-snakeoil.pem and /etc/ssl/private/ssl-cert-snakeoil.key
respectively. Update the ``ssl_certificate`` and ``ssl_certificate_key`` directives in the NGiNX config.



