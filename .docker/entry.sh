#!/usr/bin/env bash

PYTHONPATH=/commandment
export PYTHONPATH

/usr/local/bin/alembic upgrade head
exec /usr/bin/supervisord
