'''
Modelo que define a la tabla de Datos de las Sedes de una Sociedad
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Sociedades
class Sede(Base):
    '''
    `id` bigint AUTO_INCREMENT not null,
    `sociedad_id` bigint NOT NULL ,
    `nombre` varchar(200) NOT NULL,
    `direccion` text NOT NULL,
    `region_id` bigint(20) NOT NULL,
    `comuna_id` bigint(20) NOT NULL,
    `ciudad` varchar(250) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Comunas_Sede` FOREIGN KEY (`comuna_id`) REFERENCES `Comunas` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Regiones_Sede` FOREIGN KEY (`region_id`) REFERENCES `Regiones` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedades_Sede` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="Sede"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    nombre = Column(VARCHAR(200), nullable=False)
    direccion = Column (TEXT, nullable=True)      
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    comuna_id = Column (BIGINT, ForeignKey("Comunas.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    ciudad = Column(VARCHAR(250), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
