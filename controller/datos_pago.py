'''
Este archivo contiene las funciones básicas del CRUD de Datos Laborales en el sistema
Created 2024-02
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="DatosPago"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)            
    medio = Column(INTEGER, nullable=False)
    banco_id = Column(BIGINT,  nullable=True)
    tipo_cuenta = Column(INTEGER, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    user_id : int = Field(ge=1, le=20000)
    medio : int 
    banco_id : int 
    tipo_cuenta : int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "medio":1,
                    "banco_id":1,
                    "tipo_cuenta":1
                }
            ]
        }
    } 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "sede_id": 1,                    
                    "departamento_id": 1,                    
                    "grupo_id":0,
                    "cargo_id":1,
                    "user_id":1,
                    "tipo_contrato":1,
                    "termino_contrato":1,
                    "fecha_inicio":'2024-01-01',
                     "fecha_fin":'',
                    "periodo_salario":30,
                    "modalidad":0,
                    "dias_descanso":"1"
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
from models.datos_pago import DatosPago as DatosPagoModel
from models.historico_datos_pago import HistoricoDatosPago as HistoricoDatosPagoModel

#importamos el esquema de datos de Datos Laborales
from schemas.datos_pago import DatosPago as DatosPagoSchema


# esto representa los metodos implementados en la tabla
class DatosPagoController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico los Datos de Pago
    #@param datosLaborales: Modelo del registro de Datos Laborales
    #@param observavacion: Observación sobre el historico
    def create_historico_datos_pago(self, datosPago: DatosPagoModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoDatosPagoModel(
                datos_pago_id=datosPago.id,
                user_id=datosPago.user_id,
                medio=datosPago.medio,
                banco_id=datosPago.banco_id,                
                tipo_cuenta=datosPago.tipo_cuenta, 
                numero_cuenta=datosPago.numero_cuenta,               
                created=datosPago.created,
                updated=datosPago.updated,
                creator_user=datosPago.creator_user,
                updater_user=datosPago.updater_user,
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
    
    
    #metodo para insertar  los datos de pago es
    # @userCreatorId: Id del usuario que está creando el registro
    # @params datosLaborales: esquema de los datos de pago es  que se desea insertar       
    def create_datos_pago(self, datosPago:DatosPagoSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        userId=datosPago.user_id        

        # verificamos que el usuario no tenga datos de pago es previos
        nRecordDatosLaborales=  self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id == userId).count()

        if (nRecordDatosLaborales > 0):

            datoLaboralExists = self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id == userId).first()
            return ({"result":"-1","estado":"Este usuario ya tiene datos de pago es no puede volver a crearlo","data": datoLaboralExists})     
                
        else:
            #creamos el nuevo registro de Datos Laborales
            try:
                newDatosPago=DatosPagoModel(
               
                    user_id=datosPago.user_id,
                    medio=datosPago.medio,
                    banco_id=datosPago.banco_id,                
                    tipo_cuenta=datosPago.tipo_cuenta,
                    numero_cuenta=datosPago.numero_cuenta,                
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newDatosPago)
                self.db.commit()

                #creamos el registro historico de los datos de pago es
                DatosPagoController.create_historico_datos_pago(self,newDatosPago,"Se creó un Dato de pago en el sistema")

                data={
                    "id":newDatosPago.id,
                    "user_id":newDatosPago.user_id,
                    "medio":newDatosPago.medio,
                    "banco_id":newDatosPago.banco_id,
                    "tipo_cuenta":newDatosPago.tipo_cuenta,
                    "numero_cuenta":newDatosPago.numero_cuenta,
                    "created": newDatosPago.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newDatosPago.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newDatosPago.creator_user,
                    "updater_user":newDatosPago.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos Laborales por ID
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_datos_pago(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosPagoModel).filter(DatosPagoModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de pago es
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de pago es
            try:
                datosPagoExists = self.db.query(DatosPagoModel).filter(DatosPagoModel.id == id).first()                  
                # devolvemos los datos de la sede
                return ({"result":"1","estado":"Se consiguieron los Datos de Pago","data":datosPagoExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para consultar los datos Laborales por user_id
    def get_datos_pago_userid(self,userId:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos de pago es de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de pago es de este usuario
            try:
                DatosLaboralesExits = self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id == userId).first()                  
                # devolvemos los datos de pago es
                return ({"result":"1","estado":"Se consiguieron los Datos de Pago","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})    
             
            
    # metodo para consultar todas los Datos de Pago
    def list_datos_pago(self):
        consulta = self.db.query(DatosPagoModel)
        result=consulta.all()
        return (result)


    #metodo para actualizar los datos de pago es por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params datosPago: esquema de los datos de pago es que se estan actualizando
    # @params id: Id de los datos de pago es que será actualizado
    def update_datos_pago(self, datosPago:DatosPagoSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este dato de pago  existe
        nRecord = self.db.query(DatosPagoModel).filter(DatosPagoModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de pago es
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                datosPagoExists = self.db.query(DatosPagoModel).filter(DatosPagoModel.id == id).first()             

                #creamos el registro historico de datos de pago 
                self.create_historico_datos_pago(datosPagoExists ,"Actualización de Dato de Pago")

                #registramos los cambios en la tabla de datos de pago 
                datosPagoExists.user_id=datosPago.user_id,                
                datosPagoExists.medio=datosPago.medio,
                datosPagoExists.banco_id=datosPago.banco_id,                
                datosPagoExists.tipo_cuenta=datosPago.tipo_cuenta,  
                datosPagoExists.numero_cuenta=datosPago.numero_cuenta,  
                datosPagoExists.updated=ahora,
                datosPagoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":datosPagoExists.id,
                    "user_id":datosPagoExists.user_id,          
                    "medio":datosPagoExists.medio,
                    "banco_id":datosPagoExists.banco_id,
                    "tipo_cuenta":datosPagoExists.tipo_cuenta,                              
                    "numero_cuenta":datosPagoExists.numero_cuenta,  
                    "created":datosPagoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":datosPagoExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":datosPagoExists.creator_user,
                    "updater_user":datosPagoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el Dato de Pago","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para listar los datos historicos  de Dato de Pago
    # @params id: Id del dato de pago que se esta consultando
    def list_history_datos_pago(self,  id:int):

        # buscamos si exite el dato de pago en el historico
        nRecord = self.db.query(HistoricoDatosPagoModel).filter(HistoricoDatosPagoModel.datos_pago_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del dato laboral
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del dato de pago
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoDatosPagoModel).filter(HistoricoDatosPagoModel.datos_pago_id == id)
                listHistoryDatosLaborales=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos del Dato de Pago ","data": listHistoryDatosLaborales})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     