'''
Modelo que define a la tabla  Historico de Datos Bancarios del Usuario
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoBancariosUser(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `bancario_id` bigint(20) NOT NULL,  
    `user_id` bigint(20) DEFAULT NULL,
    `banco_id` bigint(20) NOT NULL,
    `numero_cuenta` varchar(100) NOT NULL,
    `en_uso` tinyint(1) NOT NULL,
    `terceros` tinyint(1) NOT NULL,
    `rut_tercero` varchar(100) DEFAULT NULL,
    `nombre_tercero` varchar(100) DEFAULT NULL,
    `email_tercero` varchar(250) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    `fecha_registro` datetime NOT NULL,  
    `observaciones` text NULL,    
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoBancariosUser"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    bancario_id  = Column(BIGINT, nullable=False)
    user_id = Column(BIGINT, nullable=False)
    banco_id = Column(BIGINT,  nullable=False)
    numero_cuenta = Column(VARCHAR(100), nullable=False)
    en_uso = Column(BOOLEAN, nullable=False)
    terceros = Column(BOOLEAN, nullable=False)
    rut_tercero = Column(VARCHAR(100), nullable=True)
    nombre_tercero = Column(VARCHAR(100), nullable=True)    
    email_tercero = Column(VARCHAR(250), nullable=True)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column(DateTime, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)       
 



