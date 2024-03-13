'''
Modelo que define a la tabla de Datos de configuraciones básicas
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,TEXT, BOOLEAN,INTEGER, NUMERIC

# Definicion de la tabla de Sociedades
class Configuraciones(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `categoria_id` bigint(20) DEFAULT NULL,
    `nombre` varchar(150) NOT NULL,
    `valor` decimal(18,4) NOT NULL,
    `detalle` text DEFAULT NULL,
    `cuenta` varchar(20) DEFAULT NULL,
    `ocultar` bit(1) NOT NULL DEFAULT b'0',
    `tipo_validacion` varchar(30) DEFAULT NULL,
    `orden` int(11) DEFAULT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el registro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el registro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_CategoriasConfiguracion_Configuraciones` FOREIGN KEY (`categoria_id`) REFERENCES `CategoriasConfiguracion` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedad_Configuraciones` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE
    '''
    __tablename__="Configuraciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
    categoria_id = Column (BIGINT, ForeignKey("CategoriasConfiguracion.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)       
    nombre = Column(VARCHAR(200), nullable=False)
    valor = Column(NUMERIC(18,4), nullable=False)
    detalle= Column(TEXT, nullable=True)
    cuenta = Column(VARCHAR(20), nullable=True)
    ocultar= Column(INTEGER, nullable=True)
    tipo_validacion = Column(VARCHAR(30), nullable=True)
    orden= Column(INTEGER, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
