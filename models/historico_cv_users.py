'''
Modelo que define a la tabla  Archivos del usuario
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,    TEXT, INTEGER

# Definicion de la tabla de Contacto de usuarios
class HistoricoCVUsuarios(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`cv_user_id` bigint(20) NOT NULL ,    
	`user_id` bigint(20) NOT NULL,
	`estado` integer NOT NULL comment '1 sin iniciar 2 completado 3 descartado',  
	`url` text NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCVUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    cv_user_id= Column(BIGINT, nullable=False)
    user_id = Column(BIGINT, nullable=False)
    estado = Column(INTEGER, nullable=False)
    url = Column(TEXT, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro=Column(DateTime, nullable=False)
    observaciones=Column(TEXT, nullable=False)
 



