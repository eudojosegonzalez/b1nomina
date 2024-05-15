'''
Modelo que define a la vista  viewUsuariosGruposEmpleados, la cual contiene 
    Nombre del Grupos
    Registro de UsuarioGrupoEmepleados
    
Created 2024-03
'''
from config.database import Base
from sqlalchemy import Column, Integer, VARCHAR, BIGINT, DATE, DateTime, Boolean,TEXT, NUMERIC

# Definicion de una tabla
class viewUsuariosGruposEmpleados(Base):
    __tablename__="viewUsuariosGruposEmpleados"
    '''
    create or replace view b1.viewUsuariosGruposEmpleados as
    SELECT 
    UsuariosGruposEmpleado.* ,
    GruposEmpleado.nombre
    FROM b1.UsuariosGruposEmpleado
    inner join b1.GruposEmpleado
    on  (UsuariosGruposEmpleado.grupo_empleados_id=GruposEmpleado.id)

    '''
    id = Column(BIGINT,primary_key=True)
    sociedad_id	= Column(BIGINT)
    grupo_empleados_id = Column(BIGINT)
    user_id	= Column(BIGINT)
    created	 = Column(DateTime)
    updated	 = Column(DateTime)
    creator_user= Column(BIGINT)
    updater_user= Column(BIGINT)
    nombre=Column(VARCHAR(200))
    

   

