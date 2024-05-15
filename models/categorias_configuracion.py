'''
Modelo que define a la tabla de Datos de las categorias de configuraciones básicas
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT, BOOLEAN,INTEGER

# Definicion de la tabla de Sociedades
class CategoriasConfiguracion(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint NOT NULL,    
	`nombre` varchar(200) NOT NULL ,
	`activo` boolean NULL,    
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el parametro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
	`creator_user` bigint NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint NOT NULL COMMENT 'usuario que actualizó el parametro',
	PRIMARY KEY (`id`),
    constraint `FK_Sociedad_CategoriasConfiguracion` foreign key (`sociedad_id`) references `Sociedad` (`id`) 
    '''
    __tablename__="CategoriasConfiguracion"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
    nombre = Column(VARCHAR(200), nullable=False)
    activo = Column(INTEGER, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
