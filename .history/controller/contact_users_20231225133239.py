# Este archivo contiene las funciones básicas para el crud del contacto del  Usuario
# Estructura del Modelo contacto usuario
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
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate



from sqlalchemy import or_,and_
import  datetime


# importamos el modelo de la base de datos
from models.contacto import Contacto as contactUserModel


# importamos el schema de datos
from schemas.contact_user import ContactUser as contactUserSchema


# esto representa los metodos implementados en la tabla
class contactUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    
    # metodo para consultar por userId
    # @params userId: id del Usuario que se desea consultar
    def get_contact_user(self, userId):
        result= self.db.query().filter(contactUserModel.user_id==userId).first()
        if (result):
            return ({"result":"1","estado":"Contato del Usuario encontrado","resultado":result })                            
        else:
            return ({"result":"-1","estado":"Comtacto del Usuario no encontrado","userId":userId })   
        
    
    #metodo para insertar  los datos personales del usuario   
    # @params usuario: esquema de los datos del usuario que se desea insertar       
    def create_contact_user(self, userId:int ,contactoUsuario:contactUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        contactUserId=contactoUsuario.id

        userContactExists=[]
        userContactExists = self.db.query(contactUserModel).filter(contactUserModel.user_id == contactUserId).first()   

        if (userContactExists):
            # el contacto del usuario ya existe no puede volver a crearlo
            return ({"result":"-2","estado":"Datos del contacto del usuario ya existen, no puede volver a crearlos","userId": userContactExists.id })


        # no existe el contacto del usuario, procedemos a insertar el registro
        try:
            newContactUser=contactUserModel(
                user_id=contactUserId,
                email=contactoUsuario.email,
                fijo=contactoUsuario.fijo,
                movil=contactoUsuario.movil,
                created=ahora,
                updated=ahora,
                creator_user = userId,
                updater_user=userIdr
            )
            self.db.add(newContactUser)
            self.db.commit()

            newcontactUserId=newContactUser.id
            return ({"result":"1","estado":"creado","newContactUserId":newcontactUserId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    
    
    #metodo para actualizar datos personales del usuario
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def update_user (self, user_updater: int, data : UserSchema ):
        try:       
            userId=data.id 
            user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()
            if (user):
                user.rut=data.rut
                user.rut_provisorio=data.rut_provisorio
                user.apellido_paterno=data.apellido_paterno.upper().strip()
                user.apellido_materno=data.apellido_materno.upper().strip()
                user.nombres=data.nombres.upper().strip()
                user.fecha_nacimiento=data.fecha_nacimiento
                user.sexo_id=data.sexo_id
                user.estado_civil_id=data.estado_civil_id
                user.nacionalidad_id=data.nacionalidad_id
                user.username=data.username
                user.activo=data.activo
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater
                self.db.commit()
                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Usuario Actualizado","UserId":id})
            else:
                # no existe el ID del usuario
                return ({"result":"-1","estado":"Usuario no encontrado","UserId":id})
        except ValueError as e:
                return( {"result":"-3","error": str(e)})
        

    #metodo para actualizar la clave de acceso del usuario
    # @params userId: Id del usuario al que se actualizará la contraseña
    # @params user_updater: Id del usuario que  actualizará la clave
    # @params password: Nueva clave del usuario que se actualizará
    def update_password_user (self, userId : int, user_updater : int, password : str):
        try:       
            user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()
            if (user):
                password=hash_password(password)                
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater
                self.db.commit()
                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Password de Usuario Actualizado","UserId":userId})
            else:
                # no existe el ID del usuario
                return ({"result":"-1","estado":"Usuario no encontrado","UserId":userId})
        except ValueError as e:
                return( {"result":"-3","error": str(e)})


    # metodo para eliminar los datos personales del usuario 
    # NO USADO
    def delete_user (self, id : int):
        #forma 1
        # result= self.db.query(UsuarioModel).filter(UsuarioModel.id==id).first()
        # self.db.delete(result)

        #forma 2
        result= self.db.query(UsuarioModel).filter(UsuarioModel.id==id).delete()
        self.db.commit()
        return
        


    