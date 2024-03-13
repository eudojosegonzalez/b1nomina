'''
Modelo que define a la tabla de Datos de Cargosusuarios
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Cargos
class CargosUsuarios(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) DEFAULT NULL,
    `sede_id` bigint(20) DEFAULT NULL,
    `user_id` bigint(20) DEFAULT NULL,
    `cargo_id` bigint(20) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `FK_Cargos_CargosUsuario` (`cargo_id`),
    KEY `FK_Sociedad_CargosUsuarios` (`sociedad_id`),
    KEY `FK_Usuario_CargosUsuario` (`user_id`),
    KEY `FK_Sede_CargosUsuario` (`sede_id`),
    CONSTRAINT `FK_Cargos_CargosUsuario` FOREIGN KEY (`cargo_id`) REFERENCES `Cargos` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sede_CargosUsuario` FOREIGN KEY (`sede_id`) REFERENCES `Sede` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedad_CargosUsuarios` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Usuario_CargosUsuario` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="CargosUsuario"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column (BIGINT, ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False) 
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    cargo_id = Column (BIGINT, ForeignKey("Cargo.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
