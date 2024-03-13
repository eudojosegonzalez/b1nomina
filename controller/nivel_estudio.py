'''
Este archivo contiene las funciones básicas del CRUD de Nivel de Estudio en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="NivelEstudio"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    descripcion=Column(VARCHAR(150), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    descripcion : str = Field(min_length=3, max_length=150)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "descripcion":"Universitaria",
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
from models.nivel_estudio import NivelEstudio as NivelEstudioModel
from models.historico_nivel_estudio import HistoricoNivelEstudio as HistoricoNivelEstudioModel

#importamos el esquema de datos de Sede
from schemas.nivel_estudio import NivelEstudio as NivelEstudioSchema



# esto representa los metodos implementados en la tabla
class NivelEstudioController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las Nivel de Estudio
    #@param nivelEstudio: Modelo del registro de Sede
    #@param observavacion: Observación sobre el historico
    def create_historico_nivel_estudio(self, nivelEstudio : NivelEstudioModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoNivelEstudioModel(
                sede_id=nivelEstudio.id,
                sociedad_id=nivelEstudio.sociedad_id,
                nombre=nivelEstudio.descripcion,
                direccion=nivelEstudio.direccion,
                region_id=nivelEstudio.region_id,
                comuna_id=nivelEstudio.comuna_id,
                ciudad=nivelEstudio.ciudad,
                created=nivelEstudio.created,
                updated=nivelEstudio.updated,
                creator_user=nivelEstudio.creator_user,
                updater_user=nivelEstudio.updater_user,
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
    
    
    #metodo para insertar  los datos del Nivel de Estudio
    # @userCreatorId: Id del usuario que está creando el registro
    # @params nivelEstudio: esquema de los datos de  sede  que se desea insertar       
    def create_nivel_estudio(self, nivelEstudio:NivelEstudioSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreSede=nivelEstudio.descripcion.upper().strip()

        # contamos si existe un Nivel de Estudio con el mismo nombre
        nRecordNombre = self.db.query(NivelEstudioModel).filter(NivelEstudioModel.descripcion == nombreSede).count()  


        if (nRecordNombre > 0):
            # buscamos la sede con el nombre y lo devolvemos
            nivelEstudioExists=self.db.query(NivelEstudioModel).filter(NivelEstudioModel.descripcion == nombreSede).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe un Nivel de Estudio con ese nombre","data":nivelEstudioExists})          
        else:    
            #creamos el nuevo registro de Nivel de Estudio
            try:
                newNivelEstudio=NivelEstudioModel(
                    descripcion=((nivelEstudio.descripcion).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId,
                    created=ahora,
                    updated=ahora
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newNivelEstudio)
                self.db.commit()

                #creamos el registro historico de Nivel de Estudio
                NivelEstudioController.create_historico_nivel_estudio(self,newNivelEstudio,"Se creó un Nivel de Estudio en el sistema")
  
                data={
                    "id": newNivelEstudio.id,    
                    "descripcion": newNivelEstudio.descripcion,
                    "created": newNivelEstudio.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newNivelEstudio.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newNivelEstudio.creator_user,
                    "updater_user":newNivelEstudio.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos de un Nivel de Estudio
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_nivel_estudio(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(NivelEstudioModel).filter(NivelEstudioModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta sede
            try:
                nivelEstudioExist = self.db.query(NivelEstudioModel).filter(NivelEstudioModel.id == id).first()                  
                # devolvemos los datos del Nivel de Estudio
                return ({"result":"1","estado":"Se consiguieron los datos del Nivel de Estudio","data":nivelEstudioExist})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    # metodo para efectuar búsquedas en las Nivel de Estudio
    # @params cadena: cadena que se buscara en la tabla Nivel de Estudio comparando con el campo nombre 
    def search_nivel_estudio(self,finding ):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(NivelEstudioModel).filter(NivelEstudioModel.descripcion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(NivelEstudioModel).filter(NivelEstudioModel.descripcion.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    # metodo para actualizar los datos de un Nivel de Estudio por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params nivelEstudio: esquema de los datos del Nivel de Estudio
    # @params id: Iddel Nivel de Estudio que será actualizado
    def update_nivel_estudio(self, nivelEstudio:NivelEstudioSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este sede existe
        nRecord = self.db.query(NivelEstudioModel).filter(NivelEstudioModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del Nivel de Estudio
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                nivelEstudioExists = self.db.query(NivelEstudioModel).filter(NivelEstudioModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_nivel_estudio(nivelEstudioExists ,"Actualización de la data del Nivel de Estudio")

                #registramnos los cambios en la tabla de Nivel de Estudio

                nivelEstudioExists.descripcion=((nivelEstudio.descripcion).upper()).strip(),
                nivelEstudioExists.updated=ahora,
                nivelEstudioExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id": nivelEstudioExists.id,    
                    "descripcion": nivelEstudioExists.descripcion,
                    "created": nivelEstudioExists.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":nivelEstudioExists.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":nivelEstudioExists.creator_user,
                    "updater_user":nivelEstudioExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato del Nivel de Estudio","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las Nivel de Estudio
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_nivel_estudio(self):
        consulta = self.db.query(NivelEstudioModel)
        result=consulta.all()
        return (result)



    # metodo para listar los datos historicos  de un Nivel de Estudio
    # @params id: Iddel Nivel de Estudio que se esta consultando
    def list_history_nivel_estudio(self,  id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoNivelEstudioModel).filter(HistoricoNivelEstudioModel.nivel_estudio_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicosdel Nivel de Estudio
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicosdel Nivel de Estudio
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoNivelEstudioModel).filter(HistoricoNivelEstudioModel.nivel_estudio_id == id)
                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos del Nivel de Estudio ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     