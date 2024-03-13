'''
Modelo que define a la vista  viewGeneralBancariosUser, la cual contiene 
    Datos Personales
    Datos Bancarios de Usuario
    Datos del Banco
Created 2024-01
'''
from config.database import Base
from sqlalchemy import Column, Integer, VARCHAR, BIGINT, DATE, DateTime, Boolean,TEXT

# Definicion de una tabla
class ViewGeneralBancariosUser(Base):
    __tablename__="viewGeneralBancariosUser"
    '''
    create or replace view b1.viewGeneralBancariosUser as
    SELECT 
    Usuario.id as user_id,
    Usuario.rut, 
    Usuario.rut_provisorio,
    Usuario.nombres,
    Usuario.apellido_paterno,
    Usuario.apellido_materno,
    BancariosUser.id as bancari_id,
    BancariosUser.banco_id,
    BancariosUser.numero_cuenta,
    BancariosUser.en_uso,
    BancariosUser.terceros,
    BancariosUser.rut_tercero,
    BancariosUser.nombre_tercero,
    BancariosUser.email_tercero,
    Bancos.nombre as banco_nombre,
    Bancos.codigo as banco_codigo
    FROM b1.Usuario
    inner join b1.BancariosUser
        on (Usuario.id=BancariosUser.user_id)
    inner join b1.Bancos
        on (Bancos.id=BancariosUser.user_id);
    '''
    rut = Column(VARCHAR(100)) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100)) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100)) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100)) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100))  #VARCHAR(100) NULL,
    bancario_id = Column (BIGINT, primary_key=True)
    banco_id = Column (BIGINT)
    numero_cuenta = Column (VARCHAR(100))
    en_uso = Column(Integer)
    terceros = Column(Integer)
    rut_tercero	 = Column (VARCHAR(100)) #varchar(100)
    nombre_tercero	= Column (VARCHAR(100)) #varchar(100)
    email_tercero	= Column (VARCHAR(250)) #varchar(250)
    banco_nombre	= Column (VARCHAR(250)) #varchar(150)
    banco_codigo	= Column (VARCHAR(250)) #varchar(50) 





   

