'''
Modelo que define a la tabla de Estado Civil
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla de Hitoricos de Sedes
class EstadoCivil(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `descripcion` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)

    '''
    __tablename__="EstadoCivil"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(VARCHAR(50), nullable=False)

