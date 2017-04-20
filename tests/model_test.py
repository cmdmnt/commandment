import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commandment.models import SSLCertificate


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Session = sessionmaker(bind=engine)
    yield Session()


class TestModels:

    def test_query_sslcertificate(self, db_session: sqlalchemy.orm.Session):
        pass

