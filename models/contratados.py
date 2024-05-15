'''
Modelo que define a la tabla  Contratados
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,   ForeignKey, TEXT, INTEGER

# Definicion de la tabla de Contacto de usuarios
class Contratados(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint(20) NOT NULL ,    
	`user_id` bigint(20) NOT NULL,
	`estado` int NOT NULL default '0' comment '0 Inactivo 1 Activo',  
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `FK_Sociedad_Contratados` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE,
	CONSTRAINT `FK_Usuario_Contratados` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE    
    '''
    __tablename__="Contratados"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    estado = Column(INTEGER, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 



