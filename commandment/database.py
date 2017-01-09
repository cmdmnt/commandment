'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import TypeDecorator
from sqlalchemy import Text, and_, or_, and_, update, insert, delete
import json
from datetime import datetime
import serializer

engine = None
mysessionmaker = sessionmaker()
db_session = scoped_session(mysessionmaker)

Base = declarative_base()
Base.query = db_session.query_property()

def config_engine(uri, echo):
    global engine, mysessionmaker, db_session

    engine = create_engine(uri, convert_unicode=True, echo=echo)
    db_session.remove()
    mysessionmaker.configure(autocommit=False, autoflush=False, bind=engine)

def init_db():
    global engine
    Base.metadata.create_all(bind=engine)

def json_datetime_serializer(o):
    '''Serialize datetime objects into ISO format string dates'''

    if isinstance(o, datetime):
        return o.isoformat()

    raise TypeError(repr(o) + " is not JSON serializable")

class JSONEncodedDict(TypeDecorator):
    '''Represents an immutable structure as a json-encoded string'''
    impl = Text
    encoding_cls = serializer.JSONMobileEncoder

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return json.dumps(value, separators=(',', ':'), cls=self.encoding_cls)

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)
