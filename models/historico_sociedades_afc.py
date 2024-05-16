'''
Modelo que define a la tabla Historico de Sociedades AFC
Created 2024-05
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  NUMERIC, TEXT

# Definicion de una tabla
class HistoricoSociedadAFC(Base):
    __tablename__="HistoricoSociedadAFC"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_afc_id` bigint(20) NOT NULL,  
    `sociedad_id` bigint(20) NOT NULL,
    `afc_empresa` numeric(5,2) NOT NULL,
    `afc_empleado` numeric(5,2) NOT NULL, 
    `afc_plazo_fijo` numeric(5,2) NOT NULL,  
    `afc_antiguedad` numeric(5,2) NOT NULL,  
    `tope_seguro_afc` numeric(5,2) NOT NULL,  
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,  
    PRIMARY KEY (`id`) 
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_afc_id = Column(BIGINT ,nullable=False)    
    sociedad_id = Column(BIGINT ,nullable=False)    
    afc_empresa = Column (NUMERIC(5,2) ,nullable=False)
    afc_empleado = Column (NUMERIC(5,2) ,nullable=False)
    afc_plazo_fijo = Column (NUMERIC(5,2) ,nullable=False) 
    afc_antiguedad = Column (NUMERIC(5,2), nullable=False)
    tope_seguro_afc= Column (NUMERIC(5,2) ,nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)     
    
    

