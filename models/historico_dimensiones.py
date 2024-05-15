'''
Modelo que define a la tabla de Dimensiones del Sistema
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoDimensiones(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`dimensiones_id` bigint(20) NOT NULL ,  
	`sociedad_id` bigint(20) NOT NULL,
	`dimension` varchar(200) DEFAULT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,  
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoDimensiones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    dimensiones_id = Column(BIGINT,  nullable=False)
    sociedad_id = Column(BIGINT,   nullable=False)
    dimension = Column(VARCHAR(200),nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro= Column (DateTime, nullable=False) #datetime NOT NULL,
    observaciones =Column(TEXT,nullable=False)