'''
Modelo que define a la tabla de Datos de los tramos de impuesto unico
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, NUMERIC, TEXT

# Definicion de la tabla de Sociedades
class HistoricoTramosAsignacionFamiliar(Base):
    '''
	`id` bigint auto_increment not NULL,
	`tramo_asignacion_familiar_id` bigint not NULL,    
	`tramo` nvarchar(5) not NULL,
	`desde` numeric(18,4) NULL,
	`hasta` numeric(18,4) NULL,
	`valor_carga` numeric(18,4) NULL,
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,    
	 PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoTramosAsignacionFamiliar"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tramo_asignacion_familiar_id = Column(BIGINT, nullable=False)
    tramo = Column(VARCHAR(50), nullable=False)
    desde = Column(NUMERIC(18,4),nullable= False)
    hasta = Column(NUMERIC(18,4),nullable= False)   
    valor_carga = Column(NUMERIC(18,4),nullable= False)     
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)       
