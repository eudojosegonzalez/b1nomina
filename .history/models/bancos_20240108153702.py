'''
Modelo que define a la tabla de Datos Bancarios del Usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT,INTEGER, DATE, DateTime, Boolean, ForeignKey

# Definicion de la tabla de Contacto de usuarios
class BancariosUser(Base):
    '''
    `id` BIGINT AUTO_INCREMENT NOT NULL,
    `user_id` BIGINT NULL, 
    `banco_id` BIGINT not NULL, 
	`numero_cuenta` varchar(100) not NULL,
	`en_uso` boolean not NULL,    
	`terceros` boolean not NULL,        
	`rut_tercero` varchar(100) NULL,     
	`nombre_tercero` varchar(100) NULL,         
	`email_tercero` varchar(250) NULL,             
	`created` datetime NOT NULL,    
	`updated`  datetime NOT NULL,   
    `creator_user` BIGINT NOT NULL,     
    `updater_user` BIGINT NOT NULL,       
    PRIMARY KEY (`id`),
    constraint `FK_Usuario_BancariosUsuario` foreign key (`user_id`) references `Usuario` (`id`) 
    on  update cascade on delete restrict,
    constraint `FK_Bancos_BancariosUsuario` foreign key (`banco_id`) references `Bancos` (`id`) 
    on  update cascade on delete restrict  
    '''
    __tablename__="BancariosUser"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"))
    banco_id = Column(BIGINT, ForeignKey)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 



