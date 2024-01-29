'''
Modelo que define a la tabla de Modulos del sistema
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,   BIGINT,  DateTime,   VARCHAR, INTEGER, ForeignKey


# Definicion de la tabla de Contacto de usuarios
class UsuarioModulo(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`user_id` bigint(20) NOT NULL,
	`modulo_id` bigint(20) NOT NULL,
	`estado` boolean NOT NULL ,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`),
    constraint `FK_Usuario_UsuarioModulo` foreign key (`user_id`) references `Usuario`(`id`) on update cascade on delete restrict,
    constraint `FK_Modulo_UsuarioModulo` foreign key (`modulo_id`) references `Modulo`(`id`) on update cascade on delete restrict
    '''
    __tablename__="UsuarioModulo"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    modulo_id = Column(BIGINT,  ForeignKey("Modulo.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    estado =Column (INTEGER, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 




