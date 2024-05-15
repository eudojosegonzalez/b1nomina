'''
Modelo que define a la tabla de Datos de Cargos
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Cargos
class Cargos(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `nombre` varchar(150) NOT NULL,
    `nivel_cargo` varchar(10) DEFAULT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    KEY `FK_Sociedad_Cargos` (`sociedad_id`),
    CONSTRAINT `FK_Sociedad_Cargos` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="Cargos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    nivel_cargo = Column(VARCHAR(10), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
