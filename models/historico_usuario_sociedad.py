'''
Modelo que define a la tabla Historico de  Sociedad Usuarios
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  TEXT

# Definicion de una tabla
class HistoricoSociedadUsuario(Base):
    __tablename__="HistoricoSociedadUsuario"
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`sociedad_user_id` bigint(20) DEFAULT NULL, 
	`sociedad_id` bigint(20) NOT NULL,    
	`user_id` bigint(20) DEFAULT NULL,  
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	`fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
	`observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',    
	PRIMARY KEY (`id`)
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_user_id = Column(BIGINT, nullable=False)  
    sociedad_id = Column(BIGINT, nullable=False)  
    user_id = Column(BIGINT,   nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True)         
    

