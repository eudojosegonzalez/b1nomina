'''
Modelo que define a la tabla de Datos Historico de las unidades de Pacto
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,TEXT, INTEGER

# Definicion de la tabla de Historico de unidades de Pacto
class HistoricoUnidadesPacto(Base):
    '''
	`id` bigint auto_increment not null,
    `unidades_id` bigint not null,
	`descripcion` varchar(150) not null,    
	`estado` boolean not null comment '0 Inactivo 1 Activo', 
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el parametro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',    
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,         
	primary key (`id`)
    '''
    __tablename__="HistoricoUnidadesPacto"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    unidades_id = Column (BIGINT, nullable=False)
    descripcion = Column(VARCHAR(150), nullable=False)
    estado= Column(INTEGER, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)    
