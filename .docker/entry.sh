#!/usr/bin/env bash

PYTHONPATH=/commandment
export PYTHONPATH

touch /commandment.db
/usr/local/bin/alembic upgrade head
exec /usr/bin/supervisord
