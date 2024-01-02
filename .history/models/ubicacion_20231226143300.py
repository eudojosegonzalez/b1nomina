'''
Modelo que define a la tabla Ubicacion del usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT, DATE, DateTime, Boolean, ForeignKey

# Definicion de la tabla de Contacto de usuarios
class Ubicacion(Base):
    '''
	id	bigint(20) AI PK
	user_id	bigint(20)
	region_id	bigint(20)
	comuna_id	bigint(20)
	direccion	text
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20) 
    '''
    __tablename__="Ubicacion"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"))
    email = Column(VARCHAR(250), nullable=True)
    fijo = Column(VARCHAR(20), nullable=True)
    movil = Column(VARCHAR(20), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 



