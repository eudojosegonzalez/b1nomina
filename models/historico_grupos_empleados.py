'''
Modelo que define a la tabla de Datos de Grupos de Empleados
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT, INTEGER

# Definicion de la tabla de Historico de Grupos de Empleados
class HistoricoGruposEmpleado(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint NOT NULL ,    
	`grupo_empleados_id` bigint NOT NULL,  
	`es_honorario` boolean NOT NULL DEFAULT 0,
	`nombre` varchar(200) NOT NULL,
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
	`observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',  
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoGruposEmpleado"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    grupo_empleados_id = Column(BIGINT,  nullable=False)
    sociedad_id = Column (BIGINT, nullable=False)  
    es_honorario = Column(INTEGER, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)        
