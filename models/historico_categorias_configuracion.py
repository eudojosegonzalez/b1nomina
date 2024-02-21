'''
Modelo que define a la tabla de Datos de las categorias de configuraciones básicas
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT, BOOLEAN,INTEGER

# Definicion de la tabla de Sociedades
class HistoricoCategoriasConfiguracion(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`categoria_id` bigint NOT NULL ,
	`sociedad_id` bigint NOT NULL,     
	`nombre` varchar(200) NOT NULL ,
	`activo` boolean NULL,     
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el parametro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
	`creator_user` bigint NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` datetime NOT NULL,
	`observaciones_update` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCategoriasConfiguracion"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    categoria_id = Column (BIGINT, nullable=False)        
    sociedad_id = Column (BIGINT, nullable=False)        
    nombre = Column(VARCHAR(200), nullable=False)
    activo = Column(INTEGER, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)    
