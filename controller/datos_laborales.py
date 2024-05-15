'''
Este archivo contiene las funciones básicas del CRUD de Datos Laborales en el sistema
Created 2024-02
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
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



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
     sociedad_id : int = Field(ge=1, le=1000)
    sede_id : int = Field(ge=1, le=1000)
    departamento_id : int = Field(ge=1, le=1000)  
    grupo_id : int = Field(ge=0, le=1000)      
    cargo_id : int = Field(ge=1, le=1000)    
    user_id : int = Field(ge=1, le=10000)    
    tipo_contrato : int = Field(ge=1, le=2)    
    termino_contrato : int = Field(ge=0, le=1) 
    fecha_inicio : date = None
    fecha_fin : date = None
    periodo_salario: int
    modalidad: int    
    dias_descanso: str = Field (min_length=1, max_length=50)
    salario_base : float 
    nivel_estudio_id : int
    unidad_sueldo : int = Field (ge=1, le=2)
    hora_ingreso : time
    hora_egreso : time   
    jefatura : int= Field (ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "sede_id": 1,                    
                    "departamento_id": 1,                    
                    "grupo_id":1,
                    "cargo_id":1,
                    "user_id":1,
                    "tipo_contrato":1,
                    "termino_contrato":1,
                    "fecha_inicio":'2024-01-01',
                    "fecha_fin":'1990-01-01',
                    "periodo_salario":30,
                    "modalidad":0,
                    "dias_descanso":"1",
                    "salario_base": 4500.00,
                    "nivel_estudio_id":1,
                    "unidad_sueldo":"1",
                    "hora_ingreso" : "08:00",
                    "hora_egreso" : "18:00",    
                    "jefatura":0                 
                }
            ]
        }
    } 
'''   

import pdb

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime
from time import time


# importamos el modelo de la base de datos
from models.datos_laborales import DatosLaborales as DatosLaboralesModel
from models.historico_datos_laborales import HistoricoDatosLaborales as HistoricoDatosLaboralesModel
from models.usuario_grupo import UsuariosGruposEmpleado as UsuariosGruposEmpleadoModel
from models.historico_usuario_grupo import HistoricoUsuariosGruposEmpleado as HistoricoUsuariosGruposEmpleadoModel
from models.usuario_departamento import UsuariosDepartamentos as UsuariosDepartamentosModel
from models.historico_usuario_departamento import HistoricoUsuariosDepartamentos as HistoricoUsuariosDepartamentosModel

#importamos el esquema de datos de Datos Laborales
from schemas.datos_laborales import DatosLaborales as DatosLaboralesSchema



