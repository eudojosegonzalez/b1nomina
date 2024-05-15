'''
Este archivo contiene las funciones básicas del CRUD de Tramos de Asignacion Familiar
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="TramosAsignacionFamiliar"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tramo = Column(VARCHAR(50), nullable=False)
    desde = Column(NUMERIC(18,4),nullable= False)
    hasta = Column(NUMERIC(18,4),nullable= False)   
    valor_carga = Column(NUMERIC(18,4),nullable= False)     
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    tramo : str = Field(min_length=3, max_length=250)
    desde :  float
    hasta : float
    valor_carga : float
    
    #'Tramo 1','0.000','13.500','0.000','0.000'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tramo":"A",
                    "desde" : 0.00,
                    "hasta" : 315841.000,
                    "valor_carga": 12364,
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
from models.tramo_asignacion_familiar import TramosAsignacionFamiliar as TramosAsignacionFamiliarModel
from models.historico_tramo_asignacion_familiar import HistoricoTramosAsignacionFamiliar as HistoricoTramosAsignacionFamiliarModel

#importamos el esquema de datos de Sociedades
from schemas.tramos_asignacion_familiar import TramosAsignacionFamiliar as TramosAsignacionFamiliarSchema


# esto representa los metodos implementados en la tabla
class TramoAsignacionFamiliarController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico del Tramo de Asignacion Familiar
    #@param TramosAsignacionFamiliarModel: Modelo del Tramo de Asignacion Familiar
    #@param observavacion: Observación sobre el historico
    def create_historico_tramo_asignacion_familiar(self, tramosAsignacionFamiliar: TramosAsignacionFamiliarModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()
        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoTramoAsignacionFamiliar= HistoricoTramosAsignacionFamiliarModel(
                tramo_asignacion_familiar_id=tramosAsignacionFamiliar.id,
                tramo=tramosAsignacionFamiliar.tramo,
                desde=tramosAsignacionFamiliar.desde,
                hasta=tramosAsignacionFamiliar.hasta,
                valor_carga=tramosAsignacionFamiliar.valor_carga,
                created=tramosAsignacionFamiliar.created,
                updated=tramosAsignacionFamiliar.updated,
                creator_user=tramosAsignacionFamiliar.creator_user,
                updater_user=tramosAsignacionFamiliar.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoTramoAsignacionFamiliar)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del  Tramo de Asignacion Familiar
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  Tramo de Asignacion Familiar  que se desea insertar       
    def create_tramo_asignacion_familiar(self, tramoAsignacionFamiliar:TramosAsignacionFamiliarSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreTramo=tramoAsignacionFamiliar.tramo.upper().strip()

        # contamos si existe un Tramo de Asignacion Familiar con el mismo tramo
        nRecordNombre = self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.tramo == nombreTramo).count()  


        if (nRecordNombre > 0):
            # buscamos el Tramo de Asignacion Familiar con el nombre y lo devolvemos
            tramoAsignacionExists=self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.tramo == nombreTramo).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe un Tramo de Asignacion Familiar con ese tramo","data":tramoAsignacionExists})          
        else:    
            #creamos el nuevo registro de Tramo de Asignacion Familiar
            try:
                newTramoImpuestoUnico=TramosAsignacionFamiliarModel(
                    tramo=((tramoAsignacionFamiliar.tramo).upper()).strip(),
                    desde=tramoAsignacionFamiliar.desde,
                    hasta=tramoAsignacionFamiliar.hasta,                    
                    valor_carga=tramoAsignacionFamiliar.valor_carga,                                     
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newTramoImpuestoUnico)
                self.db.commit()

                #creamos el registro historico de Tramo de Asignacion Familiar
                self.create_historico_tramo_asignacion_familiar(newTramoImpuestoUnico,"Se creó un Tramo de Asignacion Familiar en el sistema")
  
                data={
                    "id":newTramoImpuestoUnico.id,
                    "tramo": newTramoImpuestoUnico.tramo,
                    "desde": newTramoImpuestoUnico.desde,
                    "hasta": newTramoImpuestoUnico.hasta,
                    "valor_carga": newTramoImpuestoUnico.valor_carga,
                     "created": newTramoImpuestoUnico.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newTramoImpuestoUnico.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newTramoImpuestoUnico.creator_user,
                    "updater_user":newTramoImpuestoUnico.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un Tramo de Asignacion Familiar
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_tramo_asignacion_familiar(self,id:int):

        # buscamos si este existe este Tramo de Asignacion Familiar
        nRecord = self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este Tramo de Asignacion Familiar
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de este Tramo de Asignacion Familiar
            try:
                sedeExits = self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.id == id).first()                  
                # devolvemos los datos del  Tramo de Asignacion Familiar
                return ({"result":"1","estado":"Se consiguieron los datos del tramo de impuesto único","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los Tramos de Impuesto Único
    # @params cadena: cadena que se buscara en la tabla de Tramos de Impuesto Único comparando con el campo tramo
    def search_tramo_asignacion_familiar(self,finding):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay registros coincidentes
            nRecord=self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.tramo.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.tramo.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de un Tramo de Asignacion Familiar por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params  tramoAsignacionFamiliar: esquema de los datos del  Tramo de Asignacion Familiar
    # @params id: Id de la sede que será actualizado
    def update_tramo_asignacion_familiar(self, tramoAsignacionFamiliar:TramosAsignacionFamiliarSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del  Tramo de Asignacion Familiar
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                tramoAsignacionExists = self.db.query(TramosAsignacionFamiliarModel).filter(TramosAsignacionFamiliarModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_tramo_asignacion_familiar(tramoAsignacionExists ,"Actualización de la data del Tramo de Impueto Único")

                #registramnos los cambios en la tabla de sedes
                tramoAsignacionExists.tramo=((tramoAsignacionFamiliar.tramo).upper()).strip(),
                tramoAsignacionExists.desde=tramoAsignacionFamiliar.desde,
                tramoAsignacionExists.hasta=tramoAsignacionFamiliar.hasta,
                tramoAsignacionExists.valor_carga=tramoAsignacionFamiliar.valor_carga,
                tramoAsignacionExists.updated=ahora,
                tramoAsignacionExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":tramoAsignacionExists.id,
                    "tramo":tramoAsignacionExists.tramo,
                    "desde": tramoAsignacionExists.desde,
                    "hasta": tramoAsignacionExists.hasta,
                    "valor_carga": tramoAsignacionExists.valor_carga,                   
                    "created":tramoAsignacionExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":tramoAsignacionExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":tramoAsignacionExists.creator_user,
                    "updater_user":tramoAsignacionExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato del Tramo de Asignacion Familiar","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_tramo_asignacion_familiar(self):
        consulta = self.db.query(TramosAsignacionFamiliarModel)
        result=consulta.all()
        return (result)




    # metodo para listar los datos historicos  de un tramo
    # @params id: Id de la sociedad que se esta consultando
    def list_history_tramo_asignacion_familiar(self, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoTramosAsignacionFamiliarModel).filter(HistoricoTramosAsignacionFamiliarModel.tramo_asignacion_familiar_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del tramo
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoTramosAsignacionFamiliarModel).filter(HistoricoTramosAsignacionFamiliarModel.tramo_asignacion_familiar_id == id)
                listHistoryTramoasignacionFamiliar=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos del Tramo de Asignacion Familiar","data": listHistoryTramoasignacionFamiliar})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     