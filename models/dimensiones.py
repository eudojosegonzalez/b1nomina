'''
Modelo que define a la tabla de Dimensiones del Sistema
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN, ForeignKey

# Definicion de la tabla de Contacto de usuarios
class Dimensiones(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `dimension` varchar(200) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,  
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_Sociedad_Dimensiones` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) 
    ON UPDATE CASCADE
    '''
    __tablename__="Dimensiones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    dimension = Column(VARCHAR(200),nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
