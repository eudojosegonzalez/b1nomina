'''
Modelo que define a la tabla de Historico de  Datos De Centralizaciones
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime,  INTEGER, TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoCentralizaciones(Base):
    '''
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`centralizaciones_id` BIGINT(20) NOT NULL,    
	`sociedad_id` BIGINT(20) NOT NULL,
	`usa_centros_costos` TINYINT(1) NOT NULL,
	`cuenta_anticipo` VARCHAR(50) DEFAULT NULL,
	`cuenta_bonos_feriado` VARCHAR(50) DEFAULT NULL,
	`cuenta_honoraios` VARCHAR(50) DEFAULT NULL,
	`cuenta_prestamos_solidarios` VARCHAR(50) DEFAULT NULL,
	`prestamo_solidario_imponible` TINYINT(1) NOT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,    
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoCentralizaciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    centralizaciones_id = Column(BIGINT,  nullable=False)
    sociedad_id = Column(BIGINT,  nullable=False)
    usa_centros_costos= Column(INTEGER,   nullable=False)
    cuenta_anticipo= Column(VARCHAR(50), nullable=True)
    cuenta_bonos_feriado= Column(VARCHAR(50), nullable=True)
    cuenta_honorarios= Column(VARCHAR(50), nullable=True)
    cuenta_prestamos_solidarios= Column(VARCHAR(50), nullable=True)
    prestamo_solidario_imponible= Column(INTEGER,   nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro= Column(DateTime, nullable=False)
    observaciones= Column(TEXT, nullable=False)
