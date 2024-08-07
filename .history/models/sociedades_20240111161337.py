'''
Modelo que define a la tabla de Datos de los Bancos del Sistema
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla de Contacto de usuarios
class Sociedad(Base):
    '''
	`id` bigint auto_increment not null,
	`rut` varchar(100) not null,	
	`nombre` varchar(200) not null,	
	`direccion` text not null,
	`region_id`  bigint	not null , -- referencua a Regiones	 Listo
	`comuna_id`  bigint	not null , -- referencua a Comunas Listo
	`ciudad` varchar(250) not null,   
	`icono` varchar(250) null,    
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
    __tablename__="Sociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    rut = Column(VARCHAR(100), unique=True, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    direccion = Column (TEXT, nullable=True)      
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    comuna_id = Column (BIGINT, ForeignKey("Comunas.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    ciudad = Column(VARCHAR(250), nullable=False)
    icono = Column(VARCHAR(250), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
