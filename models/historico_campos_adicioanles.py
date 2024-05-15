'''
Modelo que define a la tabla de Datos de Campsu Adicionales Ususarios
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, INTEGER, TEXT

# Definicion de la tabla de Cargos
class HistoricoCamposAdicionales(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `campos_adicionales_id` bigint(20) NOT NULL ,
    `sociedad_id` bigint(20) NOT NULL,
    `camuser1` varchar(200) DEFAULT NULL,
    `activo1`  bool DEFAULT NULL,
    `camuser2` varchar(200) DEFAULT NULL,
    `activo2`  bool DEFAULT NULL,
    `camuser3` varchar(200) DEFAULT NULL,
    `activo3`  bool DEFAULT NULL,
    `camuser4` varchar(200) DEFAULT NULL,
    `activo4`  bool DEFAULT NULL,
    `camuser5` varchar(200) DEFAULT NULL,
    `activo5`  bool DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    `fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
    `observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',  
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCamposAdicionales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    campos_adicionales_id = Column(BIGINT,  nullable=False)
    sociedad_id = Column (INTEGER,nullable=False) 
    camuser1 = Column (VARCHAR(200), nullable=True)
    activo1=Column(INTEGER,nullable=False)
    camuser2 = Column (VARCHAR(200), nullable=True)    
    activo2=Column(INTEGER,nullable=False)    
    camuser3 = Column (VARCHAR(200), nullable=True)
    activo3=Column(INTEGER,nullable=False)    
    camuser4 = Column (VARCHAR(200), nullable=True) 
    activo4=Column(INTEGER,nullable=False)       
    camuser5 = Column (VARCHAR(200), nullable=True)
    activo5=Column(INTEGER,nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)      
