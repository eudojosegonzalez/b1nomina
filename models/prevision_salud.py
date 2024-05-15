'''
Modelo que define a la tabla de PrevisionSalud
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN

# Definicion de la tabla de Contacto de usuarios
class PrevisionSalud(Base):
    '''
	id	bigint(20) AI PK
	codigo_externo	varchar(50)
	nombre	varchar(100)
	prevision_salud_cuenta	varchar(150)
	codigo_direccion_trabajo	varchar(10)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)
    '''
    __tablename__="PrevisionSalud"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    codigo_externo = Column(VARCHAR(50), unique=True, nullable=False)
    nombre = Column(VARCHAR(100), nullable=False)
    prevision_salud_cuenta = Column(VARCHAR(150), nullable=False)
    codigo_direccion_trabajo = Column(VARCHAR(10), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
