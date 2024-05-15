'''
Modelo que define a la tabla de Datos Mutuales de la Sociedad
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,  NUMERIC, TEXT

# Definicion de la tabla de Sociedades
class HistoricoMutualesSociedad(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`mutual_sociedad_id` bigint(20) NOT NULL,
	`sociedad_id` bigint(20) NOT NULL,
	`mutual_id` bigint(20) NOT NULL,
	`porcentaje_id` numeric(13,4) NOT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoMutualesSociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    mutual_sociedad_id= Column (BIGINT,nullable=False)
    sociedad_id = Column (BIGINT, nullable=False)
    mutual_id = Column (BIGINT, nullable=False)
    porcentaje = Column (NUMERIC(13,4), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)        
