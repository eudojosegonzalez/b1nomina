'''
Modelo que define a la tabla de Historico de Datos Peronales del Usuario
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DATE, DateTime, Boolean, TEXT

# Definicion de una tabla
class HistoricoUsuario(Base):
    '''
    Estructura de la tabla
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) DEFAULT NULL,
    `rut` varchar(100) NOT NULL,
    `rut_provisorio` varchar(100) DEFAULT NULL,
    `nombres` varchar(100) NOT NULL,
    `apellido_paterno` varchar(100) NOT NULL,
    `apellido_materno` varchar(100) DEFAULT NULL,
    `fecha_nacimiento` date NOT NULL,
    `sexo_id` bigint(20) NOT NULL,
    `estado_civil_id` bigint(20) NOT NULL,
    `nacionalidad_id` bigint(20) NOT NULL,
    `username` varchar(250) NOT NULL,
    `password` varchar(250) NOT NULL,
    `activo` tinyint(1) NOT NULL COMMENT 'campo para activar o no al usuario 0 Inactivo 1 Activo',
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,    
    '''
    __tablename__="HistoricoUsuario"
    id = Column(BIGINT, primary_key=True, autoincrement=True)    
    user_id = Column(BIGINT, nullable=False)
    rut = Column(VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100), nullable=True) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100), nullable=False) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE, nullable=False) #DATE NOT NULL,
    sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
    activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True)
