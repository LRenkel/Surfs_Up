import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
conn = engine.connect()

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)