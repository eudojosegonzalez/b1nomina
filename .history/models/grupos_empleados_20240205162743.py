'''
Modelo que define a la tabla de Datos de los Bancos del Sistema
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT, INTEGER

# Definicion de la tabla de Sociedades
class GruposEmpleado(Base):
    '''
    `id` bigint NOT NULL AUTO_INCREMENT,
    `es_honorario` boolean NOT NULL DEFAULT 0,
    `nombre` varchar(200) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`)
    '''
    __tablename__="GruposEmpleado"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    es_honorario = Column(INTEGER, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
