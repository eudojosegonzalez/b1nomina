'''
Modelo que define a la tabla de Historico de Datos de los Bancos del Sistema
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column, VARCHAR, BIGINT,DateTime, BOOLEAN, TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoBancos(Base):
    '''
	`id` bigint auto_increment not null,
	`banco_id` bigint not null,    
	`codigo` varchar(50) not null,    
	`nombre` varchar(150) not null,   
	`nomina` boolean not null comment '0 No genera Nomina 1 Genera Nomina',  
    `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',    
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,     
    primary key (`id`)
    '''
    __tablename__="HistoricoBancos"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    banco_id = Column(BIGINT,nullable=False)
    codigo = Column(VARCHAR(50), nullable=False)
    nombre = Column(VARCHAR(150), nullable=False)
    nomina = Column(BOOLEAN, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column(DateTime, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)  
