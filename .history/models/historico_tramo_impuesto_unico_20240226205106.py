'''
Modelo que define a la tabla de Datos de los tramos de impuesto unico
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, NUMERIC, TEXT

# Definicion de la tabla de Sociedades
class HistoricoTramosImpuestoUnico(Base):
    '''
	`id` bigint auto_increment NOT NULL,
	`tramo_impuesto_id` bigint NOT NULL,  
	`tramo` varchar(50) NOT NULL,
	`desde` decimal(18,4) NOT NULL,
	`hasta` decimal(18,4) NOT NULL,
	`factor` decimal(18,4) DEFAULT NULL,
	`rebaja` decimal(18,4) DEFAULT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoTramosImpuestoUnico"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tramo_impuesto_id = Column(BIGINT,  nullable=False)
    tramo = Column(VARCHAR(50), nullable=False)
    desde = Column(NUMERIC(18,4),nullable= False)
    hasta = Column(NUMERIC(18,4),nullable= False)   
    factor = Column(NUMERIC(13,4),nullable= False)     
    rebaja = Column(NUMERIC(13,4),nullable= False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)      
