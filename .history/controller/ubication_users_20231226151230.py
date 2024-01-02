'''
Este archivo contiene las funciones básicas del CRUD de Ubicacion del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Ubicacion"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"))
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE") )
    comuna_id = Column (BIGINT, ForeignKey("Comunas.id", ondelete="RESTRICT", onupdate="CASCADE") )
    direccion = Column (TEXT, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    id : int = Field (ge=1, lt= 20000)
    user_id: int = Field (ge=1, lt=20000)
    region_id: int = Field (ge=1, lt=2000)
    comuna_id: int = Field (ge=1, lt=2000)
    direccion: str = Field (min_length= 0, max_length= 250)
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_




import  datetime


# importamos el modelo de la base de datos
from models.ubicacion import Ubicacion as UbicationUserModel


# importamos el schema de datos
from schemas.ubicacion_user import UbicacionUser as ubicationUserSchema


# esto representa los metodos implementados en la tabla
class ubicationserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    
    # metodo para consultar por userId
    # @params userId: id del Usuario que se desea consultar
    def get_ubication_user(self, userId):
        result= self.db.query().filter(UbicationUserModel.user_id==userId).first()
        if (result):
            return ({"result":"1","estado":"Ubicación del Usuario encontrado","resultado":result })                            
        else:
            return ({"result":"-1","estado":"Ubicación del Usuario no encontrado","userId":userId })   
        
    
    #metodo para insertar  los datos de contacto del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params ubicacionUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_ubication_user(self, userCreatorId:int , ubicacionUsuario:ubicationUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        ubicationUserId=ubicacionUsuario.user_id

        # inicializamos los resultados
        userUbicationExists=[]

        # buscamos si este usuario ya tiene un dato de contacto
        userUbicationExists = self.db.query(UbicationUserModel).filter(UbicationUserModel.user_id == ubicationUserId).first()   

        if (userUbicationExists):
            # el contacto del usuario ya existe no puede volver a crearlo
            return ({"result":"-2","estado":"Record found","userId": userUbicationExists.id })


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

            newcontactUserId=newContactUser.id
            return ({"result":"1","estado":"creado","newContactUserId":newcontactUserId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    

    #metodo para actualizar los datos de contacto del usuario
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
                userContactExists = self.db.query(contactUserModel).filter(contactUserModel.user_id == contactUserId).first()                  
                userContactExists.user_id=contactUserId
                userContactExists.email=contactoUsuario.email
                userContactExists.fijo=contactoUsuario.fijo
                userContactExists.movil=contactoUsuario.movil
                userContactExists.updated=ahora
                userContactExists.updater_user=userUpdaterId
                self.db.commit()

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
        

    