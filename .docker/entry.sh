#!/usr/bin/env bash

echo "Starting commandment..."

PYTHONPATH=/commandment
export PYTHONPATH

echo "Initialising database..."
touch /commandment.db
/usr/local/bin/alembic --config /commandment/alembic.ini upgrade head

echo "Starting uWSGI and nginx"
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