# esto representa los metodos implementados en la tabla
class DatosLaboralesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico los Datos Laborales
    #@param datosLaborales: Modelo del registro de Datos Laborales
    #@param observavacion: Observación sobre el historico
    def create_historico_datos_laborales(self, datosLaborales: DatosLaboralesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoDatosLaboralesModel(
                datos_laborales_id=datosLaborales.id,
                sociedad_id=datosLaborales.sociedad_id,
                sede_id=datosLaborales.sede_id,
                departamento_id=datosLaborales.departamento_id,
                grupo_id=datosLaborales.grupo_id,
                cargo_id=datosLaborales.cargo_id,
                user_id=datosLaborales.user_id,
                tipo_contrato=datosLaborales.tipo_contrato,
                termino_contrato=datosLaborales.termino_contrato,
                fecha_inicio=datosLaborales.fecha_inicio,
                fecha_fin=datosLaborales.fecha_fin,
                periodo_salario=datosLaborales.periodo_salario,
                modalidad=datosLaborales.modalidad,
                dias_descanso=datosLaborales.dias_descanso,
                salario_base=datosLaborales.salario_base,
                unidad_sueldo=datosLaborales.unidad_sueldo,
                nivel_estudio_id=datosLaborales.nivel_estudio_id,
                hora_ingreso=datosLaborales.hora_ingreso,
                hora_egreso=datosLaborales.hora_egreso,
                jefatura=datosLaborales.jefatura,
                created=datosLaborales.created,
                updated=datosLaborales.updated,
                creator_user=datosLaborales.creator_user,
                updater_user=datosLaborales.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoSociedad)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
        

   # funcion para crear el registro de historico los Datos Laborales
    #@param datosLaborales: Modelo del registro de Datos Laborales
    #@param observavacion: Observación sobre el historico
    def create_historico_grupos_empleados(self, EmpleadoGrupo:UsuariosGruposEmpleadoModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoGrupoEmpleado= HistoricoUsuariosGruposEmpleadoModel (
                usuarios_grupo_empleados_id=EmpleadoGrupo.id,
                sociedad_id=EmpleadoGrupo.sociedad_id,
                grupo_empleados_id=EmpleadoGrupo.grupo_empleados_id	,
                user_id=EmpleadoGrupo.user_id,
                created=EmpleadoGrupo.created,
                updated=EmpleadoGrupo.updated,
                creator_user=EmpleadoGrupo.creator_user,
                updater_user=EmpleadoGrupo.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoGrupoEmpleado)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #funcion para crrear el historico de usuarios_departamento
    def create_historico_usuarios_departamento (self,usuarioDepartamento:UsuariosDepartamentosModel, observacion:str):
        # determinamos la fecha/hora actual
        paso=1
        ahora = datetime.datetime.now()
        try:
            '''
            id	bigint(20) AI PK
            usuarios_departamentos_id	bigint(20)
            sociedad_id	bigint(20)
            sede_id	bigint(20)
            departamento_id	bigint(20)
            user_id	bigint(20)
            created	datetime
            updated	datetime
            creator_user	bigint(20)
            updater_user	bigint(20)
            fecha_registro	datetime
            observaciones	text
            
            '''
            paso=2
            historicoUsuarioDepartamento=HistoricoUsuariosDepartamentosModel(
                usuarios_departamentos_id=usuarioDepartamento.id,
                sociedad_id	=usuarioDepartamento.sociedad_id,
                sede_id=usuarioDepartamento.sede_id,
                departamento_id=usuarioDepartamento.departamento_id,
                user_id=usuarioDepartamento.user_id,
                created=usuarioDepartamento.created,
                updated=usuarioDepartamento.updated,
                creator_user=usuarioDepartamento.creator_user,
                updater_user=usuarioDepartamento.updater_user,
                fecha_registro=ahora,
                observaciones=observacion                             
            )    
            paso=3
            self.db.add (historicoUsuarioDepartamento)
            paso=4
            self.db.commit()
            
            paso=5
            result=True
            return (result)
        
        except ValueError as e:
            return( {"result":False,"error": str(e)})                


    # esta funcion permite crear un registro en la tabhla de usuarios_grupos
    def create_usuario_grupo (self,idGrupo:int,idSociedad : int, idUser:int, IdCreatorUser:int):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()       
        try:
            paso=2 
            empleadoGrupoExist=UsuariosGruposEmpleadoModel (
                sociedad_id=idSociedad,
                grupo_empleados_id=idGrupo,
                user_id=idUser,
                created=ahora,
                updated=ahora,
                creator_user=IdCreatorUser,
                updater_user=IdCreatorUser
            )
            paso=3
            self.db.add(empleadoGrupoExist)
            paso=4
            self.db.commit()

            #creamos el historico de grupo de empleados
            paso=5
            DatosLaboralesController.create_historico_grupos_empleados(self, empleadoGrupoExist,"Anexamos el usuario al grupo")        
            return (True)
        except ValueError as e:
            return( {"result":"False","cadenaError": f"Ocurrio el siguiente Error {str(e)} paso:{paso}"})   
        

    #actualizamos la asociacion usuario_grupo
    def actualiza_usuario_grupo (self,idGrupo:int,idSociedad : int, idUser:int, IdCreatorUser:int):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()  
        
        try:
            paso=2
            # existe lo actualizamos
            empleadoGrupoExist=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==idUser).first()
            #creamos el historico de grupo de empleados
            paso=3
            DatosLaboralesController.create_historico_grupos_empleados(self, empleadoGrupoExist,"Actualizacion del grupo del empleado")

            # actualizamos el grupo del empleado
            paso=4
            empleadoGrupoExist.grupo_empleados_id=idGrupo
            empleadoGrupoExist.updated=ahora
            empleadoGrupoExist.updater_user=IdCreatorUser  

            paso=5
            self.db.commit()
            
        except ValueError as e:
            return( {"result":"False","cadenaError": f"Ocurrio el siguiente Error {str(e)} paso:{paso}"})                       


    #esta funcion crea el regidtro usuario departamento
    def create_usuario_departamento(self,sociedadId : int, sedeId: int,departamentoId:int, userId:int,creatorUserId:int):
        paso=1
        ahora=datetime.datetime.now()
        '''
        id	bigint(20) AI PK
        sociedad_id	bigint(20)
        sede_id	bigint(20)
        departamento_id	bigint(20)
        user_id	bigint(20)
        created	datetime
        updated	datetime
        creator_user	bigint(20)
        updater_user	bigint(20)        
        '''
        try:
            paso=2
            newUsuarioDepartamentoExists=UsuariosDepartamentosModel(
                sociedad_id=sociedadId,
                sede_id=sedeId,
                departamento_id=departamentoId,
                user_id=userId,
                creator_user=creatorUserId,
                updater_user=creatorUserId,
                created=ahora,
                updated=ahora
            )

            paso=3
            self.db.add(newUsuarioDepartamentoExists)
            paso=4
            self.db.commit()
            
            #creamos el historico del usuario departamento
            paso=5
            DatosLaboralesController.create_historico_usuarios_departamento(self,newUsuarioDepartamentoExists,"Creacion del registro Usuario Departamento en el sistema")
            paso=6
            return (True)
                
        except ValueError as e:
            return( {"result":"False","cadenaError": f"Ocurrio el siguiente Error {str(e)} paso:{paso}"})  

    # esta funcion permite actuzlizar la asociacion usarios departamento
    def actualiza_usuario_departamento (self,sociedadId : int, sedeId: int,departamentoId:int, userId:int,creatorUserId:int):
        paso=1
        ahora=datetime.datetime.now()
        
        try:
            paso=2
            usuarioDepartamentoExists=self.db.query(UsuariosDepartamentosModel).filter(UsuariosDepartamentosModel.user_id==userId).first()
            
            #creamos el historico de usuario departamento antes de actualizar
            paso=3
            DatosLaboralesController.create_historico_usuarios_departamento(self,usuarioDepartamentoExists,"Actualización del regisrtro Usuario Departamento")            

            paso=4
            usuarioDepartamentoExists.sociedad_id=sociedadId
            usuarioDepartamentoExists.sede_id=sedeId
            usuarioDepartamentoExists.departamento_id=departamentoId
            
            paso=5
            #confiramos los cambios
            self.db.commit()
            
            return (True)
            
        except ValueError as e:
            return( {"result":"False","cadenaError": f"Ocurrio el siguiente Error {str(e)} paso:{paso}"})  
            
    
    #metodo para insertar  los datos laborales
    # @userCreatorId: Id del usuario que está creando el registro
    # @params datosLaborales: esquema de los datos laborales  que se desea insertar       
    def create_datos_laborales(self, datosLaborales:DatosLaboralesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        userId=datosLaborales.user_id        

        # verificamos que el usuario no tenga datos laborales previos
        nRecordDatosLaborales=  self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).count()

        if (nRecordDatosLaborales > 0):

            datoLaboralExists = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).first()
            return ({"result":"-1","estado":"Este usuario ya tiene datos laborales no puede volver a crearlo","data": datoLaboralExists})     
                
        else:
            #creamos el nuevo registro de Datos Laborales

            try:
                newDatosLaborales=DatosLaboralesModel(
                    sociedad_id=datosLaborales.sociedad_id,
                    sede_id=datosLaborales.sede_id,
                    departamento_id=datosLaborales.departamento_id,                
                    grupo_id=datosLaborales.grupo_id,                
                    cargo_id=datosLaborales.cargo_id,                
                    user_id=datosLaborales.user_id,
                    tipo_contrato=datosLaborales.tipo_contrato,                
                    termino_contrato=datosLaborales.termino_contrato,                
                    fecha_inicio=datosLaborales.fecha_inicio,
                    fecha_fin=datosLaborales.fecha_fin,
                    periodo_salario=datosLaborales.periodo_salario,
                    modalidad=datosLaborales.modalidad,
                    dias_descanso=datosLaborales.dias_descanso,
                    salario_base=datosLaborales.salario_base,
                    unidad_sueldo=datosLaborales.unidad_sueldo,
                    nivel_estudio_id=datosLaborales.nivel_estudio_id,   
                    hora_ingreso=datosLaborales.hora_ingreso,   
                    hora_egreso=datosLaborales.hora_egreso,  
                    jefatura=datosLaborales.jefatura,   
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newDatosLaborales)
                self.db.commit()

                #creamos el registro historico de los datos laborales
                DatosLaboralesController.create_historico_datos_laborales(self,newDatosLaborales,"Se creó un Dato Laboral en el sistema")

                #verificamos si existe usuario_grupo
                #buscamos si existe el registro en la tabla de gruposempleados
                paso=7
                nRecordGrupo=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==datosLaborales.user_id).count()
                paso=8
                if (nRecordGrupo>0):
                    #actualizamos    
                    DatosLaboralesController.actualiza_usuario_grupo(self,datosLaborales.grupo_id,datosLaborales.sociedad_id,datosLaborales.user_id,userCreatorId)

                else:
                    #no existe lo creamos
                    paso=13
                    DatosLaboralesController.create_usuario_grupo (self,datosLaborales.grupo_id,datosLaborales.sociedad_id,datosLaborales.user_id,userCreatorId)


                #verificamos si existe usuario_departamento
                paso=14
                nRecordDepartamento=self.db.query(UsuariosDepartamentosModel).filter(UsuariosDepartamentosModel.user_id==datosLaborales.user_id).count()
                if (nRecordDepartamento >0):
                    #existe actualizamos
                    paso=15
                    DatosLaboralesController.actualiza_usuario_departamento(self,datosLaborales.sociedad_id,datosLaborales.sede_id,datosLaborales.departamento_id,datosLaborales.user_id,userCreatorId)
                else:    
                    #no existe creamos
                    paso=16
                    DatosLaboralesController.create_usuario_departamento(self,datosLaborales.sociedad_id,datosLaborales.sede_id,datosLaborales.departamento_id,datosLaborales.user_id,userCreatorId)
                
                paso=17
                data={
                    "id":newDatosLaborales.id,
                    "sociedad_id":newDatosLaborales.sociedad_id,
                    "sede_id":newDatosLaborales.sede_id,
                    "departamento_id":newDatosLaborales.departamento_id,
                    "grupo_id":newDatosLaborales.departamento_id,
                    "cargo_id":newDatosLaborales.cargo_id,
                    "user_id":newDatosLaborales.user_id,
                    "tipo_contrato":newDatosLaborales.tipo_contrato,
                    "termino_contrato":newDatosLaborales.termino_contrato,
                    "fecha_inicio":newDatosLaborales.fecha_inicio,
                    "fecha_fin":newDatosLaborales.fecha_fin,
                    "periodo_salario":newDatosLaborales.periodo_salario,
                    "modalidad":newDatosLaborales.modalidad,
                    "dias_descanso":newDatosLaborales.dias_descanso,
                    "salario_base":newDatosLaborales.salario_base,
                    "unidad_sueldo":newDatosLaborales.unidad_sueldo,
                    "nivel_estudio_id":newDatosLaborales.nivel_estudio_id,
                    "hora_ingreso":str(newDatosLaborales.hora_ingreso),
                    "hora_egreso":str(newDatosLaborales.hora_egreso), 
                    "jefatura":newDatosLaborales.jefatura,               
                    "created": newDatosLaborales.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newDatosLaborales.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newDatosLaborales.creator_user,
                    "updater_user":newDatosLaborales.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos Laborales por ID
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_datos_laborales(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos laborales
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales
            try:
                datosLaboralesExists = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == id).first()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los Datos Laborales","data":datosLaboralesExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para consultar los datos Laborales por user_id
    def get_datos_laborales_userid(self,userId:int):

        # buscamos si este existe este dato laboral
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este usuario
            try:
                datosLaboralesExists = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).first()                  
                # devolvemos los datos laborales
                data={
                    "id":datosLaboralesExists.id,
                    "sociedad_id":datosLaboralesExists.sociedad_id,
                    "sede_id":datosLaboralesExists.sede_id,
                    "departamento_id":datosLaboralesExists.departamento_id,
                    "grupo_id":datosLaboralesExists.grupo_id,                    
                    "cargo_id":datosLaboralesExists.cargo_id,                    
                    "user_id":datosLaboralesExists.user_id,                    
                    "tipo_contrato":datosLaboralesExists.tipo_contrato,
                    "termino_contrato":datosLaboralesExists.termino_contrato,
                    "fecha_inicio":datosLaboralesExists.fecha_inicio,
                    "fecha_fin":datosLaboralesExists.fecha_fin,
                    "periodo_salario":datosLaboralesExists.periodo_salario,
                    "modalidad":datosLaboralesExists.modalidad,
                    "dias_descanso":datosLaboralesExists.dias_descanso,    
                    "salario_base":datosLaboralesExists.salario_base,                
                    "unidad_sueldo":datosLaboralesExists.unidad_sueldo,
                    "nivel_estudio_id":datosLaboralesExists.nivel_estudio_id,   
                    "hora_ingreso":str(datosLaboralesExists.hora_ingreso), 
                    "hora_egreso":str(datosLaboralesExists.hora_egreso),     
                    "jefatura":datosLaboralesExists.jefatura,                                
                    "created":datosLaboralesExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":datosLaboralesExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":datosLaboralesExists.creator_user,
                    "updater_user":datosLaboralesExists.updater_user
                }
                return ({"result":"1","estado":"Se consiguieron los Datos Laborales","data":data})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})    
            
             
            
    # metodo para consultar todas los Datos Laborales
    def list_datos_laborales(self):
        consulta = self.db.query(DatosLaboralesModel)
        result=consulta.all()
        return (result)


    # metodo para consultar todas los Datos Laborales
    def list_datos_laborales_sociedad(self,Id ):
        consulta = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.sociedad_id==Id)
        result=consulta.all()
        return (result)
 
            
                        
    #metodo para consultar los datos Laborales por sede_id
    def list_datos_laborales_sede(self,Id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.sede_id == Id).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este usuario
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.sede_id == Id).all()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los dtos laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})                      
            

            
    #metodo para consultar los datos Laborales por deprtamento_id
    def list_datos_laborales_departamento(self,Id:int):

        # busrcamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.departamento_id == Id).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este departamento
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este departamento
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.departamento_id == Id).all()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los dtos laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            
            
    #metodo para consultar los datos Laborales por grupo_id
    def list_datos_laborales_grupo(self,Id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.grupo_id == Id).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este grupo
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este grupo
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.grupo_id == Id).all()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los dtos laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
                                             
 
    #metodo para actualizar los datos laborales por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params datosLaborale: esquema de los datos laborales que se estan actualizando
    # @params id: Id de los datos laborales que será actualizado
    def update_datos_laborales(self, datosLaborales:DatosLaboralesSchema, userUpdaterId:int, id:int):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este dato laboral existe
        paso=2
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == id).count()
        
        #pdb.set_trace()
        
        if (nRecord == 0):
            # no se consiguieron los datos laborales
            paso=3
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                paso=4
                #extraemos los datos para guardar el histórico
                datosLaboralesExists = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == id).first()             

                #creamos el registro historico de datos laborales
                paso=5
                self.create_historico_datos_laborales(datosLaboralesExists ,"Actualización de los Datos Laborales")

                #registramnos los cambios en la tabla de datos laborales
                datosLaboralesExists.sociedad_id=datosLaborales.sociedad_id,
                datosLaboralesExists.sede_id=datosLaborales.sede_id,
                datosLaboralesExists.departamento_id=datosLaborales.departamento_id,
                datosLaboralesExists.grupo_id=datosLaborales.grupo_id,
                datosLaboralesExists.cargo_id=datosLaborales.cargo_id,
                datosLaboralesExists.user_id=datosLaborales.user_id,                
                datosLaboralesExists.tipo_contrato=datosLaborales.tipo_contrato, 
                datosLaboralesExists.termino_contrato=datosLaborales.termino_contrato, 
                datosLaboralesExists.fecha_inicio=datosLaborales.fecha_inicio,                 
                datosLaboralesExists.fecha_fin=datosLaborales.fecha_fin, 
                datosLaboralesExists.periodo_salario=datosLaborales.periodo_salario, 
                datosLaboralesExists.modalidad=datosLaborales.modalidad, 
                datosLaboralesExists.dias_descanso=datosLaborales.dias_descanso, 
                datosLaboralesExists.salario_base=datosLaborales.salario_base,
                datosLaboralesExists.unidad_sueldo=datosLaborales.unidad_sueldo,
                datosLaboralesExists.nivel_estudio_id=datosLaborales.nivel_estudio_id,
                datosLaboralesExists.hora_ingreso=datosLaborales.hora_ingreso,
                datosLaboralesExists.hora_egreso=datosLaborales.hora_egreso,
                datosLaboralesExists.jefatura=datosLaborales.jefatura,
                datosLaboralesExists.updated=ahora,
                datosLaboralesExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                paso=6
                self.db.commit()

                #actualizamos el registro de datos laborales
                #buscamos si existe el registro en la tabla de gruposempleados
                paso=7
                nRecordGrupo=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==datosLaborales.user_id).count()
                paso=8
                if (nRecordGrupo>0):
                    #actualizamos    
                    DatosLaboralesController.actualiza_usuario_grupo(self,datosLaborales.grupo_id,datosLaborales.sociedad_id,datosLaborales.user_id,userUpdaterId )

                else:
                    #no existe lo creamos
                    paso=13
                    DatosLaboralesController.create_usuario_grupo (self,datosLaborales.grupo_id,datosLaborales.sociedad_id,datosLaborales.user_id,userUpdaterId)

                                
                #verificamos si existe usuario_departamento
                paso=14
                nRecordDepartamento=self.db.query(UsuariosDepartamentosModel).filter(UsuariosDepartamentosModel.user_id==datosLaborales.user_id).count()
                if (nRecordDepartamento >0):
                    #existe actualizamos
                    paso=15
                    DatosLaboralesController.actualiza_usuario_departamento(self,datosLaborales.sociedad_id,datosLaborales.sede_id,datosLaborales.departamento_id,datosLaborales.user_id,userUpdaterId)
                else:    
                    #no existe creamos
                    paso=16
                    DatosLaboralesController.create_usuario_departamento(self,datosLaborales.sociedad_id,datosLaborales.sede_id,datosLaborales.departamento_id,datosLaborales.user_id,userUpdaterId)                
                
                paso=17
                data={
                    "id":datosLaboralesExists.id,
                    "sociedad_id":datosLaboralesExists.sociedad_id,
                    "sede_id":datosLaboralesExists.sede_id,
                    "departamento_id":datosLaboralesExists.departamento_id,
                    "grupo_id":datosLaboralesExists.grupo_id,                    
                    "cargo_id":datosLaboralesExists.cargo_id,                    
                    "user_id":datosLaboralesExists.user_id,                    
                    "tipo_contrato":datosLaboralesExists.tipo_contrato,
                    "termino_contrato":datosLaboralesExists.termino_contrato,
                    "fecha_inicio":datosLaboralesExists.fecha_inicio,
                    "fecha_fin":datosLaboralesExists.fecha_fin,
                    "periodo_salario":datosLaboralesExists.periodo_salario,
                    "modalidad":datosLaboralesExists.modalidad,
                    "dias_descanso":datosLaboralesExists.dias_descanso,    
                    "salario_base":datosLaboralesExists.salario_base,                
                    "unidad_sueldo":datosLaboralesExists.unidad_sueldo,
                    "nivel_estudio_id":datosLaboralesExists.nivel_estudio_id,   
                    "hora_ingreso":str(datosLaboralesExists), 
                    "hora_egreso":str(datosLaboralesExists.hora_egreso),  
                    "jefatura":datosLaboralesExists.jefatura,
                    "created":datosLaboralesExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":datosLaboralesExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":datosLaboralesExists.creator_user,
                    "updater_user":datosLaboralesExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                paso=18
                return ({"result":"1","estado":"Se actualizó los datos laborales","data":data})
            
            except ValueError as e:
                return( {"result":"-3","cadenaError": f"Ocurrio el siguiente Error {str(e)} paso:{paso}"})                    


    # metodo para listar los datos historicos  de un Dato Laboral
    # @params id: Id del dato laboral que se esta consultando
    def list_history_datos_laborales(self,  id:int):

        # buscamos si exite el dato laboral en el historico
        nRecord = self.db.query(HistoricoDatosLaboralesModel).filter(HistoricoDatosLaboralesModel.datos_laborales_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del dato laboral
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del dato laboral
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoDatosLaboralesModel).filter(HistoricoDatosLaboralesModel.datos_laborales_id == id)
                listHistoryDatosLaborales=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos del Dato Laboral ","data": listHistoryDatosLaborales})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     