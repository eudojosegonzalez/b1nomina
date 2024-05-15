'''
Modelo que define a la tabla  estatus de inscripcion del usuario
Created 2024-04
'''
from config.database import Base
from sqlalchemy import Column,  BIGINT, DateTime,   ForeignKey, INTEGER

# Definicion de la tabla de Contacto de usuarios
class EstatusInscripcion(Base):
    '''
	`id` bigint(20) NOT NULL AUTO_INCREMENT,
-- ------ personales     
	`user_id` bigint(20) NOT NULL,
	`rut` int not NULL default 0,
	`nombre` int not NULL default 0,    
	`apellido` int not NULL default 0,   
	`nacionalidad` int not NULL default 0,    
	`sexo` int not NULL default 0,   
	`fecha_nac` int not NULL default 0,    
	`estado_civil` int not NULL default 0,   
-- ubicacion ----------------
	`region` int not NULL default 0,   
	`comuna` int not NULL default 0,    
	`direccion` int not NULL default 0,   
-- contacto ------------------------------------
	`telefono` int not NULL default 0,    
	`email` int not NULL default 0,    
-- laborales ----------------------------------- 
	`tipo_contrato` int not NULL default 0,   
	`termino` int not NULL default 0,    
	`fecha_contratacion` int not NULL default 0,   
	`salario_base` int not NULL default 0,    
	`unidad_sueldo` int not NULL default 0,   
	`monto_sueldo` int not NULL default 0,    
	`sociedad` int not NULL default 0,       
	`sede` int not NULL default 0,   
	`departamento` int not NULL default 0,   
	`cargo` int not NULL default 0,    
	`grupo` int not NULL default 0,   
	`modalidad` int not NULL default 0,    
	`dias_descanso` int not NULL default 0,
	`nivel_estudio` int not NULL default 0,    
 -- datos de pago ------------------------------------------- 
	`medio` int not NULL default 0,   
	`banco` int not NULL default 0,    
	`tipo_cuenta` int not NULL default 0,   
	`numero` int not NULL default 0,    
-- archivos necesarios ----------------------------------------------    
	`foto` int not NULL default 0,   
	`cv` int not NULL default 0,    
	`contrato` int not NULL default 0,     
-- ----------------------------------------------
	`created` datetime NOT NULL,
	`updated` datetime NOT NULL,
	`creator_user` bigint(20) NOT NULL,
	`updater_user` bigint(20) NOT NULL,
	PRIMARY KEY (`id`)
    '''
    __tablename__="EstatusInscripcion"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True)
    rut=Column(INTEGER , nullable=False) 
    nombre=Column(INTEGER , nullable=False)     
    apellido=Column(INTEGER , nullable=False)    
    nacionalidad=Column(INTEGER , nullable=False)     
    sexo=Column(INTEGER , nullable=False)    
    fecha_nac=Column(INTEGER , nullable=False)     
    estado_civil=Column(INTEGER , nullable=False)    
    # --ubicacion ----------------
    region=Column(INTEGER , nullable=False)    
    comuna=Column(INTEGER , nullable=False)     
    direccion=Column(INTEGER , nullable=False)    
    # --contacto ------------------------------------
    telefono=Column(INTEGER , nullable=False)     
    email=Column(INTEGER , nullable=False)     
    # --laborales ---------------------------------# --
    tipo_contrato=Column(INTEGER , nullable=False)    
    termino=Column(INTEGER , nullable=False)     
    fecha_contratacion=Column(INTEGER , nullable=False)    
    salario_base=Column(INTEGER , nullable=False)     
    unidad_sueldo=Column(INTEGER , nullable=False)    
    monto_sueldo=Column(INTEGER , nullable=False)     
    sociedad=Column(INTEGER , nullable=False)        
    sede=Column(INTEGER , nullable=False)    
    departamento=Column(INTEGER , nullable=False)    
    cargo=Column(INTEGER , nullable=False)     
    grupo=Column(INTEGER , nullable=False)    
    modalidad=Column(INTEGER , nullable=False)     
    dias_descanso=Column(INTEGER , nullable=False) 
    nivel_estudio=Column(INTEGER , nullable=False)     
    # --datos de pago -----------------------------------------# --
    medio=Column(INTEGER , nullable=False)    
    banco=Column(INTEGER , nullable=False)     
    tipo_cuenta=Column(INTEGER , nullable=False)    
    numero=Column(INTEGER , nullable=False)     
    # --archivos necesarios --------------------------------------------# --   
    foto=Column(INTEGER , nullable=False)    
    cv=Column(INTEGER , nullable=False)     
    contrato=Column(INTEGER , nullable=False)  
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
 



