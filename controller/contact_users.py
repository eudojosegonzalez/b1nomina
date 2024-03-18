'''
Este archivo contiene las funciones básicas del CRUD de Contacto del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Contacto"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("usuario.id", ondelete="RESTRICT", onupdate="CASCADE"))
    email = Column(VARCHAR(250), nullable=True)
    fijo = Column(VARCHAR(20), nullable=True)
    movil = Column(VARCHAR(20), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    id : int = Field (ge=1, lt= 2000)
    user_id: int = Field (ge=1,lt=2000)
    email = Optional[str]  = Field (min_length=0, max_length=250)
    fijo = Optional[str]  = Field (min_length=0, max_length=20) 
    movil = Optional[str]  = Field (min_length=0, max_length=20)
    user : int = Field (ge=1, lt= 2000)
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime


# importamos el modelo de la base de datos
from models.contacto import Contacto as contactUserModel
from models.historico_contacto import HistoricoContacto as historicoContactUserModel


# importamos el schema de datos
from schemas.contact_user import ContactUser as contactUserSchema


# esto representa los metodos implementados en la tabla
class contactUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico deñ contacto del usuario
    #@param contactUser: Modelo del registro de contacto del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_contact_user (self, contactUser: contactUserModel, observacion:str):
     # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoContactUser= historicoContactUserModel(
                user_id=contactUser.user_id,     
                email=contactUser.email,
                fijo=contactUser.fijo,
                movil=contactUser.movil,
                created=contactUser.created,
                updated=contactUser.updated,
                creator_user = contactUser.creator_user,
                updater_user=contactUser.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoContactUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    

    #metodo para insertar  los datos de contacto del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_contact_user(self, userCreatorId:int ,contactoUsuario:contactUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        contactUserId=contactoUsuario.user_id

        # inicializamos los resultados
        userContactExists=[]

        # buscamos si este usuario ya tiene un dato de contacto
        userContactExists = self.db.query(contactUserModel).filter(contactUserModel.user_id == contactUserId).first()   

        if (userContactExists):
            # el contacto del usuario ya existe no puede volver a crearlo
            return ({"result":"-2","estado":"Record found","userId": userContactExists.id })


        # no existe el contacto del usuario, procedemos a insertar el registro
        try:
            newContactUser=contactUserModel(
                user_id=contactUserId,
                email=contactoUsuario.email,
                fijo=contactoUsuario.fijo,
                movil=contactoUsuario.movil,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )
            self.db.add(newContactUser)
            self.db.commit()

            #creamos el registro historico de contacto del usuario
            contactUserController.create_historico_contact_user(self,newContactUser,"Se creó la data de contacto del usuario")

            newcontactUserId=newContactUser.id
            return ({"result":"1","estado":"creado","newContactUserId":newcontactUserId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    

    #metodo para consultar los datos de contacto del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def get_contact_user(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(contactUserModel).filter(contactUserModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                userContactExists = self.db.query(contactUserModel).filter(contactUserModel.user_id == userId).first()                  
                contactUser={
                    "id": userContactExists.id,
                    "user_id": userContactExists.user_id,
                    "email": userContactExists.email,
                    "fijo": userContactExists.fijo,
                    "movil": userContactExists.movil,
                    "created": userContactExists.created.strftime("%Y-%m-%d %H:%M:%S"),   
                    "updated": userContactExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user" : userContactExists.creator_user,   
                    "updater_user" : userContactExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos de contacto del usuario","contactUser":contactUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
    #metodo para actualizar los datos de contacto del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def update_contact_user(self,userUpdaterId:int ,contactoUsuario:contactUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        contactUserId=contactoUsuario.user_id

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(contactUserModel).filter(contactUserModel.user_id == contactUserId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                #extraemos los datos para guardar el histórico
                userContactExists = self.db.query(contactUserModel).filter(contactUserModel.user_id == contactUserId).first()                  

                #creamos el registro historico de contacto del usuario
                self.create_historico_contact_user(userContactExists,"Actualización de la data de contacto del usuario")
   
                #registramnos los cambios en la tabla de contactos
                userContactExists.user_id=contactUserId
                userContactExists.email=contactoUsuario.email
                userContactExists.fijo=contactoUsuario.fijo
                userContactExists.movil=contactoUsuario.movil
                userContactExists.updated=ahora
                userContactExists.updater_user=userUpdaterId
                self.db.commit()

                #devolvemos un diccionario con los datos actualizados
                contactUser={
                    "id": userContactExists.id,
                    "user_id": userContactExists.user_id,
                    "email": userContactExists.email,
                    "fijo": userContactExists.fijo,
                    "movil": userContactExists.movil,
                    "created": userContactExists.created.strftime("%Y-%m-%d %H:%M:%S"), 
                    "updated": userContactExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user" : userContactExists.creator_user,   
                    "updater_user" : userContactExists.updater_user
                }

                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de contacto del usuario","contactUser":contactUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
        

    # metodo para listar los datos historicos de contacto del usuario
    # @params userId:: Id del usuario que se esta consultando
    def list_history_contact_user(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(historicoContactUserModel).filter(historicoContactUserModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                listHistoryContact = self.db.query(historicoContactUserModel).filter(historicoContactUserModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos de contacto del usuario","listHistoryContact": listHistoryContact})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     