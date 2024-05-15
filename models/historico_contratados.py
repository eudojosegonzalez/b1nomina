'''
Modelo que define a la tabla  HistoricoContratados
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,   ForeignKey, TEXT, INTEGER

# Definicion de la tabla de Contacto de usuarios
class HistoricoContratados(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`contratados_id` bigint(20) NOT NULL ,  
	`sociedad_id` bigint(20) NOT NULL ,       
	`user_id` bigint(20) NOT NULL,
	`estado` int NOT NULL default '0' comment '0 Inactivo 1 Activo',  
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el AFP',
	`fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro en el historico',    
	`observaciones` text not null,       
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoContratados"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT,  nullable=False)    
    contratados_id = Column(BIGINT, nullable=False)
    user_id = Column(BIGINT, nullable=False)
    estado = Column(INTEGER, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro=Column(DateTime, nullable=False)
    observaciones=Column(TEXT, nullable=False)    
    
 



