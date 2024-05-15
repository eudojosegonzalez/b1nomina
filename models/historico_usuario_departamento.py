'''
Modelo que define a la tabla de HistoricoUsuariosDepartamentos
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  TEXT


# Definicion de la tabla de Contacto de usuarios
class HistoricoUsuariosDepartamentos(Base):
    '''
  	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`usuarios_departamentos_id` bigint(20) NOT NULL,
	`sociedad_id` bigint(20) NOT NULL,
	`sede_id` bigint(20) NOT NULL,
	`departamento_id` bigint(20) NOT NULL,
	`user_id` bigint(20) NOT NULL,
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
	`observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoUsuariosDepartamentos"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    usuarios_departamentos_id  = Column(BIGINT,   nullable=False) 
    sociedad_id = Column(BIGINT,   nullable=False)    
    sede_id = Column(BIGINT,   nullable=False)    
    departamento_id = Column(BIGINT,   nullable=False)    
    user_id = Column(BIGINT,   nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True) 



