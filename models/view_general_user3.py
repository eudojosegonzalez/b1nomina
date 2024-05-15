'''
Modelo que define a la vista  viewGeneralUser3, la cual contiene 
    Datos Personales
    Datos de Contacto
    Datos SociedadUsuario
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column, Integer, VARCHAR, BIGINT, DATE, DateTime, Boolean,TEXT, NUMERIC

# Definicion de una tabla
class ViewGeneralUser3(Base):
    __tablename__="viewGeneralUser3"
    '''
    select `b1`.`Usuario`.`id` AS `id`,
    `b1`.`Usuario`.`rut` AS `rut`,
    `b1`.`Usuario`.`rut_provisorio` AS `rut_provisorio`,
    `b1`.`Usuario`.`nombres` AS `nombres`,
    `b1`.`Usuario`.`apellido_paterno` AS `apellido_paterno`,
    `b1`.`Usuario`.`apellido_materno` AS `apellido_materno`,
    `b1`.`Usuario`.`fecha_nacimiento` AS `fecha_nacimiento`,
    `b1`.`Usuario`.`sexo_id` AS `sexo_id`,
    `b1`.`Usuario`.`estado_civil_id` AS `estado_civil_id`,
    `b1`.`Usuario`.`nacionalidad_id` AS `nacionalidad_id`,
    `b1`.`Usuario`.`username` AS `username`,
    `b1`.`Usuario`.`password` AS `password`,
    `b1`.`Usuario`.`activo` AS `activo`,
    `b1`.`Usuario`.`created` AS `created`,
    `b1`.`Usuario`.`updated` AS `updated`,
    `b1`.`Usuario`.`creator_user` AS `creator_user`,
    `b1`.`Usuario`.`updater_user` AS `updater_user`,
    `b1`.`Contacto`.`email` AS `email`,
    `b1`.`SociedadUsuario`.`sociedad_id` AS `sociedad_id` 
    from ((`b1`.`Usuario` left join `b1`.`Contacto` 
        on(`b1`.`Usuario`.`id` = `b1`.`Contacto`.`user_id`)) 
    left join `b1`.`SociedadUsuario` 
        on(`b1`.`Usuario`.`id` = `b1`.`SociedadUsuario`.`user_id`));

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
    sociedad_id = Column(BIGINT)

   

