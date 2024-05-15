'''
Este archivo contiene las funciones básicas del CRUD de Centralizaciones del Sistema
Created 2024-03
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Centralizaciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    usa_centros_costos= Column(INTEGER,   nullable=False)
    cuenta_anticipo= Column(VARCHAR(50), nullable=True)
    cuenta_bonos_feriado= Column(VARCHAR(50), nullable=True)
    cuenta_honoraios= Column(VARCHAR(50), nullable=True)
    cuenta_prestamos_solidarios= Column(VARCHAR(50), nullable=True)
    restamo_solidario_imponible= Column(INTEGER,   nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=2000)
    usa_centros_costos : int = Field(ge=0, le=1)
    cuenta_anticipo : str =Field (min_length=0, max_length=50)
    cuenta_bonos_feriado : str =Field (min_length=0, max_length=50)
    cuenta_honorarios : str =Field (min_length=0, max_length=50)
    cuenta_prestamos_solidarios : str =Field (min_length=0, max_length=50)
    prestamo_solidario_imponible  : int = Field(ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id" : 1,
                    "usa_centros_costos" : 1,
                    "cuenta_anticipo" : "",
                    "cuenta_bonos_feriado" : "",
                    "cuenta_honoraios" : "",
                    "cuenta_prestamos_solidarios" : "",
                    "prestamo_solidario_imponible"  : 1
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
from models.centralizaciones import Centralizaciones as CentralizacionesModel
from models.historico_centralizaciones import HistoricoCentralizaciones as HistoricoCentralizacionesModel


# importamos el schema de datos
from schemas.centralizaciones import Centralizaciones as CentralizacionesSchema

# esto representa los metodos implementados en la tabla
class CentralizacionesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de centralizacion
    #@param centralizacion: Modelo del registro de centralizacion
    #@param observavacion: Observación sobre el historico
    def create_historico_centralizaciones (self, centralizacion: CentralizacionesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoBanco= HistoricoCentralizacionesModel(
                centralizaciones_id= centralizacion.id,
                sociedad_id=centralizacion.sociedad_id,
                usa_centros_costos=centralizacion.usa_centros_costos,
                cuenta_anticipo=centralizacion.cuenta_anticipo,
                cuenta_bonos_feriado=centralizacion.cuenta_bonos_feriado,
                cuenta_honorarios=centralizacion.cuenta_honorarios,
                cuenta_prestamos_solidarios=centralizacion.cuenta_prestamos_solidarios,
                prestamo_solidario_imponible=centralizacion.prestamo_solidario_imponible,
                created = centralizacion.created,
                updated = centralizacion.updated,
                creator_user= centralizacion.creator_user,
                updater_user = centralizacion.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoBanco)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de centralizacion 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params banco: esquema de los datos banco que se desea insertar       
    def create_centralizacion(self, centralizacion:CentralizacionesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        sociedadId=centralizacion.sociedad_id

        # contamos si existe una centralizacion para esta sociedad
        nRecordNombre = self.db.query(CentralizacionesModel).filter(CentralizacionesModel.sociedad_id == sociedadId).count()  
    

        if (nRecordNombre > 0):
            # buscamos el banco con el nombre y lo devolvemos
            centralizacionExists=self.db.query(CentralizacionesModel).filter(CentralizacionesModel.sociedad_id == sociedadId).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-1","estado":"Existe una centralizacion para esta sociedad","data":centralizacionExists})
              
        else:    
            #creamos el nuevo registro de centralizacion
            try:
                newCentralizacion=CentralizacionesModel(
                    sociedad_id=centralizacion.sociedad_id,
                    usa_centros_costos=centralizacion.usa_centros_costos,
                    cuenta_anticipo=centralizacion.cuenta_anticipo,
                    cuenta_bonos_feriado=centralizacion.cuenta_bonos_feriado,
                    cuenta_honorarios=centralizacion.cuenta_honorarios,
                    cuenta_prestamos_solidarios=centralizacion.cuenta_prestamos_solidarios,
                    prestamo_solidario_imponible=centralizacion.prestamo_solidario_imponible,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newCentralizacion)
                self.db.commit()

                #creamos el registro historico de centralizaciones de la socidad
                self.create_historico_centralizaciones(newCentralizacion,"Se creó una centralizacion en el sistema")
  
                data={
                    "id":newCentralizacion.id,
                    "sociedad_id":newCentralizacion.sociedad_id,
                    "usa_centros_costos":newCentralizacion.usa_centros_costos,
                    "cuenta_anticipo":newCentralizacion.cuenta_anticipo,
                    "cuenta_bonos_feriado":newCentralizacion.cuenta_bonos_feriado,
                    "cuenta_honorarios":newCentralizacion.cuenta_honorarios,
                    "cuenta_prestamos_solidarios":newCentralizacion.cuenta_prestamos_solidarios,
                    "prestamo_solidario_imponible":newCentralizacion.prestamo_solidario_imponible,
                    "created":newCentralizacion.created,
                    "updated":newCentralizacion.updated,
                    "creator_user" : newCentralizacion.creator_user,
                    "updater_user":newCentralizacion.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de centralizacion por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_centralizacion(self,id:int):

        # buscamos los datos bancarios
        nRecord = self.db.query(CentralizacionesModel).filter(CentralizacionesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta centralizacion
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                bancoExits = self.db.query(CentralizacionesModel).filter(CentralizacionesModel.id == id).first()                  

                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de centralizacion","data":bancoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
 
            
 
    #metodo para actualizar los datos de centralizacion por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params centralizacion: esquema de los datos de centralizacion  
    # @params id: Id de centralizacion que será actualizado
    def update_centralizacion(self, centralizacion:CentralizacionesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(CentralizacionesModel).filter(CentralizacionesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de centralizacion
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                centralizacionExists = self.db.query(CentralizacionesModel).filter(CentralizacionesModel.id == id).first()             

                #creamos el registro historico de bancos
                CentralizacionesController.create_historico_centralizaciones(self,centralizacionExists ,"Actualización de la data de centralizacion")

                #registramnos los cambios en la tabla de bancarios del usuario
                centralizacionExists.usa_centros_costos=centralizacion.usa_centros_costos,
                centralizacionExists.cuenta_anticipo=centralizacion.cuenta_anticipo,
                centralizacionExists.cuenta_bonos_feriado=centralizacion.cuenta_bonos_feriado,
                centralizacionExists.cuenta_honorarios=centralizacion.cuenta_honorarios,
                centralizacionExists.cuenta_prestamos_solidarios=centralizacion.cuenta_prestamos_solidarios,
                centralizacionExists.prestamo_solidario_imponible=centralizacion.prestamo_solidario_imponible
                centralizacionExists.updated=ahora,
                centralizacionExists.updater_user=userUpdaterId               


                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":centralizacionExists.id,
                    "sociedad_id":centralizacionExists.sociedad_id,
                    "usa_centros_costos":centralizacionExists.usa_centros_costos,
                    "cuenta_anticipo":centralizacionExists.cuenta_anticipo,
                    "cuenta_bonos_feriado":centralizacionExists.cuenta_bonos_feriado,
                    "cuenta_honorarios":centralizacionExists.cuenta_honorarios,
                    "cuenta_prestamos_solidarios":centralizacionExists.cuenta_prestamos_solidarios,
                    "prestamo_solidario_imponible":centralizacionExists.prestamo_solidario_imponible,
                    "created":centralizacionExists.created,
                    "updated":centralizacionExists.updated,
                    "creator_user" : centralizacionExists.creator_user,
                    "updater_user":centralizacionExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó la data del Banco","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    



    # metodo para listar los datos historicos de un banco
    # @params id: Id de centralizacion que se esta consultando
    def list_history_centralizaciones(self, id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricoCentralizacionesModel).filter(HistoricoCentralizacionesModel.sociedad_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de centralizacion
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de centralizacion
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCentralizacionesModel).filter(HistoricoCentralizacionesModel.sociedad_id == id)
                listHistoryCentralizaciones=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos de centralizacion ","data": listHistoryCentralizaciones})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     