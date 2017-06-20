from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
import json
from datetime import datetime
from sqlalchemy.types import TypeDecorator
from sqlalchemy import Text


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


def json_datetime_serializer(o):
    """Serialize datetime objects into ISO format string dates

    Raises:
        TypeError: If the https://mdmcert.download/api/v1/signrequestobject cannot be serialized.
    """

    if isinstance(o, datetime):
        return o.isoformat()

    raise TypeError(repr(o) + " is not JSON serializable")


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string"""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return json.dumps(value, separators=(',', ':'), default=json_datetime_serializer)

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)
