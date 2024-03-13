'''
Modelo que define a la tabla UsuariosGruposEmpleado
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DATE, DateTime, TEXT

# Definicion de una tabla
class HistoricoUsuariosGruposEmpleado(Base):
    __tablename__="HistoricoUsuariosGruposEmpleado"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `usuarios_grupo_empleados_id` bigint(20) NOT NULL,
    `sociedad_id` bigint(20) NOT NULL,
    `grupo_empleados_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    `fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
    `observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',
    PRIMARY KEY (`id`)
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    usuarios_grupo_empleados_id = Column(BIGINT, nullable=False)  
    sociedad_id = Column(BIGINT, nullable=False)  
    grupo_empleados_id = Column(BIGINT, nullable=False)  
    user_id = Column(BIGINT,  nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True)     

