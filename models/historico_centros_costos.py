'''
Modelo que define a la tabla de Datos de Centros de Costo del Sistema
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT

# Definicion de la tabla de Centros de Costos
class HistoricoCentrosDeCostos(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`centros_costos_id` bigint(20) NOT NULL ,  
	`sociedad_id` bigint(20) NOT NULL,
	`codigo_sap` varchar(50) DEFAULT NULL,
	`centro_costo` varchar(200) DEFAULT NULL,
	`dimension_id` int(11) DEFAULT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,  
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCentrosDeCostos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    centros_costos_id = Column(BIGINT,   nullable=False)
    sociedad_id = Column(BIGINT,   nullable=False)
    codigo_sap = Column(VARCHAR(50), nullable=True)
    centro_costo = Column(VARCHAR(200), nullable=True)
    dimension_id = Column(BIGINT,  nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)  