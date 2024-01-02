from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT, DATE, DateTime, Boolean

# Definicion de una tabla
class Usuario(Base):
    __tablename__="usuario"
    id = Column(Integer, primary_key=True)
    rut = Column(String) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(String) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100)) #VARCHAR(100) NOT NULL,
    apellido  = Column (VARCHAR(100)) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE) #DATE NOT NULL,
    sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
    activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

