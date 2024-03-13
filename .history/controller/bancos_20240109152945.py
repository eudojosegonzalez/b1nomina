'''
Este archivo contiene las funciones básicas del CRUD de Bancos del Sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    codigo = Column(VARCHAR(50), nullable=False, unique=True)
    nombre = Column(VARCHAR(150), nullable=False)
    nomina = Column(BOOLEAN, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    codigo : str = Field(min_length=3, max_length=50),
    nombre : str = Field(min_length=3, max_length=150),
    nomina : int 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo": "001",
                    "nombre":"BANCO CHILE Y EDWARDS",
                    "nomina": 1
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
from models.bancos import Bancos as BancosModel
from models.historico_bancos import HistoricoBancos as HistoricoBancosModel


# importamos el schema de datos
from schemas.bancos import Bancos as BancosSchema


# esto representa los metodos implementados en la tabla
class bancariosUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de bancos
    #@param historicoBancarioUser: Modelo del registro de Bancarios del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_bancos (self, banco: BancosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoBanco= HistoricoBancosModel(
                
                banco_id = banco.id,
                codigo = banco.codigo,
                nombre = banco.nombre,
                nomina = banco.nomina,
                created = banco.created,
                updated = banco.updated,
                creator_user= banco.creator_user,
                updater_user = banco.updater_user,
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
    
    
    #metodo para insertar  los datos del banco 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_bancario_user(self, banco:BancosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        #creamos el nuevo registro de banco
        try:
            newBanco=BancosModel(
                codigo=banco.codigo,
                nombre=banco.nombre,
                nomina=banco.nomina,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )

            #confirmamos el cambio en la Base de Datos
            self.db.add(newBanco)
            self.db.commit()

            #creamos el registro historico de bancarios del usuario
            #self.create_historico_bancario_user(newBancarioUser,"Se creó la data de contacto del usuario")

            newBancoId=newBanco.id
            return ({"result":"1","estado":"creado","newBancoId":newBancoId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    

    #metodo para consultar los datos de contacto del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def get_bancario_user(self,userId:int):

        # buscamos si este usuario ya tiene datos bancarios
        nRecord = self.db.query(BancariosUserModel).filter(BancariosUserModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos bancarios del usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                bancariosUserExits = self.db.query(BancariosUserModel).filter(BancariosUserModel.user_id == userId).first()                  
                '''contactUser={
                    "id": userContactExists.id,
                    "user_id": userContactExists.user_id,
                    "email": userContactExists.email,
                    "fijo": userContactExists.fijo,
                    "movil": userContactExists.movil,
                    "created": userContactExists.created.strftime("%Y-%m-%d %H:%M:%S"),   
                    "updated": userContactExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user" : userContactExists.creator_user,   
                    "updater_user" : userContactExists.updater_user
                }'''
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de contacto del usuario","data":bancariosUserExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
    #metodo para actualizar los datos de contacto del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def update_bancario_user(self,userUpdaterId:int ,bancarioUsuario:BancariosUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        bancarioId=bancarioUsuario.id

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(BancariosUserModel).filter(BancariosUserModel.id == bancarioId).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos bancarios del usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos baancarios del usuario, se procede a actualizar
            try:
                #extraemos los datos para guardar el histórico
                bancarioUserExists = self.db.query(BancariosUserModel).filter(BancariosUserModel.id == bancarioId).first()                  

                #creamos el registro historico de bancarios del usuario
                self.create_historico_contact_user(bancarioUserExists ,"Actualización de la data de contacto del usuario")
   
                #registramnos los cambios en la tabla de bancarios del usuario
                bancarioUserExists.user_id=bancarioUsuario.user_id,   
                bancarioUserExists.banco_id=bancarioUsuario.banco_id,
                bancarioUserExists.numero_cuenta=bancarioUsuario.numero_cuenta,
                bancarioUserExists.en_uso =bancarioUsuario.en_uso,
                bancarioUserExists.terceros = bancarioUsuario.terceros ,
                bancarioUserExists.rut_tercero = bancarioUsuario.terceros ,
                bancarioUserExists.nombre_tercero= bancarioUsuario.nombre_tercero ,
                bancarioUserExists.email_tercero = bancarioUsuario.email_tercero,
                bancarioUserExists.updated=ahora,
                bancarioUserExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de contacto del usuario","data":bancarioUserExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
        

    # metodo para listar los datos historicos de contacto del usuario
    # @params userId:: Id del usuario que se esta consultando
    def list_history_bancario_user(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(HistoricoBancariosUserModel).filter(HistoricoBancariosUserModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                listHistoryBancariosUser = self.db.query(HistoricoBancariosUserModel).filter(HistoricoBancariosUserModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos de contacto del usuario","data": listHistoryBancariosUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     