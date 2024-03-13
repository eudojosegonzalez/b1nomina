'''
Modelo que define a la tabla de fdatos Historicos de Niveles de Estudio
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime,TEXT

# Definicion de la tabla de Datos laborales
class HistoricoNivelEstudio(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `descripcion` varchar(150) NOT NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,  
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,   
    PRIMARY KEY (`id`)  
    '''
    __tablename__="HistoricoNivelEstudio"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nivel_estudio_id = Column(BIGINT, nullable=False)
    descripcion=Column(VARCHAR(150), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)          