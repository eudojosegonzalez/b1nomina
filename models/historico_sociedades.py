'''
Modelo que define a la tabla de Datos de los Bancos del Sistema
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla Historico de Socidades
class HistoricoSociedad(Base):
    '''
	`id` bigint auto_increment not null,
	`rut` varchar(100) not null,	
	`nombre` varchar(200) not null,	
	`direccion` text not null,
	`region_id`  bigint	not null , -- referencua a Regiones	 Listo
	`comuna_id`  bigint	not null , -- referencua a Comunas Listo
	`ciudad` varchar(250) not null,   
	`icono` varchar(250) null, 
    `email` varchar(250) DEFAULT NULL,
    `responsable` varchar(150) DEFAULT NULL,
    `rut_responsable` varchar(100) DEFAULT NULL,
    `email_responsable` varchar(150) DEFAULT NULL,
    `telefono_responsable` varchar(20) DEFAULT NULL,   
	`created` datetime NOT NULL comment 'fecha en que fue creado el registro',    
	`updated`  datetime NOT NULL  comment 'fecha en que fue actualizado el registro',   
    `creator_user` BIGINT NOT NULL  comment 'usuario que creó el parametro',     
    `updater_user` BIGINT NOT NULL  comment 'usuario que actualizó el parametro',      
    primary key (`id`),
    constraint `FK_Regiones_Empresa` foreign key (`region_id`) references `Regiones` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Comunas_Empresa` foreign key (`comuna_id`) references `Comunas` (`id`) 
    on  update cascade on delete restrict
    '''
    __tablename__="HistoricoSociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT, nullable=False)
    rut = Column(VARCHAR(100), nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    direccion = Column (TEXT, nullable=True)      
    region_id = Column (BIGINT, nullable=False)
    comuna_id = Column (BIGINT, nullable=False)
    ciudad = Column(VARCHAR(250), nullable=False)
    icono = Column(VARCHAR(250), nullable=True)
    email = Column(VARCHAR(250), nullable=True)
    responsable = Column(VARCHAR(150), nullable=True)
    rut_responsable = Column(VARCHAR(100), nullable=True)  
    email_responsable = Column(VARCHAR(250), nullable=True)      
    telefono_responsable = Column(VARCHAR(20), nullable=True)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)    
