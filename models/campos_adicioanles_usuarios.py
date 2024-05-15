'''
Modelo que define a la tabla de Datos de Campsu Adicionales Ususarios
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT

# Definicion de la tabla de Cargos
class CamposUser(Base):
    '''
 `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sociedad_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `camuser1` varchar(200) DEFAULT NULL,
  `camuser2` varchar(200) DEFAULT NULL,
  `camuser3` varchar(200) DEFAULT NULL,
  `camuser4` varchar(200) DEFAULT NULL,
  `camuser5` varchar(200) DEFAULT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `creator_user` bigint(20) NOT NULL,
  `updater_user` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Sociedad_CamposUser` (`sociedad_id`),
  KEY `FK_Usuario_CamposUser` (`user_id`),
  CONSTRAINT `FK_Sociedad_CamposUser` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_Usuario_CamposUser` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="CamposUser"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)   
    camuser1 = Column (VARCHAR(200), nullable=True)
    camuser2 = Column (VARCHAR(200), nullable=True)    
    camuser3 = Column (VARCHAR(200), nullable=True)
    camuser4 = Column (VARCHAR(200), nullable=True)    
    camuser5 = Column (VARCHAR(200), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
