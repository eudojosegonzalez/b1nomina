'''
Modelo que define a la tabla Comunas
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, ForeignKey


# Definicion de la tabla de Contacto de usuarios
class Comunas(Base):
    '''
	id	bigint(20) AI PK
	nombre	varchar(150)
	region_id	bigint(20)
    '''
    __tablename__="Comunas"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    nombre = Column (VARCHAR(250), nullable=False)
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False )