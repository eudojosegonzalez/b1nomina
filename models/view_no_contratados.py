'''
Modelo que define a la vista  viewGeneralUser, la cual contiene 
    Datos Personales
    Datos de Contacto
    Datos de Ubicacion
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column, Integer, VARCHAR, BIGINT, DATE, DateTime, Boolean,TEXT, NUMERIC

# Definicion de una tabla
class ViewNoContratados(Base):
    __tablename__="viewNoContratados"
    '''
    CREATE or replace VIEW `b1`.`viewNoContratados` AS 
    select `viewGeneralUser2`.`id` AS `id`,
    `viewGeneralUser2`.`rut` AS `rut`,
    `viewGeneralUser2`.`rut_provisorio` AS `rut_provisorio`,
    `viewGeneralUser2`.`nombres` AS `nombres`,
    `viewGeneralUser2`.`apellido_paterno` AS `apellido_paterno`,
    `viewGeneralUser2`.`apellido_materno` AS `apellido_materno`,
    `viewGeneralUser2`.`fecha_nacimiento` AS `fecha_nacimiento`,
    `viewGeneralUser2`.`sexo_id` AS `sexo_id`,
    `viewGeneralUser2`.`estado_civil_id` AS `estado_civil_id`,
    `viewGeneralUser2`.`nacionalidad_id` AS `nacionalidad_id`,
    `viewGeneralUser2`.`username` AS `username`,
    `viewGeneralUser2`.`password` AS `password`,
    `viewGeneralUser2`.`activo` AS `activo`,
    `viewGeneralUser2`.`created` AS `created`,
    `viewGeneralUser2`.`updated` AS `updated`,
    `viewGeneralUser2`.`creator_user` AS `creator_user`,
    `viewGeneralUser2`.`updater_user` AS `updater_user`,
    `viewGeneralUser2`.`email` AS `email`,
    `viewGeneralUser2`.`fijo` AS `fijo`,
    `viewGeneralUser2`.`movil` AS `movil`,
    `viewGeneralUser2`.`region_id` AS `region_id`,
    `viewGeneralUser2`.`comuna_id` AS `comuna_id`,
    `viewGeneralUser2`.`direccion` AS `direccion`,
    `viewGeneralUser2`.`nomregion` AS `nomregion`,
    `viewGeneralUser2`.`orden` AS `orden`,
    `viewGeneralUser2`.`nomcomuna` AS `nomcomuna`,
    `viewGeneralUser2`.`sueldo` AS `sueldo`,
    `viewGeneralUser2`.`cargo` AS `cargo`,
    `viewGeneralUser2`.`sociedad_id` AS `sociedad_id`, 
    ifnull(`b1`.`CVUsuarios`.`estado`,'1') as `cv_estado`,
    ifnull(`b1`.`CVUsuarios`.`url`,'') as `cv_url`
    from `b1`.`viewGeneralUser2`
    left join `b1`.`CVUsuarios` on  (`b1`.`viewGeneralUser2`.`id` =`b1`.`CVUsuarios`.`user_id`) 
    where `viewGeneralUser2`.`id` not in (select `b1`.`DatosLaborales`.`user_id` from `b1`.`DatosLaborales`)
    '''
    id = Column(BIGINT,primary_key=True)
    rut = Column(VARCHAR(100)) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100)) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100)) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100)) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100))  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE) #DATE NOT NULL,
    sexo_id = Column(BIGINT) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250)) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250)) #NOT NULL,  
    activo = Column(Boolean) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime) #datetime NOT NULL,    
    updated = Column (DateTime)  #datetime NOT NULL,
    creator_user= Column(BIGINT) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT) #user BIGINT NOT NULL,  
    email = Column(VARCHAR(250)) 
    fijo = Column(VARCHAR(20)) 
    movil= Column(VARCHAR(20)) 
    region_id = Column(BIGINT)
    comuna_id= Column(BIGINT)
    direccion = Column(TEXT)
    nomregion = Column(VARCHAR(250))
    orden = Column(Integer)
    nomcomuna = Column(VARCHAR(150))
    sueldo = Column(NUMERIC (18,4))
    cargo = Column(VARCHAR(50))
    sociedad_id = Column(BIGINT)
    cv_estado = Column(Integer)
    cv_url=Column(VARCHAR(250))
    contrato_estado = Column(Integer)
    contrato_url=Column(VARCHAR(250))    

   

