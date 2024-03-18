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
class ViewPrecargaUser(Base):
    __tablename__="viewPrecargaUser"
    '''
    create or replace  view b1.viewPrecargaUser as
    SELECT 
    Usuario.id as user_id,
    rut as documento,
    nombres as nombres,
    apellido_paterno as apellidos,
    Contacto.email as correo,
    nacionalidad_id as nacionalidad,
    sexo_id as genero,
    fecha_nacimiento as fechaNacimiento,
    estado_civil_id as estadoCivil,
    Ubicacion.region_id as region,
    Ubicacion.comuna_id as localidad,
    Ubicacion.direccion as direccion,
    Contacto.movil as telefonoCelular,
    Contacto.fijo as telefonoLocal
    FROM b1.Usuario
    left join b1.Contacto on (Usuario.id = Contacto.user_id)
    left join b1.Ubicacion on (Usuario.id=Ubicacion.user_id)

    '''
    user_id = Column(BIGINT,primary_key=True)
    documento = Column(VARCHAR(100)) #VARCHAR(100) NOT NULL,
    nombres = Column (VARCHAR(100)) #VARCHAR(100) NOT NULL,
    apellidos  = Column (VARCHAR(100)) #paterno VARCHAR(100) NOT NULL,
    correo = Column (VARCHAR(250))
    nacionalidad = Column(BIGINT) #BIGINT NOT NULL,     
    genero = Column(BIGINT) #BIGINT NOT NULL,
    fechaNacimiento = Column(DATE)
    estadoCivil = Column(BIGINT) #BIGINT NOT NULL,    
    region = Column(BIGINT)
    localidad = Column(BIGINT)
    direccion = Column(TEXT)
    telefonoCelular=Column(VARCHAR(20))
    telefonoLocal=Column(VARCHAR(20))

   

