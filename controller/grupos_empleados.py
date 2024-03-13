'''
Este archivo contiene las funciones básicas del CRUD de Grupos de Empleados
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="GruposEmpleado"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    es_honorario = Column(INTEGER, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    es_honorario = bool,
    nombre : str = Field(min_length=3, max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "es_honorario": True,
                    "nombre":"Demo"
                }
            ]
        }
    }    
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime


# importamos el modelo de la base de datos
from models.grupos_empleados import GruposEmpleado as GruposEmpleadoModel
from models.historico_grupos_empleados import HistoricoGruposEmpleado as HistoricoGruposEmpleadoModel


#importamos el esquema de datos de grupoEmpleadoes
from schemas.grupos_empleados import GruposEmpleado as GruposEmpleadoSchema



# esto representa los metodos implementados en la tabla
class GrupoEmpleadosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las grupoEmpleadoes
    #@param grupoEmpleado: Modelo del registro de grupoEmpleadoes
    #@param observavacion: Observación sobre el historico
    def create_historico_grupo_empleado (self, grupoEmpleado: GruposEmpleadoModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricogrupoEmpleado= HistoricoGruposEmpleadoModel(

                grupo_empleados_id=grupoEmpleado.id,
                es_honorario=grupoEmpleado.es_honorario,
                nombre=grupoEmpleado.nombre,
                created=grupoEmpleado.created,
                updated=grupoEmpleado.updated,
                creator_user=grupoEmpleado.creator_user,
                updater_user=grupoEmpleado.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricogrupoEmpleado)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la grupoEmpleado
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  grupoEmpleado que se desea insertar       
    def create_grupo_empleado(self, grupoEmpleado:GruposEmpleadoSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombregrupoEmpleado=grupoEmpleado.nombre.upper().strip()
        rutgrupoEmpleado=grupoEmpleado.rut.upper().strip()


        # contamos si existe una grupoEmpleado con el mismo nombre
        nRecordNombre = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.nombre == nombregrupoEmpleado).count()  

        if (nRecordNombre > 0):
            # buscamos la grupoEmpleado con el nombre y lo devolvemos
            grupoEmpleadoExists=self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.nombre == nombregrupoEmpleado).first() 

            # devolvemos la grupoEmpleado que ya existe
            return ({"result":"-1","estado":"Existe una grupoEmpleado con ese nombre","data":grupoEmpleadoExists})
        else:    
            #creamos el nuevo registro de banco
            try:
                newgrupoEmpleado=GruposEmpleadoModel(
                    sociedad_id=grupoEmpleado.sociedad_id,
                    es_honorario=grupoEmpleado.es_honorario,
                    nombre=((grupoEmpleado).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newgrupoEmpleado)
                self.db.commit()

                #creamos el registro historico de sede
                self.create_historico_grupo_empleado(newgrupoEmpleado,"Se creó una grupoEmpleado en el sistema")
  
                data={
                    "id":newgrupoEmpleado.id,
                    "sociedad_id":newgrupoEmpleado.sociedad_id,
                    "es_honorario":newgrupoEmpleado.es_honorario,
                    "nombre": newgrupoEmpleado.nombre,
                    "created": newgrupoEmpleado.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newgrupoEmpleado.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newgrupoEmpleado.creator_user,
                    "updater_user":newgrupoEmpleado.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una grupoEmpleado por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_grupo_empleados(self,id:int):

        # buscamos si esta grupoEmpleado existe
        nRecord = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta grupo Empleado
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de la grupo Empleado
            try:
                grupoEmpleadoExits = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.id == id).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de la Grupo Empleado","data":grupoEmpleadoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las grupo Empleadoes
    # @params cadena: cadena que se buscara en la tabla grupoEmpleadoes comparando con el campo nombre 
    def search_grupo_empleados(self,finding ):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.nombre.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de una grupo Empleado por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params grupoEmpleado: esquema de los datos de la grupoEmpleado 
    # @params id: Id de la grupoEmpleado que será actualizado
    def update_grupo_empleados(self, grupoEmpleado:GruposEmpleadoSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este grupoEmpleado existe
        nRecord = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la grupoEmpleado
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                grupoEmpleadoExists = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.id == id).first()             

                #creamos el registro historicos ociedades 
                self.create_historico_grupo_empleado(grupoEmpleadoExists ,"Actualización de la data de la grupoEmpleado")

                #registramnos los cambios en la tabla de grupo Empleados
                grupoEmpleadoExists.sociedad_id=grupoEmpleado.sociedad_id,
                grupoEmpleadoExists.es_honorario=grupoEmpleado.es_honorario,
                grupoEmpleadoExists.nombre=((grupoEmpleado.nombre).upper()).strip(),
                grupoEmpleadoExists.updated=ahora,
                grupoEmpleadoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":grupoEmpleadoExists.id,
                    "sociedad_id":grupoEmpleadoExists.sociedad_id,
                    "es_honorario":grupoEmpleadoExists.es_honorario,
                    "nombre":grupoEmpleadoExists.nombre,
                    "created":grupoEmpleadoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":grupoEmpleadoExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":grupoEmpleadoExists.creator_user,
                    "updater_user":grupoEmpleadoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de de la grupoEmpleado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para listar los datos historicos  de una grupoEmpleado
    # @params id: Id de la grupoEmpleado que se esta consultando
    def list_history_grupo_empleados(self, page:int, records: int, id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricoGruposEmpleadoModel).filter(HistoricoGruposEmpleadoModel.grupo_empleados_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la grupoEmpleado
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de la grupoEmpleado
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoGruposEmpleadoModel).filter(HistoricoGruposEmpleadoModel.grupo_empleados_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorygrupoEmpleado=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la grupoEmpleado ","data": listHistorygrupoEmpleado})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     
            
    
    # metodo para consultar todas los grupos de unaa sociedad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_grupos(self, page, records,idSociedad):
        consulta = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)  

            
    #listar los empleados de un grupo por sociedad
            
    #listar los empleados de un grupo por sociedad y sede
            
    #listar los empleados de un grupo por sociedad, sede y departamento          