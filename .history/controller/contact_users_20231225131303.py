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
    rut: str = Field (min_length=8, max_length=100)
    rut_provisorio : Optional[str]  = Field (min_length=0, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellido_paterno :str   = Field (min_length=2, max_length=100)
    apellido_materno : str = Field (min_length=2, max_length=100)
    fecha_nacimiento : date
    sexo_id : int  = Field (ge=1, le= 2)
    estado_civil_id : int  = Field (ge=1, le= 5)
    nacionalidad_id : int   = Field (ge=1, le= 200)
    username : str  = Field (min_length=5, max_length=200)   
    password : str = Field (min_length=8, max_length=200)
    user : int = Field (ge=1, lt= 2000)
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate



from sqlalchemy import or_,and_
import  datetime


from models.user import Usuario as UsuarioModel
from models.view_general_user import ViewGeneralUser


from schemas.user import User as UserSchema


# importamos la utilidad para generar el hash del password
from utils.hasher import hash_password


# esto representa los metodos implementados en la tabla
class userController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    # metodo para consultar todos los  los datos personales del usuario 
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_users(self, page, records):
        consulta = self.db.query(ViewGeneralUser)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    
    # metodo para consultar por Id
    # @params userId: id del Usuario que se desea consultar
    def get_user(self, userId):
        result= self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()
        if (result):
            return ({"result":"1","estado":"Usuario encontrado","resultado":result })                            
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })   
        
    
    #metodo para insertar  los datos personales del usuario   
    # @params usuario: esquema de los datos del usuario que se desea insertar       
    def create_user(self, usuario:UserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=usuario.rut
        rutProvisorio=usuario.rut_provisorio.strip()
        userName=usuario.username

        userExistsUserName = self.db.query(UsuarioModel).filter(UsuarioModel.username == userName).first()   
        userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first() 
        userExistsUserRutProvisorio=[]
        if (len(rutProvisorio)>0):
            userExistsUserRutProvisorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutProvisorio).first() 


        if (userExistsUserName):
            # el username esta ocupado
            return ({"result":"-2","estado":"Username ya existe, no puede volver a crearlo","userId": userExistsUserName.id,"userName":userExistsUserName.username })


        if ((userExistsUserRut) or (userExistsUserRutProvisorio)):
            # el rut ya existe
            return ({"result":"-3","estado":"Este Rut ya existe en la Base de Datos, no puede volver a crearlo","userId": userExistsUserRut.id,"rut":rutV })                
        

        # no existe el rut, procedemos a insertar el registro
        try:
            newUser=UsuarioModel(
                rut=usuario.rut,
                rut_provisorio=usuario.rut_provisorio,
                nombres = ((usuario.nombres).upper()).strip(),
                apellido_paterno = ((usuario.apellido_paterno).upper()).strip(),
                apellido_materno = ((usuario.apellido_materno).upper()).strip(),
                fecha_nacimiento = usuario.fecha_nacimiento,
                sexo_id=usuario.sexo_id,
                estado_civil_id=usuario.estado_civil_id,
                nacionalidad_id=usuario.nacionalidad_id,
                username=usuario.username,
                password=hash_password(usuario.password),
                activo=True,
                created=ahora,
                updated=ahora,
                creator_user = 1,
                updater_user=1 
            )
            self.db.add(newUser)
            self.db.commit()

            newUserId=newUser.id
            return ({"result":"1","estado":"creado","newUserId":newUserId})
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
        


    