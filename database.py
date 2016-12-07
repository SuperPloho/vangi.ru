from sqlalchemy import create_engine
engine = create_engine('postgresql:///some.db')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
#from sqlalchemy import Sequence
from sqlalchemy.dialects.postgresql import JSON

class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    url = Column(String(100))
    data = Column(String(100))

class Real(Base):
    __tablename__ = 'real'

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    address = Column(String(100))
    data = Column(String(100))

class Forecast(Base):
    __tablename__ = 'forecasts'

    id = Column(Integer, primary_key = True)
    priority = Column(String(3))
    update_DateTime = Column(DateTime)
    dateTime = Column(DateTime)
    data = Column(JSON)
    objects = relationship('Geobject', 
                        secondary = Forecast_Geobject,
                        backref = 'Forecast')
    sources = relationship('Source', 
                        secondary = Forecast_Source,
                        backref = 'Forecast')

class Geobject(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    gps = Column(String(100))

Forecast_Geobject = Table('forecast_geobjects', Base.metadata,
Column('forecast_id', Integer, ForeignKey('forecasts.id')),
Column('geobject_id', Integer, ForeignKey('objects.id'))
)

Forecast_Source = Table('forecast_source', Base.metadata,
Column('forecast_id', Integer, ForeignKey('forecasts.id')),
Column('source_id', Integer, ForeignKey('sources.id'))
)
