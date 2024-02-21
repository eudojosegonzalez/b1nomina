'''
Modelo que define a la tabla Ubicacion del usuario
Created 2023-12
    Estructura de la Tabla
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) DEFAULT NULL,
    `region_id` bigint(20) NOT NULL,
    `comuna_id` bigint(20) NOT NULL,
    `direccion` text NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    `fecha_registro` datetime NOT NULL,
    `observaciones` text DEFAULT NULL,        
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT, DATE, DateTime, Boolean, TEXT, ForeignKey


# Definicion de la tabla de Contacto de usuarios
class HistoricoUbicacion(Base):
    __tablename__="HistoricoUbicacion"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  nullable=False)
    region_id = Column (BIGINT, nullable=False)
    comuna_id = Column (BIGINT, nullable=False)
    direccion = Column (TEXT, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True)


