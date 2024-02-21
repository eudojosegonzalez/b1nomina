'''
Modelo que define a la tabla Regiones
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,   VARCHAR, BIGINT, INTEGER


# Definicion de la tabla de Contacto de usuarios
class Regiones(Base):
    '''
	id	bigint(20) AI PK
	nombre	varchar(250)
	orden	int(11)
    '''
    __tablename__="Regiones"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    nombre = Column(VARCHAR(250), nullable=False)
    orden = Column (INTEGER, nullable=False )
   




