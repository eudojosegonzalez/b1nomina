'''
Este archivo contiene las funciones básicas del CRUD de Tramos de Impuesto Único
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="TramosImpuestoUnico"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tramo = Column(VARCHAR(50), nullable=False)
    desde = Column(NUMERIC(18,4),nullable= False)
    hasta = Column(NUMERIC(18,4),nullable= False)   
    facto = Column(NUMERIC(13,4),nullable= False)     
    rebaja = Column(NUMERIC(13,4),nullable= False)
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
    factor : float
    rebaja : float
    
    #'Tramo 1','0.000','13.500','0.000','0.000'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre":"Tramo 1",
                    "desde" : 0.00,
                    "hasta" : 13.50,
                    "factor": 0.00,
                    "rebaja": 0.00
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
from models.tramo_impuesto_unico import TramosImpuestoUnico as TramosImpuestoUnicoModel
from models.historico_tramo_impuesto_unico import HistoricoTramosImpuestoUnico as HistoricoTramosImpuestoUnicoModel

#importamos el esquema de datos de Sociedades
from schemas.tramos_impuesto_unico import TramosImpuestoUnico as TramosImpuestoUnicoSchema


# esto representa los metodos implementados en la tabla
class TramosImpuestoUnicoController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico del Tramo de Impuesto Único
    #@param TramosImpuestoUnicoModel: Modelo del Tramo de Impuesto Único
    #@param observavacion: Observación sobre el historico
    def create_historico_tramo_impuesto_unico(self, tramosImpuesto: TramosImpuestoUnicoModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()
        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoTramosImpuesoUnico= HistoricoTramosImpuestoUnicoModel(
                tramo_impuesto_id=tramosImpuesto.id,
                tramo=tramosImpuesto.tramo,
                desde=tramosImpuesto.desde,
                hasta=tramosImpuesto.hasta,
                factor=tramosImpuesto.factor,
                rebaja=tramosImpuesto.rebaja,
                created=tramosImpuesto.created,
                updated=tramosImpuesto.updated,
                creator_user=tramosImpuesto.creator_user,
                updater_user=tramosImpuesto.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoTramosImpuesoUnico)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del  Tramo de Impuesto Único
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  Tramo de Impuesto Único  que se desea insertar       
    def create_tramo_impuesto_unico(self, tramoImpuestoUnico:TramosImpuestoUnicoSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreTramo=tramoImpuestoUnico.tramo.upper().strip()

        # contamos si existe un Tramo de Impuesto Único con el mismo tramo
        nRecordNombre = self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.tramo == nombreTramo).count()  


        if (nRecordNombre > 0):
            # buscamos el Tramo de Impuesto Único con el nombre y lo devolvemos
            tramoImpuestoExists=self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.tramo == nombreTramo).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe un Tramo de Impuesto Único con ese tramo","data":tramoImpuestoExists})          
        else:    
            #creamos el nuevo registro de Tramo de Impuesto Único
            try:
                newTramoImpuestoUnico=TramosImpuestoUnicoModel(
                    tramo=((tramoImpuestoUnico.tramo).upper()).strip(),
                    desde=tramoImpuestoUnico.desde,
                    hasta=tramoImpuestoUnico.hasta,                    
                    factor=tramoImpuestoUnico.factor,                    
                    rebaja=tramoImpuestoUnico.rebaja,                    
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newTramoImpuestoUnico)
                self.db.commit()

                #creamos el registro historico de Tramo de Impuesto Único
                self.create_historico_tramo_impuesto_unico(newTramoImpuestoUnico,"Se creó un Tramo de Impuesto Único en el sistema")
  
                data={
                    "id":newTramoImpuestoUnico.id,
                    "tramo": newTramoImpuestoUnico.tramo,
                    "desde": newTramoImpuestoUnico.desde,
                    "hasta": newTramoImpuestoUnico.hasta,
                    "factor": newTramoImpuestoUnico.factor,
                    "rebaja": newTramoImpuestoUnico.rebaja,
                     "created": newTramoImpuestoUnico.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newTramoImpuestoUnico.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newTramoImpuestoUnico.creator_user,
                    "updater_user":newTramoImpuestoUnico.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un Tramo de Impuesto Único
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_tramo_impuesto_unico(self,id:int):

        # buscamos si este existe este Tramo de Impuesto Único
        nRecord = self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este Tramo de Impuesto Único
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de este Tramo de Impuesto Único
            try:
                sedeExits = self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.id == id).first()                  
                # devolvemos los datos del  Tramo de Impuesto Único
                return ({"result":"1","estado":"Se consiguieron los datos del tramo de impuesto único","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los Tramos de Impuesto Único
    # @params cadena: cadena que se buscara en la tabla de Tramos de Impuesto Único comparando con el campo tramo
    def search_tramo_impuesto_unico(self,finding):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay registros coincidentes
            nRecord=self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.tramo.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.tramo.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de un Tramo de Impuesto Único por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params  tramoImpuestoUnico: esquema de los datos del  Tramo de Impuesto Único
    # @params id: Id de la sede que será actualizado
    def update_tramo_impuesto_unico(self, tramoImpuestoUnico:TramosImpuestoUnicoSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del  Tramo de Impuesto Único
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                tramoImpuestoExists = self.db.query(TramosImpuestoUnicoModel).filter(TramosImpuestoUnicoModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_tramo_impuesto_unico(tramoImpuestoExists ,"Actualización de la data del Tramo de Impueto Único")

                #registramnos los cambios en la tabla de sedes
                tramoImpuestoExists.tramo=((tramoImpuestoUnico.tramo).upper()).strip(),
                tramoImpuestoExists.desde=tramoImpuestoUnico.desde,
                tramoImpuestoExists.hasta=tramoImpuestoUnico.hasta,
                tramoImpuestoExists.factor=tramoImpuestoUnico.factor,
                tramoImpuestoExists.rebaja=tramoImpuestoUnico.rebaja,
                tramoImpuestoExists.updated=ahora,
                tramoImpuestoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":tramoImpuestoExists.id,
                    "tramo":tramoImpuestoExists.tramo,
                    "desde": tramoImpuestoExists.desde,
                    "hasta": tramoImpuestoExists.hasta,
                    "factor": tramoImpuestoExists.factor,
                    "rebaja": tramoImpuestoExists.rebaja,                    
                    "created":tramoImpuestoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":tramoImpuestoExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":tramoImpuestoExists.creator_user,
                    "updater_user":tramoImpuestoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato del Tramo de Impuesto Único","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_tramo_impuesto_unico(self):
        consulta = self.db.query(TramosImpuestoUnicoModel)
        result=consulta.all()
        return (result)




    # metodo para listar los datos historicos  de un tramo
    # @params id: Id de la sociedad que se esta consultando
    def list_history_tramo_impuesto_unico(self, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoTramosImpuestoUnicoModel).filter(HistoricoTramosImpuestoUnicoModel.tramo_impuesto_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del tramo
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoTramosImpuestoUnicoModel).filter(HistoricoTramosImpuestoUnicoModel.tramo_impuesto_id == id)
                listHistoryTRamoImpuestoUnico=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos del Tramo de Impuesto Único","data": listHistoryTRamoImpuestoUnico})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     