'''
Este archivo contiene las funciones básicas del CRUD de Bancarios del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) DEFAULT NULL,
    `banco_id` bigint(20) NOT NULL,
    `numero_cuenta` varchar(100) NOT NULL,
    `en_uso` tinyint(1) NOT NULL,
    `terceros` tinyint(1) NOT NULL,
    `rut_tercero` varchar(100) DEFAULT NULL,
    `nombre_tercero` varchar(100) DEFAULT NULL,
    `email_tercero` varchar(250) DEFAULT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    `creator_user` bigint(20) NOT NULL,
    `updater_user` bigint(20) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `FK_Usuario_BancariosUsuario` (`user_id`),
    KEY `FK_Bancos_BancariosUsuario` (`banco_id`),
    CONSTRAINT `FK_Bancos_BancariosUsuario` FOREIGN KEY (`banco_id`) REFERENCES `Bancos` (`id`) ON UPDATE CASCADE,
    CONSTRAINT `FK_Usuario_BancariosUsuario` FOREIGN KEY (`user_id`) REFERENCES `Usuario` (`id`) ON UPDATE CASCADE

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    user_id: int = Field (ge=1,lt=20000)
    banco_id : int = Field(gr=1, lt=100)
    numero_cuenta : str = Field (min_length=3, max_length=100)
    en_uso : int
    terceros : int
    rut_tercero : str = Field (max_length=100)
    nombre_tercero: str = Field (max_length=100)
    email_tercero  : str = Field (max_length=250)
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime


# importamos el modelo de la base de datos
from models.bancarios_usuarios import BancariosUser as BancariosUserModel
from models.historico_bancarios_usuarios import HistoricoBancariosUser as HistoricoBancariosUserModel
#importamos laa vista ue permite consultar todos los datos bancarios de todos los usuarios
from models.view_general_bancarios_user import ViewGeneralBancariosUser  as ViewGeneralBancariosUserModel


# importamos el schema de datos
from schemas.bancarios_user import BancarioUser as BancariosUserSchema


# esto representa los metodos implementados en la tabla
class bancariosUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de datos bancarios del usuario
    #@param historicoBancarioUser: Modelo del registro de Bancarios del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_bancario_user (self, bancarioUser: BancariosUserModel, observacion:str):
     # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:

            #creamos la instancia la nuevo registro del historico
            newHistoricoBancarioUser= HistoricoBancariosUserModel(
                bancario_id=bancarioUser.id,
                user_id=bancarioUser.user_id,     
                banco_id=bancarioUser.banco_id ,
                numero_cuenta=bancarioUser.numero_cuenta,
                en_uso =bancarioUser.en_uso,
                terceros = bancarioUser.terceros ,
                rut_tercero = bancarioUser.rut_tercero ,
                nombre_tercero= bancarioUser.nombre_tercero ,
                email_tercero = bancarioUser.email_tercero ,
                created=bancarioUser.created,
                updated=bancarioUser.updated,
                creator_user = bancarioUser.creator_user,
                updater_user=bancarioUser.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoBancarioUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos bancarios del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_bancario_user(self, bancarioUsuario:BancariosUserSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        #creamos el nuevo registro de bancarios de usuarios
        try:
            newBancarioUser=BancariosUserModel(
                user_id=bancarioUsuario.user_id,   
                banco_id=bancarioUsuario.banco_id,
                numero_cuenta=bancarioUsuario.numero_cuenta,
                en_uso =1,
                terceros = 1 ,
                rut_tercero = bancarioUsuario.rut_tercero ,
                nombre_tercero= bancarioUsuario.nombre_tercero ,
                email_tercero = bancarioUsuario.email_tercero,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )

            #confirmamos el cambio en la Base de Datos
            self.db.add(newBancarioUser)
            self.db.commit()

            #creamos el registro historico de bancarios del usuario
            self.create_historico_bancario_user(newBancarioUser,"Se creó los datos bancarios  del usuario")

            newBancarioUserId=newBancarioUser.id
            return ({"result":"1","estado":"creado","newBancarioUserId":newBancarioUserId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    

    #metodo para consultar los datos bancarios del usuario 
    # @params userId: id del Usuario al cual se le estan consultadn los datos bancarios
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
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos bancarios del usuario","data":bancariosUserExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
    #metodo para actualizar los datos bancarios del usuario 
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def update_bancario_user(self,userUpdaterId:int ,bancarioUsuario:BancariosUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        bancarioId=bancarioUsuario.id

        # buscamos si existe el banco
        nRecord = self.db.query(BancariosUserModel).filter(BancariosUserModel.id == bancarioId).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del bnco
            return ({"result":"-2","estado":f"No record found {bancarioId}"})
        else:
            # existen los datosdel banco se puede actualizar
            try:
                #extraemos los datos para guardar el histórico
                bancarioUserExists = self.db.query(BancariosUserModel).filter(BancariosUserModel.id == bancarioId).first()                  

                #creamos el registro historico de banco
                #self.create_historico_bancario_user(bancarioUserExists,"Actualización de la data de contacto del usuario")   

                enUsoT=0
                if (bancarioUsuario.en_uso==True):
                    enUsoT=1    

                tercerosT=0
                if (bancarioUsuario.terceros==True):
                    tercerosT=1

                #registramnos los cambios en la tabla de bancarios del usuario
                bancarioUserExists.user_id=bancarioUsuario.user_id,   
                bancarioUserExists.banco_id=bancarioUsuario.banco_id,
                bancarioUserExists.numero_cuenta=bancarioUsuario.numero_cuenta,
                bancarioUserExists.en_uso =  1,
                bancarioUserExists.terceros = 1,
                bancarioUserExists.rut_tercero = bancarioUsuario.rut_tercero,
                bancarioUserExists.nombre_tercero= ((bancarioUsuario.nombre_tercero).upper()).strip() ,
                bancarioUserExists.email_tercero = bancarioUsuario.email_tercero,
                bancarioUserExists.updated=ahora,
                bancarioUserExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de contacto del usuario","BancariosUser":bancarioUserExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
        

    # metodo para consultar todos los  los datos personales del usuario 
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_bancarios_users(self, page, records):
        consulta = self.db.query(ViewGeneralBancariosUserModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)
            

    # metodo para listar los datos historicos bancarios del usuario 
    # @params userId:: Id del usuario que se esta consultando
    def list_history_bancario_user(self,userId):

        # buscamos si existen los datos bancarios del usuario
        nRecord = self.db.query(HistoricoBancariosUserModel).filter(HistoricoBancariosUserModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el banco no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe extraemos los datos y los enviamos
            try:
                listHistoryBancariosUser = self.db.query(HistoricoBancariosUserModel).filter(HistoricoBancariosUserModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos los registros
                return ({"result":"1","estado":"Se consiguieron los datos bancarios del usuario","data": listHistoryBancariosUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     