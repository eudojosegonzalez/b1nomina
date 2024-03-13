'''
Modelo que define a la tabla de Niveles de Estudio
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT

# Definicion de la tabla de Datos laborales
class NivelEstudio(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `descripcion` varchar(150) NOT NULL,
    PRIMARY KEY (`id`)  
    '''
    __tablename__="NivelEstudio"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    descripcion=Column(VARCHAR(150), nullable=False)
