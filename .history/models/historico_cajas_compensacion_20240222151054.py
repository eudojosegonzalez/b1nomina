'''
Modelo que define a la tabla de Datos de las Caja de Compensación
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT, INTEGER

# Definicion de la tabla de Sociedades
class CajasCompensacion(Base):
    '''
	`id` BIGINT AUTO_INCREMENT NOT NULL,
	`nombre` VARCHAR(200) NOT NULL,
	`codigo_externo` VARCHAR(50) NOT NULL,
	`cuenta_contable` VARCHAR(50) NOT NULL,
	`codigo_direccion_trabajo` VARCHAR(10) NULL,    
	`created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
	`updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
	`creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro',
	PRIMARY KEY (`id`) 
    '''
    __tablename__="CajasCompensacion"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(VARCHAR(200), nullable= False)
    codigo_externo= Column(VARCHAR(50), nullable= False)
    cuenta_contable = Column(VARCHAR(10), nullable= False)
    codigo_direccion_trabajo = Column(VARCHAR(50), nullable= False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
