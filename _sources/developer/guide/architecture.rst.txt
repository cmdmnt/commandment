Architecture
============

Backend
-------

The backend is a `Flask <http://flask.pocoo.org/>`_ application which is expected to run on **Python 3.6+**
using type annotations.

The persistence layer is handled using SQLAlchemy via `Flask-SQLAlchemy <http://flask-sqlalchemy.pocoo.org/>`_.
Database schema migrations are performed by `Alembic <http://alembic.zzzcomputing.com/en/latest/>`_.

The REST API follows the `JSON-API standard <http://jsonapi.org/format/>`_ using
`Flask-REST-JSONAPI <https://flask-rest-jsonapi.readthedocs.io/en/latest/>`_.

API that fits an RPC model better than a REST model is serialized using `marshmallow <https://marshmallow.readthedocs.io/en/latest/>`_
which is what **Flask-REST-JSONAPI** uses anyway.

Frontend
--------

The frontend framework is `React <https://facebook.github.io/react/>`_, using `Redux <http://redux.js.org/>`_ for state
management. The source is written in `TypeScript <https://www.typescriptlang.org/>`_ and transpiled to ES5.

The UI framework/CSS framework is `semantic-ui <https://semantic-ui.com/>`_. We use the React components for this as well.


