'''
Modelo que define a la tabla de Modulos del sistema
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,   VARCHAR, INTEGER


# Definicion de la tabla de Contacto de usuarios
class viewGeneralUserModulo(Base):
    '''
    select 
    UsuarioModulo.*,
    Modulo.nombre as nombremodulo,
    Modulo.url as urlmodulo,
    Modulo.icono as iconomodulo,
    Modulo.estado as estadomodulo 
    from b1.UsuarioModulo 
    inner join b1.Modulo
    on (UsuarioModulo.modulo_id=Modulo.id)

	id	bigint(20)
	user_id	bigint(20)
	modulo_id	bigint(20)
	estado	tinyint(1)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)
	nombremodulo	varchar(250)
	urlmodulo	varchar(250)
	iconomodulo	varchar(250)
	estadomodulo	tinyint(1)
    '''
    __tablename__="viewGeneralUserModulo"
    id = Column(BIGINT, primary_key=True, nullable=False)
    user_id = Column(BIGINT, nullable=False)
    modulo_id = Column(BIGINT, nullable=False)    
    estado =Column (INTEGER, nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    nombremodulo =Column (VARCHAR(250), nullable=False)
    urlmodulo =Column (VARCHAR(250), nullable=True)
    iconomodulo = Column (VARCHAR(250), nullable=True)
    estadomodulo =Column (INTEGER, nullable=False)  





