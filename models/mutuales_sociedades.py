'''
Modelo que define a la tabla de Datos Mutuales de la Sociedad
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime, ForeignKey, NUMERIC

# Definicion de la tabla de Sociedades
class MutualesSociedad(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint(20) NOT NULL,
	`mutual_id` bigint(20) NOT NULL,
	`porcentaje_id` numeric(13,4) NOT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `FK_Sociedad_MutualesSociedad` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) 
    ON UPDATE CASCADE on delete restrict,    
	CONSTRAINT `FK_Mutuales_MutualesSociedad` FOREIGN KEY (`mutual_id`) REFERENCES `Mutuales` (`id`) 
    ON UPDATE CASCADE on delete restrict
    '''
    __tablename__="MutualesSociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    mutual_id = Column (BIGINT, ForeignKey("Mutuales.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    porcentaje = Column (NUMERIC(13,4), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
