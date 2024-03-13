'''
Modelo que define a la tabla de Datos de las Sedes de una Sociedad
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Sociedades
class HistoricoTiposPrestamos(Base):
    '''
	`id` bigint auto_increment NOT NULL,
	`prestamo_id` bigint NOT NULL,    
	`sociedad_id` bigint  NOT NULL,     
	`descripcion` varchar(150)  NOT NULL,
	`cuenta` varchar(30)  NULL,
	`CCAF` boolean DEFAULT 0 NOT NULL,
	`caja_compensacion_id` bigint NULL,-- esta columna se relaciona con las cajas de compensacion si y solo si la cuenta es CCAF
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` bigint(20) NOT NULL,
	`observaciones` text DEFAULT NULL,    
	PRIMARY KEY (`id`)
    '''
    __tablename__="HistoricoTiposPrestamos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    descripcion = Column(VARCHAR(150), nullable=False)
    cuenta = Column(VARCHAR(30), nullable=True)     
    CCAF = Column (int, nullable=False)    
    caja_compensacion_id = Column (BIGINT, nullable=True)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)    
