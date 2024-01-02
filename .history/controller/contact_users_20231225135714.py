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
                updater_user=userId
            )
            self.db.add(newContactUser)
            self.db.commit()

            newcontactUserId=newContactUser.id
            return ({"result":"1","estado":"creado","newContactUserId":newcontactUserId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    
    
 
        


    