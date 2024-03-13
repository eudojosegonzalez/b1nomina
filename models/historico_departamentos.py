'''
Modelo que define a la tabla de Datos de los datos Historicos de  los Departamentos de una Sociedad
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Sociedades
class HistoricoDepartamentos(Base):
    '''
    `id` bigint NOT NULL AUTO_INCREMENT,
    `departamento_id` bigint NOT NULL , 
    `sociedad_id` bigint NOT NULL , 
    `sede_id` bigint NOT NULL ,   
    `nombre` varchar(200) NOT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint NOT NULL COMMENT 'usuario que actualizó el parametro',
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,  
    PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoDepartamentos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    departamento_id = Column(BIGINT, nullable=False)    
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column (BIGINT, ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False) 
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)     
