'''
Modelo que define a la tabla de Historico de Datos de Contactos de Usuario
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT

# Definicion de la tabla de Historico de Contacto de usuarios
class HistoricoContacto(Base):
    '''
    Modelo que define a la tabla  Contacto del usuario
    Created 2023-12
        Estructura de la Tabla
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `user_id` bigint(20) DEFAULT NULL,
        `email` varchar(250) DEFAULT NULL,
        `fijo` varchar(20) DEFAULT NULL,
        `movil` varchar(20) DEFAULT NULL,
        `created` datetime NOT NULL,
        `updated` datetime NOT NULL,
        `creator_user` bigint(20) NOT NULL,
        `updater_user` bigint(20) NOT NULL,
        `fecha_registro` datetime NOT NULL,
        `observaciones` text DEFAULT NULL,    
    '''
    __tablename__="HistoricoContacto"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,nullable=False)
    email = Column(VARCHAR(250), nullable=True)
    fijo = Column(VARCHAR(20), nullable=True)
    movil = Column(VARCHAR(20), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)     
 



