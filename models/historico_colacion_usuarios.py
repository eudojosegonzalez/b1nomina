'''
Modelo que define a la tabla  Datos Historicos de Colacion de los Usuarios
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column, BIGINT, DateTime,  NUMERIC, TEXT

# Definicion de la tabla de Historico de Colacion Usuarios
class HistoricoColacionUsuarios(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`colacion_usuario_id` bigint(20) NOT NULL ,    
	`sociedad_id` bigint(20) NOT NULL,
	`user_id` bigint(20) NOT NULL,  
	`movilizacion` numeric(18,4) NOT NULL,  
	`colacion` numeric(18,4) NOT NULL,    
	`familiar` numeric(18,4) NOT NULL,      
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoColacionUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    colacion_usuario_id = Column(BIGINT,   nullable=False)
    sociedad_id = Column(BIGINT,  nullable=False)
    user_id = Column(BIGINT,  nullable=False)
    movilizacion = Column(NUMERIC(18,4), nullable=False)
    colacion  = Column(NUMERIC(18,4), nullable=False)
    familiar  = Column(NUMERIC(18,4), nullable=False) 
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)       
    

