'''
Modelo que define a la tabla de Datos de los Bancos del Sistema
Created 2023-12
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN,ForeignKey,TEXT

# Definicion de la tabla de Sociedades
class Sociedad(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `rut` varchar(100) NOT NULL,
    `nombre` varchar(200) NOT NULL,
    `direccion` text NOT NULL,
    `region_id` bigint(20) NOT NULL,
    `comuna_id` bigint(20) NOT NULL,
    `ciudad` varchar(250) NOT NULL,
    `icono` varchar(250) DEFAULT NULL,
    `email` varchar(250) DEFAULT NULL,
    `responsable` varchar(150) DEFAULT NULL,
    `rut_responsable` varchar(100) DEFAULT NULL,
    `email_responsable` varchar(150) DEFAULT NULL,
    `telefono_responsable` varchar(20) DEFAULT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    KEY `FK_Regiones_Empresa` (`region_id`),
    KEY `FK_Comunas_Empresa` (`comuna_id`),
    CONSTRAINT `FK_Comunas_Empresa` FOREIGN KEY (`comuna_id`) REFERENCES `Comunas` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Regiones_Empresa` FOREIGN KEY (`region_id`) REFERENCES `Regiones` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="Sociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    rut = Column(VARCHAR(100), unique=True, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    direccion = Column (TEXT, nullable=True)      
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    comuna_id = Column (BIGINT, ForeignKey("Comunas.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    ciudad = Column(VARCHAR(250), nullable=False)
    icono = Column(VARCHAR(250), nullable=True)
    email = Column(VARCHAR(250), nullable=True)
    responsable = Column(VARCHAR(150), nullable=True)
    rut_responsable = Column(VARCHAR(100), nullable=True)  
    email_responsable = Column(VARCHAR(250), nullable=True)      
    telefono_responsable = Column(VARCHAR(20), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,

    # metodo que permite convertir el registro en un diccionario
    def to_dict(self):
        result={
            "id":self.id,
            "rut":self.rut,
            "nombre":self.nombre,
            "direccion":self.direccion,
            "region_id":self.region_id,
            "comuna_id":self.comuna_id,
            "ciudad":self.ciudad,
            "icono":self.icono,
            "email":self.email,
            "responsable":self.responsable,
            "rut_responsable":self.rut_responsable,
            "email_responsable":self.email_responsable,
            "telefono_responsable":self.telefono_responsable,
            "created":self.created,
            "updated":self.updated,
            "creator_user":self.creator_user, 
            "updater_user":self.updater_user
        }
        return (result)
    
    
    # metodo que permite convertir los datos basicos en un diccionario
    def basicos_to_dict(self):
        result={
            "id":self.id,
            "rut":self.rut,
            "nombre":self.nombre,
            "direccion":self.direccion,
            "region_id":self.region_id,
            "comuna_id":self.comuna_id,
            "ciudad":self.ciudad
        }
        return (result)
    

    # metodo que permite convertir los datos del representante en un diccionario
    def representante_to_dict(self):
        result={
            "id":self.id,
            "responsable":self.responsable,
            "rut_responsable":self.rut_responsable,
            "email_responsable":self.email_responsable,
            "telefono_responsable":self.telefono_responsable,
        }
        return (result)