'''
Modelo que define a la tabla de Datos Laborales del Empleado
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,INTEGER, DATE, TEXT, NUMERIC

# Definicion de la tabla de Datos laborales
class HistoricoDatosLaborales(Base):
    '''
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `datos_laborales_id` bigint(20) NOT NULL,
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
    `fecha_registro` datetime NOT NULL,
    `observaciones` text NOT NULL,
    PRIMARY KEY (`id`)  
    '''
    __tablename__="HistoricoDatosLaborales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    datos_laborales_id= Column(BIGINT, nullable=False)
    sociedad_id = Column (BIGINT, nullable=False)    
    sede_id = Column (BIGINT,nullable=False)    
    departamento_id = Column (BIGINT, nullable=False)    
    grupo_id = Column (BIGINT,  nullable=False)    
    cargo_id = Column (BIGINT, nullable=False)    
    user_id = Column (BIGINT, nullable=False)            
    tipo_contrato = Column(INTEGER, nullable=False)
    termino_contrato = Column(INTEGER, nullable=False)
    fecha_inicio =Column(DATE, nullable=False)    
    fecha_fin =Column(DATE, nullable=True)    
    periodo_salario = Column(INTEGER, nullable=False)    
    salario_base=Column(NUMERIC, nullable=False)
    modalidad = Column(INTEGER, nullable=False)   
    dias_descanso=Column(VARCHAR(50), nullable=False)
    nivel_estudio_id =  Column (BIGINT,nullable=False)    
    unidad_sueldo=Column(VARCHAR(5), nullable=False)    
    hora_ingreso =Column(DateTime, nullable=True)
    hora_egreso =Column(DateTime, nullable=True)  
    jefatura=Column(INTEGER, nullable=False)  
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
    fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
    observaciones = Column(TEXT, nullable= True) 

