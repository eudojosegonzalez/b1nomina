'''
Modelo que define a la tabla  Archivos del usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT,INTEGER, DATE, DateTime, Boolean, ForeignKey, TEXT, UniqueConstraint

# Definicion de la tabla de Contacto de usuarios
class PicUsuarios(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint NOT NULL,
    `url` text NOT NULL,  
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    unique (`user_id`),
    constraint `FK_Usuario_FilesUsers` foreign key (`user_id`) references `Usuario`(`id`)
    on update cascade on delete restrict
    '''
    __tablename__="FotosUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True)
    url = Column(TEXT, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 



