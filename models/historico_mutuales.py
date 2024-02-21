'''
Modelo que define a la tabla de Datos de los Historicos Mututales del Sistema
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN, TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoMututales(Base):
    '''
	id	bigint(20) AI PK
	mutuales_id	bigint(20)
	nombre	varchar(250)
	codigo_externo	varchar(50)
	cuenta_contable	varchar(50)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)
	fecha_registro	datetime
	observaciones	text
    '''
    __tablename__="HistoricoMutuales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    mutuales_id = Column(BIGINT,  nullable=False)    
    nombre = Column(VARCHAR(150), nullable=False)
    codigo_externo = Column(VARCHAR(50), nullable=False)
    cuenta_contable = Column(VARCHAR(50), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column(DateTime, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)      
