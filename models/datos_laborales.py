'''
Modelo que define a la tabla de Datos Laborales del Empleado
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,INTEGER, DATE, NUMERIC

# Definicion de la tabla de Datos laborales
class DatosLaborales(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `sociedad_id` bigint(20) NOT NULL,
    `sede_id` bigint(20) NOT NULL,
    `departamento_id` bigint(20) NOT NULL,
    `grupo_id` bigint(20) NOT NULL,
    `cargo_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `tipo_contrato` int(11) NOT NULL,
    `termino_contrato` int(11) NOT NULL,
    `fecha_inicio` date NOT NULL,
    `fecha_fin` date DEFAULT NULL,
    `periodo_salario` int(11) NOT NULL COMMENT 'Representa cual es el periodo en dias de calculo de nomina 1 Quincenal 2 Mensual',
    `salario_base` decimal(18,4) NOT NULL,
    `modalidad` int(11) NOT NULL COMMENT 'Representa 0 Presencial 1 Teletrabajo',
    `dias_descanso` varchar(50) NOT NULL COMMENT 'Es un texto de la siguiente manera 1,2,3,4,5,6,7',
    `nivel_estudio_id` bigint(20) NOT NULL,
    `unidad_sueldo` varchar(5) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `FK_Sociedad_DatosLaborales` (`sociedad_id`),
    KEY `FK_Sede_DatosLaborales` (`sede_id`),
    KEY `FK_Departamento_DatosLaborales` (`departamento_id`),
    KEY `FK_Grupo_DatosLaborales` (`grupo_id`),
    KEY `FK_Cargo_DatosLaborales` (`cargo_id`),
    KEY `FK_Usuario_DatosLaborales` (`user_id`),
    CONSTRAINT `FK_Cargo_DatosLaborales` FOREIGN KEY (`cargo_id`) REFERENCES `Cargos` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Departamento_DatosLaborales` FOREIGN KEY (`departamento_id`) REFERENCES `Departamentos` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Grupo_DatosLaborales` FOREIGN KEY (`grupo_id`) REFERENCES `GruposEmpleado` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sede_DatosLaborales` FOREIGN KEY (`sede_id`) REFERENCES `Sede` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Sociedad_DatosLaborales` FOREIGN KEY (`sociedad_id`) REFERENCES `Sociedad` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Usuario_DatosLaborales` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_NivelEstudio_DatosLaborales` FOREIGN KEY (`nivel_estudio_id`) REFERENCES `NivelEstudio` (`id`) ON UPDATE CASCADE    
    '''
    __tablename__="DatosLaborales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column (BIGINT, ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    departamento_id = Column (BIGINT, ForeignKey("Departamentos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    grupo_id = Column (BIGINT, ForeignKey("GruposEmpleado.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    cargo_id = Column (BIGINT, ForeignKey("Cargos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)            
    tipo_contrato = Column(INTEGER, nullable=False)
    termino_contrato = Column(INTEGER, nullable=False)
    fecha_inicio =Column(DATE, nullable=False)    
    fecha_fin =Column(DATE, nullable=True)    
    periodo_salario = Column(INTEGER, nullable=False)    
    salario_base=Column(NUMERIC, nullable=False)
    modalidad = Column(INTEGER, nullable=False)   
    dias_descanso=Column(VARCHAR(50), nullable=False)
    nivel_estudio_id =  Column (BIGINT, ForeignKey("NivelEstudio.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    unidad_sueldo=Column(VARCHAR(5), nullable=False)
    hora_ingreso =Column(DateTime, nullable=True)
    hora_egreso =Column(DateTime, nullable=True)
    jefatura=Column(INTEGER, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
