'''
Modelo que define a la tabla de Datos de Campsu Adicionales Ususarios
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT

# Definicion de la tabla de Cargos
class HistoricoCamposUser(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `campos_user_id` bigint(20) NOT NULL,
    `sociedad_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `camuser1` varchar(200) DEFAULT NULL,
    `camuser2` varchar(200) DEFAULT NULL,
    `camuser3` varchar(200) DEFAULT NULL,
    `camuser4` varchar(200) DEFAULT NULL,
    `camuser5` varchar(200) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCamposUser"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    campos_user_id = Column (BIGINT, nullable=False)
    sociedad_id = Column (BIGINT,nullable=False)    
    user_id = Column (BIGINT, nullable=False)   
    camuser1 = Column (VARCHAR(200), nullable=True)
    camuser2 = Column (VARCHAR(200), nullable=True)    
    camuser3 = Column (VARCHAR(200), nullable=True)
    camuser4 = Column (VARCHAR(200), nullable=True)    
    camuser5 = Column (VARCHAR(200), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column(DateTime, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)     
