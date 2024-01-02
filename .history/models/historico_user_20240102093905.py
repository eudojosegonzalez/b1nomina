'''
Modelo que define a la tabla de Historico de Datos Peronales del Usuario
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT, DATE, DateTime, Boolean

# Definicion de una tabla
class HistoricoUsuario(Base):
    __tablename__="HistoricoUsuario"
    id = Column(BIGINT, nullable=False)
    rut = Column(VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100), nullable=True) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100), nullable=False) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE, nullable=False) #DATE NOT NULL,
    sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
    activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column(BIGINT, nullable=False)  #datetime NOT NULL,  

