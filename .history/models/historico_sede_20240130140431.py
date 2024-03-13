'''
Modelo que define a la tabla de Datos de las Sedes de una Ssociedad
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla de Sociedades
class HistoricoSede(Base):
    '''
    `id` bigint NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint NOT NULL ,
    `nombre` varchar(200) NOT NULL,
    `direccion` text NOT NULL,
    `region_id` bigint NOT NULL,
    `comuna_id` bigint NOT NULL,
    `ciudad` varchar(250) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint NOT NULL COMMENT 'usuario que actualizó el parametro',
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,  
    '''
    __tablename__="HistoricoSede"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    nombre = Column(VARCHAR(200), nullable=False)
    direccion = Column (TEXT, nullable=True)      
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    comuna_id = Column (BIGINT, ForeignKey("Comunas.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    ciudad = Column(VARCHAR(250), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)     

