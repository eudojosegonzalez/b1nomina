'''
Modelo que define a la tabla de UsuariosDepartamentos
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,   VARCHAR, INTEGER, ForeignKey


# Definicion de la tabla de Contacto de usuarios
class UsuariosDepartamentos(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `sede_id` bigint(20) NOT NULL,
    `departamento_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    KEY `FK_Sociedad_UsuariosDepartamentos` (`sociedad_id`),
    KEY `FK_Sede_UsuariosDepartamentos` (`sede_id`),
    KEY `FK_Departamento_UsuariosDepartamentos` (`departamento_id`),
    CONSTRAINT `FK_Departamento_UsuariosDepartamentos` FOREIGN KEY (`departamento_id`) REFERENCES `Departamentos` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sede_UsuariosDepartamentos` FOREIGN KEY (`sede_id`) REFERENCES `Sede` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedad_UsuariosDepartamentos` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE	
    '''
    __tablename__="UsuariosDepartamentos"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column(BIGINT,  ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    departamento_id = Column(BIGINT,  ForeignKey("Departamentos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 




