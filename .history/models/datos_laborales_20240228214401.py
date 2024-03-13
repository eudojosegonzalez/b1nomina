'''
Modelo que define a la tabla de Datos Laborales del Empleado
Created 2024-02
'''
from config.database import Base
from sqlalchemy import Column,  VARCHAR, BIGINT, DateTime, ForeignKey,INTEGER, DATE

# Definicion de la tabla de Datos laborales
class DatosLaborales(Base):
    '''
	`id` bigint NOT NULL AUTO_INCREMENT,
	`sociedad_id` bigint not null,
	`sede_id` bigint not null,
	`departamento_id` bigint not null,    
	`grupo_id` bigint not null,
	`cargo_id` bigint not null,    
	`user_id` bigint NOT NULL,
	`tipo_contrato` int NOT NULL,  
	`termino_contrato` int NOT NULL,
	`fecha_inicio` date NOT NULL,
	`fecha_fin` date NULL, 
	`periodo_salario` int not null comment 'Representa cual es el periodo en dias de calculo de nomina 1 Quincenal 2 Mensual',  
	`salario_base` numeric(18,4) not null, 
	`modalidad` int not null comment 'Representa 0 Presencial 1 Teletrabajo',   
	`dias_descanso` varchar(50) not null comment 'Es un texto de la siguiente manera 1,2,3,4,5,6,7',    
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,    
	primary key(`id`),
    constraint `FK_Sociedad_DatosLaborales` foreign key (`sociedad_id`) references `Sociedad` (`id`)
    on update cascade on delete restrict,
    constraint `FK_Sede_DatosLaborales` foreign key (`sede_id`) references `Sede` (`id`)
    on update cascade on delete restrict,
    constraint `FK_Departamento_DatosLaborales` foreign key (`departamento_id`) references `Departamentos` (`id`)
    on update cascade on delete restrict,    
    constraint `FK_Grupo_DatosLaborales` foreign key (`grupo_id`) references `GruposEmpleado` (`id`)
    on update cascade on delete restrict,    
    constraint `FK_Cargo_DatosLaborales` foreign key (`cargo_id`) references `Cargos` (`id`)
    on update cascade on delete restrict,    
    constraint `FK_Usuario_DatosLaborales` foreign key (`user_id`) references `Usuario` (`id`)
    on update cascade on delete restrict      
    '''
    __tablename__="DatosLaborales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column (BIGINT, ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    departamento_id = Column (BIGINT, ForeignKey("Departamentos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    grupo_id = Column (BIGINT, ForeignKey("GruposEmpleado.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    cargo_id = Column (BIGINT, ForeignKey("Cargo.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)            
    tipo_contrato = Column(INTEGER, nullable=False)
    termino_contrato = Column(INTEGER, nullable=False)
    fecha_inicio =Column(DATE, nullable=False)    
    fecha_fin =Column(DATE, nullable=True)    
    periodo_salario = Column(INTEGER, nullable=False)    
    modalidad = Column(INTEGER, nullable=False)   
    dias_descanso=Column(VARCHAR(50), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
