'''
Modelo que define a la tabla de Datos de las instituciones APV
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime

# Definicion de la tabla de Contacto de usuarios
class APVInstituciones(Base):
    '''
	`id` bigint auto_increment not null,
	`nombre` varchar(30) not NULL,
	`nombre_largo` varchar(250) not NULL,
	`cuenta_contable` varchar(100)  NULL,
	`codigo_externo` varchar(50) NULL,
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',      
	 PRIMARY KEY (`id`)
    '''
    __tablename__="APVInstituciones"
    id = Column(BIGINT, primary_key=True,  nullable=False)
    nombre = Column(VARCHAR(30), nullable=False)
    nombre_largo = Column(VARCHAR(250), nullable=False)
    cuenta_contable=Column(VARCHAR(100), nullable=True)
    codigo_externo=Column(VARCHAR(50), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
