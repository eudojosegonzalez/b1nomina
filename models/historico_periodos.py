'''
Modelo que define a la tabla de Historico Periodos
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT, INTEGER, NUMERIC

# Definicion de la tabla de Sociedades
class HistoricoPeriodos(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`anio` integer NOT NULL ,
	`mes` integer NOT NULL ,  
	`nombre` varchar(200) NOT NULL ,
	`observaciones` text NULL ,  
	`activo` boolean NULL,    
	`utm` numeric(18,4) default NULL,  
	`uf` numeric(18,4) default NULL,    
	`factor_actualizacion` numeric(18,4) default NULL,    
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el parametro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
	`creator_user` bigint NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` datetime NOT NULL,
	`observaciones_update` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoPeriodos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    periodos_id= Column(BIGINT,  nullable=False)
    anio = Column(INTEGER, nullable=False)
    mes = Column(INTEGER, nullable=False)    
    nombre = Column(VARCHAR(200), nullable=False)
    observaciones = Column(TEXT, nullable=True)
    activo=Column(INTEGER, nullable=False)    
    utm=Column(NUMERIC(18,4), nullable=False)    
    uf=Column(NUMERIC(18,4), nullable=False)     
    factor_actualizacion=Column(NUMERIC(18,4), nullable=False) 
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones_update = Column(TEXT, nullable= True)        
