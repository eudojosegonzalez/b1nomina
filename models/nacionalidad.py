'''
Modelo que define a la tabla de Nacionalidad
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla de Hitoricos de Sedes
class Nacionalidad(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `Nacionalidad` varchar(150) NOT NULL,
    PRIMARY KEY (`id`)
    '''
    __tablename__="Nacionalidad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    Nacionalidad = Column(VARCHAR(50), nullable=False)

