Installation on Ubuntu
======================

This guide was written using Ubuntu Server 19.04. Amendments are welcome for different versions.
This guide assumes you are a regular user who is part of the sudoers group.

1. Dependencies
---------------

Install packages::

	sudo apt install -y python3 python3-venv nginx uwsgi uwsgi-plugin-python3 nodejs npm pipenv

Clone the project into /var/www::

	sudo git clone https://github.com/cmdmnt/commandment.git /var/www/commandment

Install backend dependencies::

	$ cd /var/www/commandment
	$ python3 -m venv virtualenv
	$ . ./virtualenv/bin/activate
	(virtualenv)$ pipenv --python /usr/bin/python3 install

Install frontend dependencies::

	$ cd /var/www/commandment/ui
	$ npm install

2. Backend
----------

2.1 uWSGI
^^^^^^^^^

uWSGI runs multiple copies of the backend to service requests.

Create a new uWSGI configuration in /etc/uwsgi/apps-available/commandment.ini

If you are following this guide use the template below, which you can adjust later if you want to move locations of
various components::

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


Symlink to **apps-enabled**::

	sudo ln -s /etc/uwsgi/apps-available/commandment.ini /etc/uwsgi/apps-enabled/commandment.ini

Verify that the backend actually starts::

	systemctl restart uwsgi

2.2 NGiNX
^^^^^^^^^

Configure NGiNX to pass requests to uWSGI.

Decide on a DNS name for your installation. This will later require certificates, and your devices cannot be moved without
re-enrollment. So it's going to be a pain to change.

Generate a self-signed or properly signed SSL certificate for your fqdn.

Add an NGiNX configuration accordingly to /etc/nginx/sites-available/commandment.conf, using the following as a guide::

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

Symlink to **sites-enabled**::

	sudo ln -s /etc/nginx/sites-available/commandment.conf /etc/nginx/sites-enabled/commandment.conf

Verify that NGiNX actually starts::

	systemctl restart uwsgi


