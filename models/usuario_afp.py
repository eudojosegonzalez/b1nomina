'''
Modelo que define a la tabla UsuariosAFP
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  ForeignKey,NUMERIC

# Definicion de una tabla
class UsuariosAFP(Base):
    __tablename__="UsuariosAFP"
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`user_id` bigint(20) NOT NULL,
	`jubilado_afp` int NOT NULL comment '0 no jubilado 1 jubilado',
	`afp_id` bigint(20) NULL,
    `ahorro_afp2` numeric (13,4) NULL,
	`created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
	`updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
	`creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
	`updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Usuario_UsuariosAFP` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_AFP_UsuariosAFP` FOREIGN KEY (`afp_id`) REFERENCES `AFP` (`id`) ON UPDATE CASCADE
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    jubilado_afp= Column (BIGINT,nullable=False)
    afp_id = Column(BIGINT,  ForeignKey("AFP.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)  
    ahorro_afp2 = Column(NUMERIC (13,4),nullable=True)  
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

