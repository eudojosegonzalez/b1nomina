'''
Modelo que define a la tabla  Datos de Colacion de los Usuarios
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column, BIGINT, DateTime, ForeignKey, NUMERIC

# Definicion de la tabla de Datos de Colacion de usuarios
class ColacionUsuarios(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint(20) NOT NULL,
	`user_id` bigint(20) NOT NULL,  
	`movilizacion` numeric(18,4) NOT NULL,  
	`colacion` numeric(18,4) NOT NULL,    
	`familiar` numeric(18,4) NOT NULL,      
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `FK_Sociedad_ColacionUsuarios` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) 
    ON UPDATE CASCADE on delete restrict,
	CONSTRAINT `FK_Usuario_ColacionUsuarios` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) 
    ON UPDATE CASCADE on delete restrict  
    '''
    __tablename__="ColacionUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    movilizacion = Column(NUMERIC(18,4), nullable=False)
    colacion  = Column(NUMERIC(18,4), nullable=False)
    familiar  = Column(NUMERIC(18,4), nullable=False) 
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

