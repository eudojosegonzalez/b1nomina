'''
Modelo que define a la tabla de Datos Historicos de los Cargos
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla de Sociedades
class HistoricoCargos(Base):
    '''
    `id` bigint NOT NULL AUTO_INCREMENT,
    `cargo_id` bigint NOT NULL,  
    `nombre` varchar(200) NOT NULL, 
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint NOT NULL,
    `updater_user` bigint NOT NULL,
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCargos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    cargo_id  = Column(BIGINT, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)     
