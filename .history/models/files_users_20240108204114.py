'''
Modelo que define a la tabla  Archivos del usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime,  ForeignKey, TEXT

# Definicion de la tabla de Contacto de usuarios
class ArchivosUsuarios(Base):
    '''
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `user_id` bigint NOT NULL,
        `nombre` varchar(250) NULL,  
        `url` text NOT NULL,    
        `created` datetime NOT NULL,
        `updated` datetime NOT NULL,
        `creator_user` bigint(20) NOT NULL,
        `updater_user` bigint(20) NOT NULL,
        PRIMARY KEY (`id`),
        constraint `FK_Usuario_ArchivosUsuarios` foreign key (`user_id`) references `Usuario`(`id`)
        on update cascade on delete restrict
    '''
    __tablename__="ArchivosUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"))
    nombre = Column(VARCHAR(250), nullable=False)
    url = Column(TEXT, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 



