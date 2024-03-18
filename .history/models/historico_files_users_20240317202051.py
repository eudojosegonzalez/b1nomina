'''
Modelo que define a la tabla  de Historico de Archivos del usuario
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT,INTEGER, DATE, DateTime, Boolean, ForeignKey, TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoArchivosUsuarios(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) NOT NULL,
    `nombre` varchar(250) DEFAULT NULL,
    `url` text NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    `fecha_registro` datetime NOT NULL,  
    `observaciones` text NULL,  
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoArchivosUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    file_id = Column(BIGINT, nullable=False)
    user_id = Column(BIGINT, nullable=False)
    nombre = Column(VARCHAR(250), nullable=False)
    url = Column(TEXT, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column(DateTime, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)     
 



