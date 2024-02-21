# importamos la configuracion de la base de datos
from config.database import Base
# importamos los tipos a usar en la base de datos segun 
# la Manejador de la BD
from sqlalchemy import Column, Integer, String, Float

# Definicion de una tabla
class Movie(Base):
    __tablename__="movies"
    id = Column(Integer, primary_key=True)
    overview = Column (String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column (String)

