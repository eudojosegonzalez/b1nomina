'''
Este archivo contiene las funciones básicas del CRUD de Unidades de Pacto
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(VARCHAR(150), nullable=False)
    estado= Column(BOOLEAN, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    descripcion : str = Field(min_length=1, max_length=150),
    estado : bool 


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "descripcion":"UF",
                    "estado": True
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
from models.unidad_pacto import UnidadesPacto as UnidadesPactoModel
from models.historico_unidad_pacto import HistoricoUnidadesPacto as HistoricoUnidadesPactoModel


# importamos el schema de datos
from models.unidad_pacto import UnidadesPacto as UnidadesPactoSchema


# esto representa los metodos implementados en la tabla
class UnidadesPactoController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de Unidades de Pacto
    #@param unidadPacto: Modelo del registro de Unidades de Pacto
    #@param observavacion: Observación sobre el historico
    def create_historico_unidades_pacto (self, unidadPacto: UnidadesPactoModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()


        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoUnidaesPacto= HistoricoUnidadesPactoModel(
                
                unidades_id = unidadPacto.id,
                descripcion = unidadPacto.descripcion,
                estado = unidadPacto.estado,
                created = unidadPacto.created,
                updated = unidadPacto.updated,
                creator_user= unidadPacto.creator_user,
                updater_user = unidadPacto.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoUnidaesPacto)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la unidad de pacto 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params banco: esquema de los datos banco que se desea insertar       
    def create_unidad_pacto(self, unidadPacto:UnidadesPactoSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreUnidadPacto=unidadPacto.descripcion.upper().strip()


        # contamos si existe un banco con el mismo nombre
        nRecordNombre = self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.descripcion == nombreUnidadPacto).count()  

        if (nRecordNombre > 0):
            # buscamos el banco con el nombre y lo devolvemos
            unidadPactoExists=self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.descripcion == nombreUnidadPacto).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-1","estado":"Existe una Unidad de Pacto con ese nombre","data":unidadPactoExists})
        
        else:    
            #creamos el nuevo registro de banco
            try:
                newUnidadPacto=UnidadesPactoModel(
                    descripcion=((unidadPacto.descripcion).upper()).strip(),
                    estado=unidadPacto.estado,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newUnidadPacto)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_unidades_pacto(newUnidadPacto,"Se creó una unidad de pacto en el sistema")
  
                data={
                    "id":newUnidadPacto.id,
                    "desripcion": newUnidadPacto.descripcion,
                    "estado":newUnidadPacto.estado,
                    "created": newUnidadPacto.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newUnidadPacto.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newUnidadPacto.creator_user,
                    "updater_user":newUnidadPacto.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una unidad de pacto por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_unidad_pacto(self,id:int):

        # buscamos los datos de la unidad de pacto
        nRecord = self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta unidad de pacto
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                unidadPactoExits = self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.id == id).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de la unidad de pacto","data":unidadPactoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las unidades de pacto
    # @params cadena: cadena que se buscara en la tabla banco comparando con el campo nombre y codigo      
    def search_unidad_pacto(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.descripcion.like(findingT) ).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.descripcion.like(findingT) )
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de una unidad de pacto por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params unidadPacto: esquema de los datos de la unidad de pacto
    # @params id: Id del de la unidad de pacto que se esta actualizando
    def update_unidad_pacto(self, unidadPacto:UnidadesPactoSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este la unidad de pacto existe
        nRecord = self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos  de la unidad de pacto
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                unidadPactoExists = self.db.query(UnidadesPactoModel).filter(UnidadesPactoModel.id == id).first()             

                #creamos el registro historico de unidades de pacto
                self.create_historico_unidades_pacto(unidadPactoExists ,"Actualización de la data del de la unidad de pacto")

                #registramnos los cambios en la tabla de unidades de pacto
                estadoV=0

                if (str(unidadPacto.estado).upper()=="TRUE"):
                    estadoV=1

                #return ({"result":"1","estado":"Se actualizó la data de la unidad de Pacto","data":str(estadoV)})

                unidadPactoExists.descripcion=((unidadPacto.descripcion).upper()).strip(),
                unidadPactoExists.estado=estadoV,
                unidadPactoExists.updated=ahora,
                unidadPactoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":unidadPactoExists.id,
                    "descripcion":unidadPactoExists.descripcion,
                    "estado":unidadPactoExists.estado,
                    "created":unidadPactoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":unidadPactoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":unidadPactoExists.creator_user,
                    "updater_user":unidadPactoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó la data de la unidad de Pacto","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todos las unidades de pacto
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_unidades_pacto(self, page, records):
        consulta = self.db.query(UnidadesPactoModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos de una unidad de pacto
    # @params id: Id de la unidad de pacto que se esta consultando
    def list_history_unidad_pacto(self, page:int, records: int, id:int):

        # buscamos si exite la unidad de pacto
        nRecord = self.db.query(HistoricoUnidadesPactoModel).filter(HistoricoUnidadesPactoModel.unidades_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la unidad de pacto
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de la unidad de pacto
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoUnidadesPactoModel).filter(HistoricoUnidadesPactoModel.unidades_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistoryBancos=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la unidad de pacto ","data": listHistoryBancos})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     