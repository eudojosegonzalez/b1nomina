'''
Modelo que define a la tabla  Archivos del usuario
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,   ForeignKey, TEXT, INTEGER

# Definicion de la tabla de Contacto de usuarios
class CVUsuarios(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`user_id` bigint(20) NOT NULL,
	`estado` int NOT NULL comment '1 sin iniciar 2 completado 3 descartado',  
	`url` text NULL,
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `user_id` (`user_id`),
	CONSTRAINT `FK_Usuario_CVUsuarios` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="CVUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True)
    estado = Column(INTEGER, nullable=False)
    url = Column(TEXT, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 

    #metodp para convertir en diccionario
    def to_dict(self):
        result = {
            "id":self.id,
            "user_id": self.user_id,
            "estado":self.estado,
            "url":self.url,
            "created":self.created,
            "updated":self.updated,
            "creator_user":self.creator_user,
            "updater_user":self.updater_user
        }
        return (result)    

