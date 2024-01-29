'''
Modelo que define a la tabla de Modulos del sistema
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,   VARCHAR, INTEGER


# Definicion de la tabla de Contacto de usuarios
class Modulo(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`nombre` varchar(250) NOT NULL,
	`url` varchar(250) NULL,  
	`icono` varchar(250) NULL,    
	`estado` boolean NOT NULL ,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
    '''
    __tablename__="Modulo"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    nombre =Column (VARCHAR(250), nullable=False)
    url =Column (VARCHAR(250), nullable=True)
    icono = Column (VARCHAR(250), nullable=True)
    estado =Column (INTEGER, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 




