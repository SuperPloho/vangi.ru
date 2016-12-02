from sqlalchemy import create_engine
from sqlalchemy import MetaData, DateTime, String, Integer 
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, JSONB

import os

if os.path.exists("some.db"):
    os.remove("some.db")
engine = create_engine("sqlite:///some.db")

metadata = MetaData(engine)

source_table = Table('source',
               Column('ID_source', Integer, primary_key=True),
               Column('name', String(50)),
               Column('url', String(100)),
               Column('data', String(100))
               )

real_table = Table('real', metadata,
              # Column('param', source_table)
               Column('ID_source', Integer, primary_key=True),
               Column('name', String(50)),
               Column('address', String(100)),
               Column('data', String(100))
               )

forecastTable = Table('forecast', metadata,
               Column('ID_object', Integer, primary_key=True),
               Column('Priority', String(3)),
               Column('Update_DateTime', DateTime),
               Column('DateTime', DateTime),
               Column('Data', JSONB)
               # Column('Predicted_forecast', predicted_table),
               # Column('Real_forecast', real_table)
               )

object_table = Table('object', metadata,
                Column('ID_object', Integer, primary_key=True),
                Column('Name', String(50)),
                Column('GPS', String(50)),
                # Column('TimeZone', DateTime)
                )
 
metadata.create_all()