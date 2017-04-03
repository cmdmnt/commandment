from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Boolean, DateTime, Enum

db = SQLAlchemy()


class SCEPConfig(db.Model):
    __tablename__ = 'scep_config'

    id = Column(Integer, primary_key=True)
    challenge = Column(String, nullable=False)
