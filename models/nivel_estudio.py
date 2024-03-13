'''
Modelo que define a la tabla de Niveles de Estudio
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime

# Definicion de la tabla de Datos laborales
class NivelEstudio(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `descripcion` varchar(150) NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,    
    PRIMARY KEY (`id`)  
    '''
    __tablename__="NivelEstudio"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    descripcion=Column(VARCHAR(150), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,      