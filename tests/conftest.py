import pytest
import os
from flask import Flask
from typing import Generator
from commandment import create_app
from commandment.models import db as _db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from tests.client import MDMClient
from alembic.command import upgrade
from alembic.config import Config


TEST_DIR = os.path.realpath(os.path.dirname(__file__))
ALEMBIC_CONFIG = os.path.realpath(TEST_DIR + '/../../alembic.ini')


def apply_migrations():
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')


@pytest.fixture(scope='session')
def app() -> Generator[Flask, None, None]:
    """Flask Application Fixture"""
    a = create_app()
    a.config['TESTING'] = True
    ctx = a.app_context()
    ctx.push()

    yield a

    ctx.pop()


@pytest.fixture(scope='session')
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Flask-SQLAlchemy Fixture"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_ECHO'] = False
    _db.init_app(app)
    _db.create_all()
    #apply_migrations()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def session(db: SQLAlchemy) -> Generator[scoped_session, None, None]:
    """SQLAlchemy session Fixture"""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='function')
def client(app: Flask) -> MDMClient:
    """Flask test client"""
    app.test_client_class = MDMClient
    test_client = app.test_client()
    return test_client

