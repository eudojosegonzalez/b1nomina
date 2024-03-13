'''
Modelo que define a la tabla de Datos de los Tramos de Asigancion Familiar
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, NUMERIC

# Definicion de la tabla de Sociedades
class TramosAsignacionFamiliar(Base):
    '''
	`id` bigint auto_increment NOT NULL,
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
    __tablename__="TramosAsignacionFamiliar"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tramo = Column(VARCHAR(50), nullable=False)
    desde = Column(NUMERIC(18,4),nullable= False)
    hasta = Column(NUMERIC(18,4),nullable= False)   
    valor_carga = Column(NUMERIC(18,4),nullable= False)     
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
