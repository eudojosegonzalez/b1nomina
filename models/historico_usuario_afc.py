'''
Modelo que define a la tabla UsuariosAFC
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,  ForeignKey,TEXT

# Definicion de una tabla
class HistoricoUsuariosAFC(Base):
    __tablename__="HistoricoUsuariosAFC"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `usuarios_afc_id` bigint(20) ,
    `user_id` bigint(20) NOT NULL,
    `estado` int NOT NULL comment '0 no afiliado 1 afiliado',
    `antiguedad` int NOT NULL comment '0 no maxima 1 maxima',
    `vejez` int NOT NULL comment '0 no no 1 si',
    `invalidez` int NOT NULL comment '0 no no 1 si',  
    `exinp` int NOT NULL comment '0 no no 1 si',      
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Usuario_UsuariosAFC` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    usuarios_afc_id = Column(BIGINT,  nullable=False)    
    user_id = Column(BIGINT,  nullable=False)    
    estado = Column(BIGINT, nullable=False)
    antiguedad= Column(BIGINT, nullable=False)
    vejez= Column(BIGINT, nullable=False)
    invalidez= Column(BIGINT, nullable=False)
    exinp= Column(BIGINT, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  
    fecha_registro = Column(DateTime, nullable=False)  #datetime NOT NULL,  
    observaciones = Column(TEXT, nullable= True)  
