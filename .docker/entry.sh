#!/usr/bin/env bash

PYTHONPATH=/commandment
export PYTHONPATH

touch /commandment.db
/usr/local/bin/alembic --config /commandment/alembic.ini upgrade head
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

