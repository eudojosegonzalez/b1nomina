'''
Este archivo contiene las funciones básicas del CRUD del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Usuario"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    rut = Column(VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    rut_provisorio  = Column(VARCHAR(100), nullable=True) #VARCHAR(100) NULL,
    nombres = Column (VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
    apellido_paterno  = Column (VARCHAR(100), nullable=False) #paterno VARCHAR(100) NOT NULL,
    apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
    fecha_nacimiento = Column(DATE, nullable=False) #DATE NOT NULL,
    sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
    estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
    nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
    username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
    password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
    activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
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
import os
import re
import uuid


from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles


# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy import or_,and_
import  datetime


#Importamos los modeloas necesarios
from models.user import Usuario as UsuarioModel
from models.historico_user import HistoricoUsuario as HistoricoUsuarioModel
#from models.files_users import ArchivosUsuarios as ArchivosUsuariosModel
from models.view_general_user import ViewGeneralUser


from schemas.user import User as UserSchema


# importamos la utilidad para generar el hash del password
from utils.hasher import hash_password


# esto representa los metodos implementados en la tabla
class userController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    #metodo para guardar en el historico del usuario
    #@params userUpdater: usuario que efectua la accion sobre el usuario
    #@params user: Registro de user para guardar en el historico
    #@params observacion: Observacion que se guradará en el historico del usuario como refencia de la acción efectuada        
    def create_history_user (userUpdater: int, user:UsuarioModel, Observacion: str):
        result=1
        return (result)

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
        
    
    # metodo para consultar por Id el historico de la data personal del suaurio
    # @params userId: id del Usuario que se desea consultar
    def get_user_history_data_personal(self, userId):
        result= self.db.query(HistoricoUsuarioModel).filter(HistoricoUsuarioModel.user_id==userId).all()
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

        # contamos si existe un username identico en la base de datos
        nRecordUserName = self.db.query(UsuarioModel).filter(UsuarioModel.username == userName).count()  

        # contamos si existe un rut identico en la base de datos 
        nRecordUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).count()

        # inicializamos el arreglo userExistsUserRutProvisorio para determiniar si hay rut provisiior en la base de dtos
        userExistsUserRutProvisorio=[]
        
        # verificamos que se haya suministrado un rut provisorio
        if (len(rutProvisorio)>0):
            # contamos si hay un rut provisiorio en la base de datos que coincida con el sumnistrado por el usuario
            nRecordUserRutProvisorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutProvisorio).count() 
            

        if (nRecordUserName > 0):
            # el username esta ocupado
            userExistsUserName = self.db.query(UsuarioModel).filter(UsuarioModel.username == userName).first()  
            return ({"result":"-2","estado":"Username ya existe, no puede volver a crearlo","userId": userExistsUserName.id,"userName":userExistsUserName.username })


        if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisorio > 0)):
            # el rut ya existe
            userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()
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
                # ojo crear una funcion de usuo privado para insertar los datos en el historico
                # creamos un registro en el historico del usuario
                newHistoricoUser=HistoricoUsuarioModel(
                user_id=user.id,     
                rut=user.rut,
                rut_provisorio=user.rut_provisorio,
                nombres = ((user.nombres).upper()).strip(),
                apellido_paterno = ((user.apellido_paterno).upper()).strip(),
                apellido_materno = ((user.apellido_materno).upper()).strip(),
                fecha_nacimiento = user.fecha_nacimiento,
                sexo_id=user.sexo_id,
                estado_civil_id=user.estado_civil_id,
                nacionalidad_id=user.nacionalidad_id,
                username=user.username,
                password=user.password,
                activo=user.activo,
                created=user.created,
                updated=user.updated,
                creator_user = user.creator_user,
                updater_user=user.updater_user,
                fecha_registro=datetime.datetime.now())
                # confirmamos el registro en el historico
                self.db.add(newHistoricoUser)
                self.db.commit()

                
                #actualizamos la data personal del usuario
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
        


    #metodo para activar al usuario del sistema
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def activate_user (self, user_updater: int, data : UserSchema ):
        try:       
            userId=data.id 
            user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()
            if (user):
                user.activo=1
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater
                self.db.commit()
                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Usuario Desactivo al usuario","UserId":id})
            else:
                # no existe el ID del usuario
                return ({"result":"-1","estado":"Usuario no encontrado","UserId":id})
        except ValueError as e:
                return( {"result":"-3","error": str(e)})
        


    #metodo para desactivar al usuario del sistema
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def deactivate_user (self, user_updater: int, data : UserSchema ):
        try:       
            userId=data.id 
            user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()
            if (user):
                user.activo=0
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater
                self.db.commit()
                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Usuario Desactivo al usuario","UserId":id})
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
            nRecordUser=self.db.query(UsuarioModel).filter(UsuarioModel.id == userId).count()
        except ValueError as e:
                return( {"result":"-3","error": str(e)})
        
        if (nRecordUser>0):
            try:
                #buscamos el registro
                user = self.db.query(UsuarioModel).filter(UsuarioModel.id == userId).first()

                # insertamos los datos en el historico

                # se calcula el hash de la clave
                newPassword = hash_password(password)

                # actualizamos los registros
                user.password=newPassword
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater

                #confirmamos los cambios
                self.db.commit()

                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Password de Usuario Actualizado","UserId":userId,"newPassword": newPassword})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})            
        else:
            # no existe el ID del usuario
            return ({"result":"-1","estado":"Usuario no encontrado","UserId":userId})


    # metodo para eliminar los datos personales del usuario 
    # NO USADO
    def delete_user (self, id : int):
        result= self.db.query(UsuarioModel).filter(UsuarioModel.id==id).delete()
        self.db.commit()
        return
        

    # metodo para ejecutar búsquedas en los usuarios
    # @params finding: contenido que se buscará entre los campos de la vista de usuarios
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def search_users(self, finding, page, records):
        '''
            Posibles campos de busqueda
            ----------------------------------------
            rut	varchar(100)
            rut_provisorio	varchar(100)
            nombres	varchar(100)
            apellido_paterno	varchar(100)
            apellido_materno	varchar(100)
            username	varchar(250)
            email	varchar(250)
            fijo	varchar(20)
            movil	varchar(20)
        '''
        findingT="%"+finding+"%"
        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(ViewGeneralUser).filter(ViewGeneralUser.rut.like(findingT) | 
                                                            ViewGeneralUser.rut_provisorio.like(findingT) |  
                                                            ViewGeneralUser.nombres.like(findingT) | 
                                                            ViewGeneralUser.apellido_materno.like(findingT) |
                                                            ViewGeneralUser.apellido_paterno.like(findingT) |
                                                            ViewGeneralUser.username.like(findingT) |
                                                            ViewGeneralUser.fijo.like(findingT) |
                                                            ViewGeneralUser.movil.like(findingT) |
                                                            ViewGeneralUser.email.like(findingT) 
                                                            ).count()
            
            if (nRecord >0):
                consulta = self.db.query(ViewGeneralUser).filter(ViewGeneralUser.rut.like(findingT) | 
                                                                ViewGeneralUser.rut_provisorio.like(findingT) |  
                                                                ViewGeneralUser.nombres.like(findingT) | 
                                                                ViewGeneralUser.apellido_materno.like(findingT) |
                                                                ViewGeneralUser.apellido_paterno.like(findingT) |
                                                                ViewGeneralUser.username.like(findingT) |
                                                                ViewGeneralUser.fijo.like(findingT) |
                                                                ViewGeneralUser.movil.like(findingT) | 
                                                                ViewGeneralUser.email.like(findingT) 
                                                                )
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                result=consulta.all()
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los creiterios de búesqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})
            
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})
