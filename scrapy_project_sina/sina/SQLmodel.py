from sqlalchemy import Column, create_engine, Text, DateTime, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime)
    title = Column(Text())
    article = Column(LONGTEXT())
    category = Column(Text())
    pagetype = Column(Text())

