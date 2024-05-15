'''
Modelo que define a la tabla  Datos Bancarios del Usuario
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column, VARCHAR, BIGINT, DateTime, ForeignKey, BOOLEAN, Boolean

# Definicion de la tabla de Datos Bancarios de usuarios
class BancariosUser(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) not NULL,
    `banco_id` bigint(20) NOT NULL,
    `numero_cuenta` varchar(100) NOT NULL,
    `en_uso` tinyint(1) NOT NULL,
    `terceros` tinyint(1) NOT NULL,
    `rut_tercero` varchar(100) DEFAULT NULL,
    `nombre_tercero` varchar(100) DEFAULT NULL,
    `email_tercero` varchar(250) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `FK_Usuario_BancariosUsuario` (`user_id`),
    KEY `FK_Bancos_BancariosUsuario` (`banco_id`),
    CONSTRAINT `FK_Bancos_BancariosUsuario` FOREIGN KEY (`banco_id`) REFERENCES `Bancos` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Usuario_BancariosUsuario` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="BancariosUser"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    banco_id = Column(BIGINT, ForeignKey("Bancos.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    numero_cuenta = Column(VARCHAR(100), nullable=False)
    en_uso = Column(Boolean, nullable=False)
    terceros = Column(Boolean, nullable=False)
    rut_tercero = Column(VARCHAR(100), nullable=True)
    nombre_tercero = Column(VARCHAR(100), nullable=True)    
    email_tercero = Column(VARCHAR(250), nullable=True)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

