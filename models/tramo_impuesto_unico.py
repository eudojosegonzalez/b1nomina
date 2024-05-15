'''
Modelo que define a la tabla de Datos de los tramos de impuesto unico
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, NUMERIC

# Definicion de la tabla de Sociedades
class TramosImpuestoUnico(Base):
    '''
    `id` int(11) NOT NULL,
    `tramo` varchar(50) NOT NULL,
    `desde` decimal(18,4) NOT NULL,
    `hasta` decimal(18,4) NOT NULL,
    `factor` decimal(18,4) DEFAULT NULL,
    `rebaja` decimal(18,4) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`)
    '''
    __tablename__="TramosImpuestoUnico"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tramo = Column(VARCHAR(50), nullable=False)
    desde = Column(NUMERIC(18,4),nullable= False)
    hasta = Column(NUMERIC(18,4),nullable= False)   
    factor = Column(NUMERIC(13,4),nullable= False)     
    rebaja = Column(NUMERIC(13,4),nullable= False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
