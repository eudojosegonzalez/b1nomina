'''
Modelo que define a la tabla  Archivos del usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,   ForeignKey, TEXT

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
 


    #metodp para convertir en diccionario
    def to_dict(self):
        result = {
            "id":self.id,
            "user_id": self.user_id,
            "url":self.url,
            "created":self.created,
            "updated":self.updated,
            "creator_user":self.creator_user,
            "updater_user":self.updater_user
        }
        return (result)    

