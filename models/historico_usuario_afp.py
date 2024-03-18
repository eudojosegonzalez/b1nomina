'''
Modelo que define a la tabla UsuariosAFP
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,   NUMERIC, TEXT

# Definicion de una tabla
class HistoricoUsuariosAFP(Base):
    __tablename__="HistoricoUsuariosAFP"
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`usuarios_afp_id` bigint(20) NOT NULL,
	`user_id` bigint(20) NOT NULL,
	`jubilado_afp` int NOT NULL comment '0 no jubilado 1 jubilado',
	`afp_id` bigint(20) NULL,
    `ahorro_afp2` numeric (13,4) NULL,
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
	`fecha_registro` datetime NOT NULL,
	`observaciones` text DEFAULT NULL,    
     PRIMARY KEY (`id`)
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    usuarios_afp_id= Column(BIGINT,  nullable=False) 
    user_id = Column(BIGINT,  nullable=False)    
    jubilado_afp= Column (BIGINT,nullable=False)
    afp_id = Column(BIGINT,  nullable=False)  
    ahorro_afp2 = Column(NUMERIC (13,4),nullable=True)  
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True)      

