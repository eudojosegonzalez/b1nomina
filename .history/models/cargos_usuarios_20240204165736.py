'''
Modelo que define a la tabla de Datos de Cargos
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Cargos
class Cargos(Base):
    '''
    `id` bigint NOT NULL AUTO_INCREMENT,
    `nombre` varchar(200) NOT NULL, 
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint NOT NULL,
    `updater_user` bigint NOT NULL,
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,
    PRIMARY KEY (`id`)
    '''
    __tablename__="Cargos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
