'''
Modelo que define a la tabla Usuario
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DATE, DateTime, Boolean

# Definicion de una tabla
class Usuario(Base):
    __tablename__="Usuario"
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `rut` varchar(100) NOT NULL,
    `rut_provisorio` varchar(100) DEFAULT NULL,
    `nombres` varchar(100) NOT NULL,
    `apellido_paterno` varchar(100) NOT NULL,
    `apellido_materno` varchar(100) DEFAULT NULL,
    `fecha_nacimiento` date NOT NULL,
    `sexo_id` bigint(20) NOT NULL,
    `estado_civil_id` bigint(20) NOT NULL,
    `nacionalidad_id` bigint(20) NOT NULL,
    `username` varchar(250) NOT NULL,
    `password` varchar(250) NOT NULL,
    `activo` tinyint(1) NOT NULL COMMENT 'campo para activar o no al usuario 0 Inactivo 1 Activo',
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `rut` (`rut`),
    UNIQUE KEY `username` (`username`),
    KEY `FK_Nacionalidad_Usuario` (`nacionalidad_id`),
    KEY `FK_Sexo_Usuario` (`sexo_id`),
    KEY `FK_EstadoCivil_Usuario` (`estado_civil_id`),
    CONSTRAINT `FK_EstadoCivil_Usuario` FOREIGN KEY (`estado_civil_id`) REFERENCES `EstadoCivil` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Nacionalidad_Usuario` FOREIGN KEY (`nacionalidad_id`) REFERENCES `Nacionalidad` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sexo_Usuario` FOREIGN KEY (`sexo_id`) REFERENCES `Sexo` (`id`) ON UPDATE CASCADE    
    '''
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    rut = Column(VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100), nullable=True) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100), nullable=False) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE, nullable=False) #DATE NOT NULL,
    sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
    activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  


    #interface que permite extraer en forma de diccionario los datos personales
    def to_dict_personal_data(self):
        result = {
            "user_id": self.id,
            "rut": self.rut  ,
            "nombres": self.nombres  ,
            "apellido_paterno": self.apellido_paterno  ,
            "fecha_nacimiento": self.fecha_nacimiento  ,
            "sexo_id": self.sexo_id  ,
            "estado_civil_id": self.estado_civil_id  ,
            "nacionalidad_id": self.nacionalidad_id  
        }
        return (result)     