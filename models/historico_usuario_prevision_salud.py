'''
Modelo que define a la tabla Historico Usuarios Prevision Salud
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  NUMERIC, INTEGER, TEXT

# Definicion de una tabla
class HistoricoUsuariosPrevisionSalud(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `usuario_prevision_salud_id` bigint  not null,    
    `prevision_salud_id` bigint  not null,
    `user_id` bigint  not null,
    `pactado` numeric(18,4)  not null default 0,  
    `tipo_contrato` integer not null ,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el UsuariosPrevisionSalud',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el UsuariosPrevisionSalud',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el UsuariosPrevisionSalud',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el UsuariosPrevisionSalud',
    `fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
    `observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',    
    '''
    __tablename__="HistoricoUsuariosPrevisionSalud"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    usuario_prevision_salud_id = Column(BIGINT, nullable=False)
    prevision_salud_id = Column(BIGINT, nullable=False)
    user_id = Column(BIGINT,  nullable=False)    
    pactado= Column(NUMERIC (18,4),nullable=False)   
    tipo_contrato= Column(INTEGER,nullable=False)   
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True)      
    
    

