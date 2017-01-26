from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

engine = create_engine('postgresql://postgres:1@localhost:5432/Weather')
Base = declarative_base()

Forecast_Geobject = Table('forecast_geobjects', Base.metadata,
                          Column('forecast_id', Integer, ForeignKey('forecasts.id')),
                          Column('geobject_id', Integer, ForeignKey('objects.id'))
                         )

Forecast_Source = Table('forecast_source', Base.metadata,
                        Column('forecast_id', Integer, ForeignKey('forecasts.id')),
                        Column('source_id', Integer, ForeignKey('sources.id'))
                       )

class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(100))
    data = Column(String(100))

    forecasts = relationship('Forecast',
                             secondary=Forecast_Source,
                             back_populates='sources')

class Real(Base):
    __tablename__ = 'real'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(100))
    data = Column(String(100))

class Forecast(Base):
    __tablename__ = 'forecasts'

    id = Column(Integer, primary_key=True)
    priority = Column(String(3), nullable=False)
    update_datetime = Column(DateTime)
    date_time = Column(DateTime)
    data = Column(JSON)
    objects = relationship('Geobject',
                           secondary=Forecast_Geobject,
                           back_populates='forecasts')
    sources = relationship('Source',
                           secondary=Forecast_Source,
                           back_populates='forecasts')

class Geobject(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    gps = Column(String(100))

    forecasts = relationship('Forecast',
                             secondary=Forecast_Geobject,
                             back_populates='objects')


if __name__ == "__main__":
    Base.metadata.create_all(engine)
