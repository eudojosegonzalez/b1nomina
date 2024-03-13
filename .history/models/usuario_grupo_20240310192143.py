'''
Modelo que define a la tabla UsuariosGruposEmpleado
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DATE, DateTime, Boolean, ForeignKey

# Definicion de una tabla
class UsuariosGruposEmpleado(Base):
    __tablename__="UsuariosGruposEmpleado"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `grupo_empleados_id` bigint(20) NOT NULL,
    `sociedad_id` bigint(20) NOT NULL,
    `sede_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    `fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
    `observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',
    PRIMARY KEY (`id`),
    KEY `FK_Sociedad_UsuariosGruposEmpleado` (`sociedad_id`),
    KEY `FK_Sede_UsuariosGruposEmpleado` (`sede_id`),
    KEY `FK_Usuario_UsuariosGruposEmpleado` (`user_id`),
    CONSTRAINT `FK_Sede_UsuariosGruposEmpleado` FOREIGN KEY (`sede_id`) REFERENCES `Sede` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedad_UsuariosGruposEmpleado` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Usuario_UsuariosGruposEmpleado` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE  
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    grupo_id = Column(BIGINT, nullable=False)           
    sociedad_id = Column(BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)  
    sede_id = Column(BIGINT, ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False) 
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

