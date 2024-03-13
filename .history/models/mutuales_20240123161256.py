'''
Modelo que define a la tabla de Datos de los Mututales del Sistema
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN

# Definicion de la tabla de Contacto de usuarios
class Mututales(Base):
    '''
	id	bigint(20) AI PK
	nombre	varchar(250)
	codigo_externo	varchar(50)
	cuenta_contable	varchar(50)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)
    '''
    __tablename__="Mutuales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(VARCHAR(150), nullable=False)
    codigo_externo = Column(VARCHAR(50), nullable=False)
    cuenta_contable = Column(VARCHAR(50), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
