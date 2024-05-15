'''
Modelo que define a la tabla de Datos de los Bancos del Sistema
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN

# Definicion de la tabla de Bancos
class Bancos(Base):
    '''
	`id` bigint auto_increment not null,
	`codigo` varchar(50) not null,    
	`nombre` varchar(150) not null,   
	`nomina` boolean not null comment '0 No genera Nomina 1 Genera Nomina',  
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',    
    primary key (`id`),
    unique (`codigo`)
    '''
    __tablename__="Bancos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    codigo = Column(VARCHAR(50), unique=True, nullable=False)
    nombre = Column(VARCHAR(150), nullable=False)
    nomina = Column(BOOLEAN, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
