'''
Modelo que define a la tabla de Datos De Centralizaciones
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN, ForeignKey, INTEGER

# Definicion de la tabla de Contacto de usuarios
class Centralizaciones(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `usa_centros_costos` tinyint(1) NOT NULL,
    `cuenta_anticipo` varchar(50) DEFAULT NULL,
    `cuenta_bonos_feriado` varchar(50) DEFAULT NULL,
    `cuenta_honoraios` varchar(50) DEFAULT NULL,
    `cuenta_prestamos_solidarios` varchar(50) DEFAULT NULL,
    `prestamo_solidario_imponible` tinyint(1) NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,  
    PRIMARY KEY (`id`),
    KEY `FK_Sociedad_Centralizaciones` (`sociedad_id`),
    CONSTRAINT `FK_Sociedad_Centralizaciones` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="Centralizaciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
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
