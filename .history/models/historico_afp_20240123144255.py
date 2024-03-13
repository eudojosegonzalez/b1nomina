'''
Modelo que define a la tabla de Datos de los AFP del Sistema
Created 20234-01
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, BOOLEAN, NUMERIC, TEXT

# Definicion de la tabla de Contacto de usuarios
class HistoricoAFP(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `codigo_previred` varchar(50) DEFAULT NULL,
    `nombre` varchar(100) DEFAULT NULL,
    `cotizacion` decimal(18,4) DEFAULT NULL,
    `cuenta_AFP` varchar(150) DEFAULT NULL,
    `sis` decimal(18,4) DEFAULT NULL,
    `cuenta_sis_cred` varchar(20) DEFAULT NULL,
    `cuenta_ahorro_AFP_cuenta2` varchar(150) DEFAULT NULL,
    `codigo_direccion_trabajo` varchar(10) DEFAULT NULL,
    `created` datetime NOT NULL COMMENT 'fecha en que fue creado el parametro',
    `updated` datetime NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
    `creator_user` bigint(20) NOT NULL COMMENT 'usuario que creó el parametro',
    `updater_user` bigint(20) NOT NULL COMMENT 'usuario que actualizó el parametro',
    `fecha_registro` DATETIME NOT NULL COMMENT 'fecha en que fue creado el registro historico',
    `observaciones` DATETIME NOT NULL COMMENT 'observaciones del historico',    
    '''
    __tablename__="HistoricoAFP"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    afp_id = Column(BIGINT,  autoincrement=True, nullable=False)
    codigo_previred = Column(VARCHAR(50), unique=True, nullable=False)
    nombre = Column(VARCHAR(100), nullable=False)
    cotizacion=Column(NUMERIC(18,4),nullable=True)
    cuenta_AFP=Column(VARCHAR(150), nullable=True)
    sis=Column(NUMERIC(18,4),nullable=True)
    cuenta_sis_cred=Column(VARCHAR(20), nullable=True)
    cuenta_ahorro_AFP_cuenta2=Column(VARCHAR(150), nullable=True)
    codigo_direccion_trabajo=Column(VARCHAR(150), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column(DateTime, nullable=False) #user BIGINT NOT NULL,   
    observaciones = Column(TEXT, nullable= True)      
