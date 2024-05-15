'''
Modelo que define a la tabla de Historico de Datos de configuraciones de remuneraciones
Created 2024-05
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, TEXT, INTEGER, NUMERIC

# Definicion de la tabla de Sociedades
class HistoricoConfRemuneraciones(Base):
    '''
 	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`conf_remuneracion_id` bigint(20) NOT NULL,    
	`sociedad_id` bigint(20) NOT NULL,
	`sueldo_minimo` float (18,4) not null default '0',
	`gratificacion_minimo` float (6,2) not null default '0' comment 'Porcentaje de gratificacion mínimo',
	`tope_gratificacion` float (6,2) not null default '0' comment 'Porcentaje de gratificacion maximo',
	`dias_vacaciones` integer not null default '1',
	`horas_legales` integer not null default '8',
	`retencion_honorarios` float (6,2) not null default '0' comment 'Porcentaje de retención de honorarios',
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoConfRemuneraciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    conf_remuneracion_id=Column(INTEGER,nullable=False) 
    sociedad_id = Column (BIGINT, nullable=False)        
    sueldo_minimo= Column(NUMERIC(18,4), nullable=False)
    gratificacion_minimo= Column(NUMERIC(5,2), nullable=False)
    tope_gratificacion= Column(NUMERIC(5,2), nullable=False)
    dias_vacaciones= Column(INTEGER, nullable=False)
    horas_legales= Column(INTEGER, nullable=False)
    retencion_honorarios= Column(NUMERIC(5,2), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)     
    
