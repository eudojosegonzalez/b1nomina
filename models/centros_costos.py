'''
Modelo que define a la tabla de Datos de Centros de Costo del Sistema
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey

# Definicion de la tabla de Centros de Costos
class CentrosDeCostos(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint(20) NOT NULL,
	`codigo_sap` varchar(50) DEFAULT NULL,
	`centro_costo` varchar(200) DEFAULT NULL,
	`dimension_id` bigint(20) not null,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,  
	PRIMARY KEY (`id`),
	CONSTRAINT `FK_Sociedad_CentrosDeCostos` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) 
	ON UPDATE CASCADE,
	CONSTRAINT `FK_Dimension_CentrosDeCostos` FOREIGN KEY (`dimension_id`) REFERENCES `Dimensiones` (`id`) 
	ON UPDATE CASCADE
    '''
    __tablename__="CentrosDeCostos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    codigo_sap = Column(VARCHAR(50), nullable=True)
    centro_costo = Column(VARCHAR(200), nullable=True)
    dimension_id = Column(BIGINT,  ForeignKey("Dimensiones.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
