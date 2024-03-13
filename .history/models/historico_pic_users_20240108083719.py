'''
Modelo que define a la tabla  Archivos del usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT,INTEGER, DATE, DateTime, Boolean, ForeignKey, TEXT, UniqueConstraint

# Definicion de la tabla de Contacto de usuarios
class HistoricoPicUsuarios(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `pic_id` bigint(20) NOT NULL,  
    `user_id` bigint(20) NOT NULL,
    `url` text NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoFotosUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    pic_id = Column(BIGINT)
    user_id = Column(BIGINT)
    url = Column(TEXT, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)        
 



