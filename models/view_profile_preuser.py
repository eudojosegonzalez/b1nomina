'''
Modelo que define a la vista  viewProfileUser, la cual contiene 
    Datos Personales
    Datos de Contacto
    Datos Ubicacion
    Datos SociedadUsuario
    Datos Laborales
    Datos Pago    
    Datos Bancarios Usuario
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column, INTEGER, VARCHAR, BIGINT, DATE, DateTime, TEXT, NUMERIC

# Definicion de una tabla
class ViewProfilePreUser(Base):
    '''
    CREATE or replace VIEW `b1`.`viewProfilePreUser` AS 
    select 
    `b1`.`Usuario`.`id` AS `user_id`,
    `b1`.`Usuario`.`rut` AS `rut`,
    `b1`.`Usuario`.`rut_provisorio` AS `rut_provisorio`,
    `b1`.`Nacionalidad`.`Nacionalidad` AS `Nacionalidad`,
    `b1`.`Usuario`.`nombres` AS `nombres`,
    `b1`.`Usuario`.`apellido_paterno` AS `apellido_paterno`,
    `b1`.`Usuario`.`apellido_materno` AS `apellido_materno`,
    `b1`.`Usuario`.`fecha_nacimiento` AS `fecha_nacimiento`,
    `b1`.`Usuario`.`sexo_id` AS `sexo_id`,
    `b1`.`Usuario`.`estado_civil_id` AS `estado_civil_id`,
    `b1`.`Usuario`.`nacionalidad_id` AS `nacionalidad_id`,
    `b1`.`Usuario`.`username` AS `username`,
    `b1`.`Usuario`.`activo` AS `activo`,
    ifnull(`b1`.`Contacto`.`email`,'') AS `email`,
    ifnull(`b1`.`Contacto`.`fijo`,'') AS `fijo`,
    ifnull(`b1`.`Contacto`.`movil`,'') AS `movil`,
    ifnull(`b1`.`Ubicacion`.`region_id`,'') AS `region_id`,
    ifnull(`b1`.`Ubicacion`.`comuna_id`,'') AS `comuna_id`,
    ifnull(`b1`.`Ubicacion`.`direccion`,'') AS `direccion`,
    ifnull(`b1`.`Regiones`.`nombre`,'') AS `nomregion`,
    ifnull(`b1`.`Regiones`.`orden`,'') AS `orden`,
    ifnull(`b1`.`Comunas`.`nombre`,'') AS `nomcomuna`,
    ifnull(`b1`.`UsuariosDepartamentos`.`sociedad_id`,'') AS `sociedad_id`,
    ifnull(`b1`.`UsuariosDepartamentos`.`sede_id`,'') AS `sede_id`,
    ifnull(`b1`.`UsuariosDepartamentos`.`departamento_id`,'') AS `departamento_id`,
    ifnull(`b1`.`Departamentos`.`nombre`,'') AS `nomdepartamento`,
    ifnull(`b1`.`UsuariosGruposEmpleado`.`grupo_empleados_id`,'') AS `grupo_id`,
    ifnull(`b1`.`GruposEmpleado`.`nombre`,'') AS `nombre_grupo`,
    ifnull(`b1`.`Sede`.`nombre`,'') AS `nombre_sede`,
    ifnull(`b1`.`DatosLaborales`.`salario_base`,'') AS `salario_base`,
    ifnull(`b1`.`DatosLaborales`.`periodo_salario`,30) AS `periodo_salario`,
    ifnull(`b1`.`DatosLaborales`.`dias_descanso`,'6,7') AS `dias_descanso`,
    ifnull(`b1`.`DatosLaborales`.`unidad_sueldo`,'6,7') AS `unidad_sueldo`,
    ifnull(`b1`.`DatosLaborales`.`hora_ingreso`,'08:00') AS `hora_ingreso`,
    ifnull(`b1`.`DatosLaborales`.`hora_egreso`,'18:00') AS `hora_egreso`,
    ifnull(`b1`.`Cargos`.`nombre`,'') AS `cargo`,
    ifnull(`b1`.`DatosLaborales`.`cargo_id`,'') AS `cargo_id`,
    ifnull(`b1`.`BancariosUser`.`banco_id`,'') AS `banco_id`,
    ifnull(`b1`.`BancariosUser`.`numero_cuenta`,'') AS `numero_cuenta`,
    ifnull(`b1`.`BancariosUser`.`en_uso`,'') AS `en_uso`,
    ifnull(`b1`.`BancariosUser`.`terceros`,'') AS `terceros`,
    ifnull(`b1`.`BancariosUser`.`rut_tercero`,'') AS `rut_tercero`,
    ifnull(`b1`.`BancariosUser`.`nombre_tercero`,'') AS `nombre_tercero`,
    ifnull(`b1`.`BancariosUser`.`email_tercero`,'') AS `email_tercero`,
    '0' AS `vacaciones_acumuladas`,`b1`.`Sexo`.`descripcion` AS `sexo`,
    ifnull(`b1`.`Bancos`.`nombre`,'') AS `nombre_banco`,
    ifnull(`b1`.`DatosPago`.`medio`,'') AS `medio_pago`,
    ifnull(`b1`.`DatosPago`.`tipo_cuenta`,'') AS `tipo_cuenta`,
    ifnull(`b1`.`DatosLaborales`.`tipo_contrato`,'1') AS `tipo_contrato`,
    ifnull(`b1`.`DatosLaborales`.`termino_contrato`,'1') AS `termino_contrato`,
    ifnull(`b1`.`DatosLaborales`.`fecha_inicio`,'') AS `fecha_inicio`,
    ifnull(if(`b1`.`DatosLaborales`.`fecha_fin` <> '1990-01-01',`b1`.`DatosLaborales`.`fecha_fin`,''),'') AS `fecha_fin`,
    ifnull(`b1`.`DatosLaborales`.`modalidad`,'') AS `modalidad`,
    ifnull(`b1`.`DatosLaborales`.`jefatura`,0) AS `jefatura`,'' AS `rol_user`,
    ifnull(`b1`.`NivelEstudio`.`descripcion`,'') AS `nivel_estudio`,
    ifnull(`b1`.`FotosUsuarios`.`url`,'') AS `foto` 
    from (((((((((((((((((((((`b1`.`Usuario` 
    left join `b1`.`Contacto` on(`b1`.`Usuario`.`id` = `b1`.`Contacto`.`user_id`)) 
    left join `b1`.`Ubicacion` on(`b1`.`Usuario`.`id` = `b1`.`Ubicacion`.`user_id`)) 
    left join `b1`.`Regiones` on(`b1`.`Ubicacion`.`region_id` = `b1`.`Regiones`.`id`)) 
    left join `b1`.`Comunas` 
    on(`b1`.`Ubicacion`.`comuna_id` = `b1`.`Comunas`.`id` and `b1`.`Ubicacion`.`region_id` = `b1`.`Comunas`.`region_id`)) 
    left join `b1`.`UsuariosDepartamentos` on(`b1`.`UsuariosDepartamentos`.`user_id` = `b1`.`Usuario`.`id`)) 
    left join `b1`.`DatosLaborales` on(`b1`.`Usuario`.`id` = `b1`.`DatosLaborales`.`user_id`)) 
    left join `b1`.`Departamentos` on(`b1`.`UsuariosDepartamentos`.`departamento_id` = `b1`.`Departamentos`.`id`)) 
    left join `b1`.`UsuariosGruposEmpleado` on(`b1`.`UsuariosGruposEmpleado`.`user_id` = `b1`.`Usuario`.`id`)) 
    left join `b1`.`GruposEmpleado` on(`b1`.`GruposEmpleado`.`id` = `b1`.`UsuariosGruposEmpleado`.`grupo_empleados_id`)) 
    left join `b1`.`Sede` on(`b1`.`Sede`.`id` = `b1`.`UsuariosDepartamentos`.`sede_id`)) 
    left join `b1`.`Cargos` on(`b1`.`DatosLaborales`.`cargo_id` = `b1`.`Cargos`.`id`)) 
    left join `b1`.`CargosUsuario` 
    on(`b1`.`CargosUsuario`.`cargo_id` = `b1`.`Cargos`.`id` and `b1`.`CargosUsuario`.`user_id` = `b1`.`Usuario`.`id`)) 
    left join `b1`.`Nacionalidad` on(`b1`.`Usuario`.`nacionalidad_id` = `b1`.`Nacionalidad`.`id`)) 
    left join `b1`.`BancariosUser` on(`b1`.`BancariosUser`.`user_id` = `b1`.`Usuario`.`id`)) 
    left join `b1`.`Sexo` on(`b1`.`Sexo`.`id` = `b1`.`Usuario`.`sexo_id`)) 
    left join `b1`.`DatosPago` on(`b1`.`DatosPago`.`user_id` = `b1`.`Usuario`.`id`)) 
    left join `b1`.`Bancos` on(`b1`.`Bancos`.`id` = `b1`.`BancariosUser`.`banco_id`)) 
    left join `b1`.`NivelEstudio` on(`b1`.`NivelEstudio`.`id` = `b1`.`DatosLaborales`.`nivel_estudio_id`)) 
    left join `b1`.`TerminoContrato` on(`b1`.`DatosLaborales`.`termino_contrato` = `b1`.`TerminoContrato`.`id`)) 
    left join `b1`.`TiposContrato` on(`b1`.`DatosLaborales`.`tipo_contrato` = `b1`.`TiposContrato`.`id`)) 
    left join `b1`.`FotosUsuarios` on(`b1`.`FotosUsuarios`.`user_id` = `b1`.`Usuario`.`id`)) 
    group by `b1`.`Usuario`.`id`;  
    '''
    __tablename__="viewProfilePreUser"
    user_id = Column(BIGINT,primary_key=True)
    rut	= Column(VARCHAR(100))
    rut_provisorio= Column(VARCHAR(100))
    Nacionalidad= Column(VARCHAR(150))
    nombres= Column(VARCHAR(100))
    apellido_paterno= Column(VARCHAR(100))
    apellido_materno= Column(VARCHAR(100))
    fecha_nacimiento= Column(DATE)
    sexo_id	= Column(INTEGER)
    estado_civil_id	= Column(INTEGER)
    nacionalidad_id	= Column(INTEGER)
    username= Column(VARCHAR(250))
    activo		= Column(INTEGER)
    email= Column(VARCHAR(250))
    fijo= Column(VARCHAR(20))
    movil= Column(VARCHAR(20))
    region_id	= Column(INTEGER)
    comuna_id	= Column(INTEGER)
    direccion= Column(TEXT)
    nomregion= Column(VARCHAR(250))
    orden	= Column(INTEGER)
    nomcomuna= Column(VARCHAR(150))
    sociedad_id		= Column(INTEGER)
    sede_id		= Column(INTEGER)
    departamento_id	= Column(INTEGER)
    nomdepartamento= Column(VARCHAR(200))
    grupo_id	= Column(INTEGER)
    nombre_grupo= Column(VARCHAR(2000))
    nombre_sede= Column(VARCHAR(200))
    salario_base= Column(NUMERIC(18,4))
    periodo_salario=Column(INTEGER)
    dias_descanso=Column(VARCHAR(50))
    unidad_sueldo= Column(VARCHAR(4))
    hora_ingreso= Column(VARCHAR(10))
    hora_egreso= Column(VARCHAR(10))
    cargo= Column(VARCHAR(200))
    cargo_id= Column(VARCHAR(20))
    banco_id= Column(VARCHAR(20))
    numero_cuenta= Column(VARCHAR(100))
    en_uso	= Column(VARCHAR(15))
    terceros= Column(VARCHAR(15))
    rut_tercero= Column(VARCHAR(100))
    nombre_tercero= Column(VARCHAR(100))
    email_tercero= Column(VARCHAR(250))
    vacaciones_acumuladas	= Column(INTEGER)
    nombre_banco=Column(VARCHAR(200))
    medio_pago=Column(INTEGER)
    tipo_cuenta= Column(VARCHAR(11))	
    tipo_contrato=Column(INTEGER)
    termino_contrato=Column(INTEGER)
    fecha_inicio=Column(VARCHAR(20))
    fecha_fin=Column(VARCHAR(20))
    modalidad=Column(VARCHAR(20))   
    jefatura=Column(INTEGER)
    rol_user=Column(VARCHAR(50))  
    nivel_estudio=Column(VARCHAR(50))  
    nivel_estudio_id=Column(INTEGER)  
    foto =Column(TEXT)


    #metodp para convertir en diccionario
    def to_dict(self):
        result = {
            "user_id": self.user_id,
            "rut": self.rut  ,
            "rut_provisorio": self.rut_provisorio  ,
            "Nacionalidad": self.Nacionalidad  ,
            "nombres": self.nombres  ,
            "apellido_paterno": self.apellido_paterno  ,
            "apellido_materno": self.apellido_materno  ,
            "fecha_nacimiento": self.fecha_nacimiento  ,
            "sexo_id": self.sexo_id  ,
            "estado_civil_id": self.estado_civil_id  ,
            "nacionalidad_id": self.nacionalidad_id  ,
            "username": self.username  ,
            "activo": self.activo  ,
            "email": self.email  ,
            "fijo": self.fijo  ,
            "movil": self.movil  ,
            "region_id": self.region_id  ,
            "comuna_id": self.comuna_id  ,
            "direccion": self.direccion  ,
            "nomregion": self.nomregion  ,
            "orden": self.orden  ,
            "nomcomuna": self.nomcomuna  ,
            "sociedad_id": self.sociedad_id  ,
            "sede_id": self.sede_id  ,
            "departamento_id": self.departamento_id  ,
            "nomdepartamento": self.nomdepartamento  ,
            "grupo_id": self.grupo_id  ,
            "nombre_grupo": self.nombre_grupo  ,
            "nombre_sede": self.nombre_sede  ,
            "salario_base": self.salario_base  ,
            "periodo_salario": self.periodo_salario ,
            "dias_descanso": self.dias_descanso ,  
            "unidad_sueldo": self.unidad_sueldo ,
            "hora_ingreso": self.hora_ingreso  ,
            "hora_egreso": self.hora_egreso  ,
            "cargo": self.cargo  ,
            "cargo_id": self.cargo_id  ,
            "banco_id": self.banco_id  ,
            "numero_cuenta": self.numero_cuenta  ,
            "en_uso": self.en_uso  ,
            "terceros": self.terceros  ,
            "rut_tercero": self.rut_tercero  ,
            "nombre_tercero": self.nombre_tercero  ,
            "email_tercero": self.email_tercero  ,
            "vacaciones_acumuladas": self.vacaciones_acumuladas  ,
            "nombre_banco": self.nombre_banco ,
            "medio_pago": self.medio_pago ,
            "tipo_cuenta": self.tipo_cuenta  ,
            "tipo_contrato": self.tipo_contrato,
            "termino_contrato": self.termino_contrato ,
            "fecha_inicio": self.fecha_inicio  ,
            "fecha_fin": self.fecha_fin ,
            "modalidad": self.modalidad  ,   
            "jefatura": self.jefatura ,
            "rol_user": self.rol_user,    
            "nivel_estudio": self.nivel_estudio,    
            "nivel_estudio_id": self.nivel_estudio_id,    
            "foto": self.foto 
        }
        return (result)