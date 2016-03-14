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
from sqlalchemy import Text, and_, or_
import json

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

class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()

    def update(self, *arg, **kwargs):
        self.changed()
        return dict.update(self, *arg, **kwargs)

class JSONEncodedDict(TypeDecorator):
    '''Represents an immutable structure as a json-encoded string'''
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return json.dumps(value, separators=(',', ':'))

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)

MutableDict.associate_with(JSONEncodedDict)
