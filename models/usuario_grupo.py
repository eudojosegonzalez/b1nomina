'''
Modelo que define a la tabla UsuariosGruposEmpleado
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  ForeignKey

# Definicion de una tabla
class UsuariosGruposEmpleado(Base):
    __tablename__="UsuariosGruposEmpleado"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,  
    `grupo_empleados_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    primary key (id),
    CONSTRAINT `FK_GruposEmpleados_UsuariosGruposEmpleado` FOREIGN KEY (`grupo_empleados_id`) REFERENCES `GruposEmpleado` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedad_UsuariosGruposEmpleado` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Usuario_UsuariosGruposEmpleado` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE 
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)  
    grupo_empleados_id = Column(BIGINT, ForeignKey("GruposEmpleado.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)  
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

