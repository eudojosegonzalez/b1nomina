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
import io
import csv

from fastapi import File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import openpyxl
from controller.validaciones_user import ValidationController
from controller.contact_users import contactUserController
from controller.ubication_users import ubicationUserController
from controller.datos_laborales import DatosLaboralesController


# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy import or_,and_
import  datetime


#Importamos los modeloas necesarios
from models.user import Usuario as UsuarioModel
from models.historico_user import HistoricoUsuario as HistoricoUsuarioModel
from models.modulo import Modulo as ModuloModel
from models.datos_laborales import DatosLaborales as DatosLaboralesModel
from models.view_general_user import ViewGeneralUser
from models.view_general_user_modulos import viewGeneralUserModulo as viewGeneralUserModuloModel
from models.view_general_user3 import ViewGeneralUser3 as ViewGeneralUser3Model
from models.view_precarga_user import ViewPrecargaUser as ViewPrecargaUserModel
from models.contacto import Contacto as contactUserModel
from models.ubicacion import Ubicacion as UbicacionUserModel


from schemas.user import User as UserSchema
from schemas.user2 import UserMassive as UserMassiveSchema
from schemas.preregistro_user import PreUser as PreUserSchema
from schemas.preregistro_user2 import PreUser2 as PreUser2Schema
from schemas.contact_user2 import ContactUserMassive as contactUserSchema
from schemas.ubicacion_user2 import UbicacionUserMassive as ubicacionUserSchema
from schemas.datos_laborales import DatosLaborales as DatosLaboralesSchema



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
    def create_history_user (self, user:UsuarioModel, observacion: str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
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
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})


    # metodo para consultar todos los  los datos personales del usuario 
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_users(self, page, records):
        consulta = self.db.query(ViewGeneralUser)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para consultar por Id al usuario
    # @params userId: id del Usuario que se desea consultar
    def get_user(self, userId):
        result= self.db.query(ViewGeneralUser3Model).filter(ViewGeneralUser3Model.id==userId).all()
        if (result):
            return ({"result":"1","estado":"Usuario encontrado","resultado":result })                            
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })   

    

    # metodo para consultar por Id al preusuario
    # @params userId: id del Usuario que se desea consultar
    def get_preuser(self, userId):
        nrecord=self.db.query(ViewPrecargaUserModel).filter(ViewPrecargaUserModel.user_id==userId).count()
        if (nrecord > 0):
            result= self.db.query(ViewPrecargaUserModel).filter(ViewPrecargaUserModel.user_id==userId).first()

            if (result):
                data={
                    "documento": result.documento,
                    "nombres": result.nombres,            
                    "apellidos": result.apellidos,
                    "correo": result.correo,
                    "nacionalidad": result.nacionalidad,
                    "genero": result.genero,
                    "fechaNacimiento": result.fechaNacimiento,
                    "estadoCivil": result.estadoCivil,
                    "region": result.region,
                    "localidad": result.localidad,
                    "direccion": result.direccion,
                    "telefonoCelular": result.telefonoCelular,
                    "telefonoLocal": result.telefonoLocal
                }
                return ({"result":"1","estado":"Usuario encontrado","data":data })   
            else:
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })                                       
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
        


    #metodo para insertar  los datos personales de preregistro del usuario   
    # @params preUser: esquema de los datos del usuario que se desea insertar       
    def create_pre_user(self, preUser:PreUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=preUser.documento


        # contamos si existe un rut identico en la base de datos 
        nRecordUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).count()


        # contamos si existe un rut identico en la base de datos 
        nRecordUserRutProvisiorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutV).count()        

        #verificamos si existe o no el rut y el rutprovisorio
        if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisiorio > 0)):
            # el rut ya existe
            userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()
            return ({"result":"-3","estado":"Este Documento ya existe en la Base de Datos, no puede volver a crearlo","user": userExistsUserRut})                
        

        # no existe el rut, procedemos a insertar el registro
        #generamos un user name aleatorio
        arregloNombres=preUser.nombres.split()
        arregloApellidos=preUser.apellidos.split()
        usernameV=arregloNombres[0]+"."+arregloApellidos[0]

        try:
            newUser=UsuarioModel(
                rut=preUser.documento,
                rut_provisorio="",
                nombres = preUser.nombres.upper().strip(),
                apellido_paterno = preUser.apellidos.upper().strip(),
                apellido_materno = "",
                fecha_nacimiento = ahora,
                sexo_id=1,
                estado_civil_id=1,
                nacionalidad_id=1,
                username=usernameV,
                password=hash_password(usernameV),
                activo=True,
                created=ahora,
                updated=ahora,
                creator_user = 1,
                updater_user=1 
            )
            self.db.add(newUser)
            self.db.commit()

            newUserId=newUser.id

            
        except ValueError as e:
            return( {"result":"-1","error": str(e)})   
                 
            
        try:
            # creamos el registro de la foto
            newContactUser=contactUserModel(
                user_id=newUserId,
                email=preUser.correo,
                fijo="",
                movil="",
                created=ahora,
                updated=ahora,
                creator_user = 1,
                updater_user=1
            )
            self.db.add(newContactUser)
            self.db.commit()

            return ({"result":"1","estado":"creado","newUserId":newUserId})

        except ValueError as e:
            return( {"result":"-1","error": str(e)})   
        

    #metodo para insertar  los datos personales de preregistro del usuario   
    # @params preUser: esquema de los datos del usuario que se desea insertar       
    def update_pre_user(self, preUser:PreUser2Schema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=preUser.documento


        # contamos si existe un rut identico en la base de datos 
        nRecordUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).count()


        # contamos si existe un rut identico en la base de datos 
        nRecordUserRutProvisiorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutV).count()        

        #verificamos si existe o no el rut y el rutprovisorio
        if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisiorio > 0)):
            # el rut ya existe actualizamos
            userExists = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()

            '''
            "documento": "19176716-0",
            "nombres": "CLAUDIA ESTEFANIA",
            "apellidos": "OLGUIN",
            "correo": "valentina.castro@2callcenter.cl",
            "nacionalidad": 1,
            "genero": 2,
            "fechaNacimiento": "1997-01-24",
            "estadoCivil": 1,
            "region": 13,
            "localidad": 13101,
            "direccion": "Sazie 2496",
            "telefonoCelular": "930542965",
            "telefonoLocal": "",            
            '''
            try:

                userExists.rut=preUser.documento,
                userExists.rut_provisorio="",
                userExists.nombres = preUser.nombres.upper().strip(),
                userExists.apellido_paterno = preUser.apellidos.upper().strip(),
                userExists.fecha_nacimiento = datetime.datetime.strptime(preUser.fechaNacimiento,"%Y-$m-%d")
                userExists.sexo_id=1,
                userExists.estado_civil_id=preUser.genero,
                userExists.nacionalidad_id=preUser.nacionalidad,
                userExists.updated=ahora,
                userExists.updater_user=1 
                
                self.db.add(userExists)
                self.db.commit()

                userId=userExists.id

                # actualizamos los datos de contacto
                # buscamos si existe los datos de contacto
                nRecordContacUser = self.db.query(contactUserModel).filter(contactUserModel.user_id==userId).count()
                if (nRecordContacUser>0):
                    # creamos l esquema de los datos de contacto 

                    #existe Actualizamos
                    contactUserExists = self.db.query(contactUserModel).filter(contactUserModel.user_id==userId).first()

                    # guardamos los datos historicos antes de guardar los cambio
                    contactUserController.create_historico_contact_user(self,contactUserExists,"Actualizacion de los dtos de contacto del usuario")

                    contactUserExists.email=preUser.correo.lower().strip()
                    contactUserExists.movil=preUser.telefonoCelular
                    contactUserExists.fijo=preUser.telefonoLocal
                    contactUserExists.updated=ahora
                    contactUserExists.updater_user=1     

                    self.db.commit()      

                else:
                    #no existe creamos
                    newContactUser=contactUserModel(
                        user_id=userId,
                        email=preUser.correo.lower().strip(),
                        movil=preUser.telefonoCelular,
                        fijo=preUser.telefonoLocal,
                        created=ahora,
                        updated=ahora,
                        creator_user=1,
                        updater_user=1 
                          )
                    self.db.add(newContactUser)
                    self.db.commit()  
                    # guardamos los datos historicos despues de guardar los cambio
                    contactUserController.create_historico_contact_user(self,newContactUser,"Creacion de los dtos de contacto del usuario")


                # actualizamos los datos de ubicacion
                # buscamos si existe los datos de ubicacion   
                nRecordUbicationUser = self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==userId).count()
                if (nRecordUbicationUser > 0):
                    #existe actualizamos

                    ubicacionUserExists=self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==userId).first()

                    #guardamos los datos antes de actualizar en el historico
                    ubicationUserController.create_historico_ubication_user(self,ubicacionUserExists,"Actualizacion de los datos de  ubicacion del usuario")

                    ubicacionUserExists.region_id=preUser.region,
                    ubicacionUserExists.comuna_id=preUser.localidad,
                    ubicacionUserExists.direccion=preUser.direccion,
                    ubicacionUserExists.updated=ahora,
                    ubicacionUserExists.update_user=1
                    self.db.commit()  
                else:
                    #no existe creamos el registro
                    newUbicacionUser=UbicacionUserModel(
                        user_id = userId,
                        region_id =preUser.region,
                        comuna_id=preUser.localidad,
                        direccion =preUser.direccion,
                        created =ahora,    
                        updated = ahora,
                        creator_user= 1,   
                        updater_user=1                  
                    )        

                    self.db.add(newUbicacionUser)
                    self.db.commit()  
                    # guardamos los datos historicos despues de guardar los cambio
                    ubicationUserController.create_historico_ubication_user(self,newUbicacionUser,"Creacion de los datos de ubicacion del usuario")
                    
            except ValueError as e:
                return( {"result":"-1","error": str(e)})   


        else:
            return( {"result":"-1","estado":"Empleado no existe"}) 



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
        nRecordUserRutProvisorio=0
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

            #insertamos el registro en el historico
            self.create_history_user (newUser, "Creación del Usuario")            

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

                #verificamos que ese usuario no este siendo usado por otro
                userExists=self.db.query(UsuarioModel).filter(UsuarioModel.username == data.username).first()
                nRecordUsername=0
                if ((userExists) and (userExists.id != data.user)):
                    nRecordUsername=1

                #verificamos que ese rut no este registrado en el sistema
                userExists=self.db.query(UsuarioModel).filter((UsuarioModel.rut == data.rut)).first() 
                nRecordRut=0
                if ((userExists) and (userExists.id != data.user)):
                    nRecordRut=1

                #verificamos que ese rut_provisorio no este registrado en el sistema
                nRecordRutProvisorio=0
                if (data.rut_provisorio!=""):
                    userExists=self.db.query(UsuarioModel).filter((UsuarioModel.rut_provisorio==data.rut_provisorio) ).first()  
                    if ((userExists) and (userExists.id != data.user)):
                        nRecordRutProvisorio=1                                                                   


                if (nRecordUsername > 0):
                    # se el rut ya esta siendo usado por otra persona
                    #buscamos el id de este dato que existe 
                    userExists=self.db.query(UsuarioModel).filter((UsuarioModel.username == data.username) and (UsuarioModel.id != data.user)).first()
                    return ({"result":"-2","estado":"Este Username ya esta siendo ocupado en el sistema","UserId": userExists.id})     
                elif (nRecordRut > 0):    
                    # se el rut ya esta siendo usado por otra persona
                    #buscamos el id de este dato que existe 
                    userExists=self.db.query(UsuarioModel).filter((UsuarioModel.rut == data.rut) and (UsuarioModel.id != data.user)).first()
                    return ({"result":"-4","estado":"Este RUT ya esta registrado a nombre de otro usuario","UserId": userExists.id})        
                elif (nRecordRutProvisorio > 0):    
                    # se el rut ya esta siendo usado por otra persona
                    #buscamos el id de este dato que existe 
                    userExists=self.db.query(UsuarioModel).filter((UsuarioModel.rut_provisorio==data.rut_provisorio) and (UsuarioModel.id!=data.user)).first()
                    return ({"result":"-5","estado":"Este RUT Provisorio ya esta registrado a nombre de otro usuario","UserId": userExists.id})                                                            
                else:

                    # ojo crear una funcion de usuo privado para insertar los datos en el historico
                    # creamos un registro en el historico del usuario
                    self.create_history_user(user,"Actualización de la data personal del usuario")                    

                    if (user.rut != data.rut):
                        user.rut=data.rut
                    if (user.rut_provisorio==data.rut_provisorio):
                        user.rut_provisorio=data.rut_provisorio
                    user.apellido_paterno=data.apellido_paterno.upper().strip()
                    user.apellido_materno=data.apellido_materno.upper().strip()
                    user.nombres=data.nombres.upper().strip()
                    user.fecha_nacimiento=data.fecha_nacimiento
                    user.sexo_id=data.sexo_id
                    user.estado_civil_id=data.estado_civil_id
                    user.nacionalidad_id=data.nacionalidad_id
                    if (user.username != data.username):
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
    def activate_user (self, user_updater: int, userId:int  ):
        try:       
            #verificamos que el usuario exista
            nRecordUser=self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).count()
            
            if (nRecordUser > 0):
                # extremos los datos para guardar en el historico
                user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()

                # creamos un registro en el historico del usuario
                self.create_history_user(user,"Activacion del Usuario")    

                user.activo=1
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater
                self.db.commit()
                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Se activo al usuario","UserId":userId})
            else:
                # no existe el ID del usuario
                return ({"result":"-1","estado":"Usuario no encontrado","UserId":userId})
        except ValueError as e:
                return( {"result":"-3","error": str(e)})
        


    #metodo para desactivar al usuario del sistema
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def deactivate_user (self, user_updater: int, userId:int ):
        try:       
            #verificamos que el usuario exista
            nRecordUser=self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).count()
            
            if (nRecordUser > 0):
                # extremos los datos para guardar en el historico
                user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()

                # creamos un registro en el historico del usuario
                self.create_history_user(user,"Desactivacion del Usuario")    

                user.activo=0
                user.updated=datetime.datetime.now()
                user.updater_user=user_updater
                self.db.commit()
                # se actualizó la data personal del usuario
                return ({"result":"1","estado":"Se desactivo al usuario","UserId":userId})
            else:
                # no existe el ID del usuario
                return ({"result":"-1","estado":"Usuario no encontrado","UserId":userId})
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

                # creamos un registro en el historico del usuario
                self.create_history_user(user,"Actualización de la clave del usuario")

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
        

    # metodo para consultar por Id los modulos asignados a una persona
    # @params userId: id del Usuario que se desea consultar
    def get_user_modules(self, userId):
        #buscamos los modulos del sistema
        Modulos= list(self.db.query(ModuloModel).filter(ModuloModel.estado==1).all())

        # buscamos los modulos asociados al usuario
        ModulosUsuario= list(self.db.query(viewGeneralUserModuloModel).filter(viewGeneralUserModuloModel.user_id==userId).all())
    

        #recorremos los modulos
        ModulosAsignados=[]


        for modulo in Modulos:
            idModulo=modulo.id
            nombreModulo=modulo.nombre
            urlModulo=modulo.url
            iconoModulo=modulo.icono
            asignado=False
            for moduloAsignado in ModulosUsuario:
                idModuloAsignadoV=moduloAsignado.modulo_id
                if (idModuloAsignadoV==idModulo):
                    asignado=True
                
            elemento={
                "idModulo":idModulo,
                "nombreModulo":nombreModulo,
                "urlModulo":urlModulo[1:],
                "iconoModulo":iconoModulo,
                "asignado":asignado
            }
            ModulosAsignados.append(elemento)
                
        result= ModulosAsignados

        if (result):
            return ({"result":"1","estado":"Modulos de Usuario encontrado","resultado":result})                            
        else:
            return ({"result":"-1","estado":"Modulos de Usuario encontrado","userId":userId })   
        


    #metodo para consultar los datos Laborales por user_id
    def get_datos_laborales_userid(self,userId:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este usuario
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).first()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los Datos Laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})    

    
    # metodo para subir datos masivos de usuarios al servidor
    # @params creatorUserId: usuario que subio el archivo
    # @params file: archivo que se está subiendo al archivo
    async def upload_massive_user(self,sociedadId,creatorUserId,file):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        try:
            # declaramos la ruta de almacenaje de las fotos del usuario            
            ruta = os.getenv("MASSIVE_USERS")

            #diccionario que contiene los tipos archivos permitidos
            permitedExtensionMassiveUsers=  os.getenv("PERMITED_MASSIVE_FILES_USERS") 
            
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})


        # Guarda el archivo en el directorio "MASSIVE_USERS"
        try:
            slug = os.path.splitext(file.filename)[0]
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})            

        # Reemplaza los caracteres no deseados por caracteres seguros
        safeFilename = re.sub(r"[^a-zA-Z0-9_-]", "_", slug)+str(uuid.uuid4())

        #path = os.path.join("files_users", file.filename)
        try:
            path = os.path.join(ruta, f"{safeFilename}.{file.filename.split('.')[-1]}")
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})            

        
        #devolvemos la extensión para verificr si se puede o no guardar el archivo
        fileExtension=file.filename.split('.')[-1]


        if (fileExtension in permitedExtensionMassiveUsers):

            file_bytes = await file.read()
            file_stream = io.BytesIO(file_bytes)


            wb = openpyxl.load_workbook(file_stream)
            sheet = wb['CargaEmpleados']


            #definimos el arreglo de resultados
            resultados=[]

            for row in sheet.iter_rows(min_row=2,values_only=True):  # Omitir primera fila (encabezados)
                if (row is not None):
                    # Obtener valores de las celdas
                    # esta es la estructura del archivo excel
                    '''
                    0	Rut
                    1	FechaIncorporacion
                    2	Nombres
                    3	ApellidoPaterno
                    4	ApellidoMaterno
                    5	Region
                    6	Comuna
                    7	Direccion
                    8	Correo
                    9	FechaNacimiento
                    10	EstadoCivil
                    11	Sexo
                    12	Nacionalidad
                    13	TelFijo
                    14	Celular
                    15	SueldoBase
                    16	UnidadSueldoBase
                    17	Jubilado AFP
                    18	Id_AFP
                    19	Dejar en blanco
                    20	Dejar en Blanco
                    21	Afiliado_AFC
                    22	Id_Prev_Salud
                    23	Pactado_Salud
                    24	IdTipoContrato
                    25	AsignacionColacion
                    26	AsignacionMovilizacion
                    27	MedioDePago
                    28	IdGrupo
                    29	H_Ingreso
                    30	H_Salida
                    31	Ciudad
                    32	Tipo de Identificador (RUT)
                    33	Observaciones Generales
                    34	Campo Usr1
                    35	Campo Usr2
                    36	Campo Usr3
                    37	Campo Usr4
                    38	Campo Usr5
                    39	CorreoPersonal
                    40	Id Dim 1
                    41	Id Dim 2
                    42	Id Dim 3
                    43	Id Dim 4
                    44	Id Dim 5
                    45	IdNivelEstudios
                    '''
                    if ((row[0] is not None) and (len(row[0].strip())>0)):  
                        rutv=row[0]
                        fechaInicio=row[1]
                        if (row[2] is not None):
                            nombresV = row[2].upper()
                        if (row[3] is not None):    
                            apellidoPaterno = row[3].upper()
                        if (row[4] is not None):    
                            apellidoMaterno = row[4].upper()
                        region=row[5]
                        comuna=row[6]
                        direccion=row[7]
                        if (row[4] is not None):                  
                            correo = row[8].lower()
                        fechaNacimiento=row[9]
                        estadoCivil=row[10]
                        sexo=row[11]
                        nacionalidad=row[12]
                        telefonoFijo=row[13]
                        celular=row[14]
                        sueldoBase=row[15]
                        UnidadSueldoBase=row[16]
                        JubiladoAFP=row[17]
                        Afiliado_AFC=row[21]
                        Id_Prev_Salud=row[22]
                        Pactado_Salud=row[23]
                        IdTipoContrato=row[24]
                        AsignacionColacion=row[25]
                        AsignacionMovilizacion=row[26]
                        MedioDePago=row[27]
                        IdGrupo=row[28]
                        H_Ingreso=row[29]
                        H_Salida=row[30]
                        Ciudad=row[31]
                        TipoIdentificador=row[32]
                        Observaciones_Generales=row[33]
                        Campo_Usr1=row[34]
                        Campo_Usr2=row[35]
                        Campo_Usr3=row[36]
                        Campo_Usr4=row[37]
                        Campo_Usr5=row[38]
                        CorreoPersonal=row[39]
                        IdDim1=row[40]
                        IdDim2=row[41]
                        IdDim3=row[42]
                        IdDim4=row[43]
                        IdDim5=row[44]
                        IdNivelEstudios=row[45]

                        allOk=True
                        causa=""


                        #validaciones
                        #formato del rut
                        if (not ValidationController.validarRut(rutv)):
                            allOk=False
                            causa="Formato de Rut invalido"                    


                        #validar email
                        if (not ValidationController.validarEmail(correo)):
                            allOk=False
                            causa="Correo invalido"       

                        
                        #validamos el nombre personal
                        if (not ValidationController.validar_nombre(nombresV)):
                            allOk=False
                            causa="El nombre personal posee caracteres inválidos"       

                        
                        #validamos el apellio paterno
                        if (not ValidationController.validar_nombre(apellidoPaterno)):
                            allOk=False
                            causa="El apellido paterno posee caracteres inválidos"    

                        
                        #validamos el apellio materno
                        if (not ValidationController.validar_nombre(apellidoMaterno)):
                            allOk=False
                            causa="El apellido materno posee caracteres inválidos"                     
                                                        
                        
                        if (sexo =="M"):
                            sexoT=1
                        else:
                            sexoT=0
                            
                        # creamos el username sumando el primer nombre + "." + primer apellido
                        mi_string = nombresV
                        if mi_string.isspace():
                            arreglo = mi_string.split()
                            primer_elemento = arreglo[0].lower()
                        else:
                            primer_elemento=mi_string.lower()


                        mi_string = apellidoPaterno
                        if mi_string.isspace():
                            arreglo = mi_string.split()
                            segundo_elemento = arreglo[0].lower()
                        else:
                            segundo_elemento=mi_string.lower()

                        usernameV = (".".join([primer_elemento, segundo_elemento]))

                        if (allOk):                    
                            Persona=UserMassiveSchema(rut=rutv,
                                                    rut_provisorio="",
                                                    nombres=nombresV,
                                                    apellido_paterno=apellidoPaterno,
                                                    apellido_materno=apellidoMaterno,
                                                    fecha_nacimiento=datetime.datetime.strptime(fechaNacimiento, "%d/%m/%Y"),
                                                    sexo_id=sexoT,
                                                    estado_civil_id=estadoCivil,
                                                    nacionalidad_id=nacionalidad,
                                                    username=usernameV,
                                                    password=hash_password(rutv),
                                                    activo=True
                                                    )
                            

                            result=self.create_user(Persona)


                            if (result['result']=="1"):
                                # se inserto correctamente los datos personales
                                newUserId=result["newUserId"]
                                
                                # insertamos datos de contacto
                                contactoUsuario=contactUserSchema (
                                    user_id=newUserId,
                                    email=correo,
                                    fijo=telefonoFijo,
                                    movil=celular
                                )
                                result2=contactUserController.create_contact_user(self,creatorUserId ,contactoUsuario)

                                # insertamos datos de localizacion
                                '''
                                user_id: int = Field (ge=1, lt=20000)
                                region_id: int = Field (ge=1, lt=20000)
                                comuna_id: int = Field (ge=1, lt=20000)
                                direccion: str = Field (min_length= 0, max_length= 250)                        
                                '''
                                ubicacionUsuario=ubicacionUserSchema(
                                    user_id=newUserId,
                                    region_id=region,
                                    comuna_id=comuna,
                                    direccion=direccion
                                )
                                result3=ubicationUserController.create_ubication_user(self,creatorUserId,ubicacionUsuario)

                                
                                #insertamos datos de laborales
                                datosLaborales=DatosLaboralesSchema(
                                    sociedad_id=sociedadId,
                                    sede_id=1,
                                    departamento_id=1,
                                    grupo_id=IdGrupo,
                                    cargo_id=1,
                                    user_id=newUserId,
                                    tipo_contrato=IdTipoContrato,
                                    termino_contrato=1,
                                    fecha_inicio= datetime.datetime.strptime(fechaInicio, "%d/%m/%Y"),
                                    fecha_fin=None,
                                    periodo_salario=30,
                                    modalidad=1,
                                    dias_descanso="6,7",
                                    salario_base=sueldoBase,
                                    nivel_estudio_id=IdNivelEstudios,
                                    unidad_sueldo=UnidadSueldoBase
                                )
                                result4=DatosLaboralesController.create_datos_laborales(self,datosLaborales,creatorUserId)
                                
                                #insertamos los datos de pago
                                
                                #insertamos los datos en los campos adicionales
                                
                                #asignar a grupo
                                
                                #datos AFC
                                
                                #datos AFP
                                
                                #datos APV
                                
                                #insertamos datos de estudio
                                
                                #conformamos los estatus de insercion de los datos del archivo
                                estatusOk="Se insertaron los siguientes datos: Personales"
                                estatusError=". No se insertaron los siguientes datos"

                                if (result2["result"]=="1"):
                                    estatusOk = estatusOk + ", Contacto"
                                else:   
                                    estatusError= " Contacto"

                                if (result3["result"]=="1"):
                                    estatusOk = estatusOk + ", Localizacion"
                                else:   
                                    estatusError= ", Localizacion"    

                                if (result4["result"]=="1"):
                                    estatusOk = estatusOk + ", Datos Laborales"
                                else:   
                                    estatusError= ", Datos Laborales"    

                            
                            elif (result['result']=="-2"):
                                estatusOk=" "
                                estatusError="No se insertaron ninguno de los datos del empleado. Ya existe este username en el sistema"                        

                            elif (result['result']=="-3"):
                                estatusOk=" "
                                estatusError="No se insertaron ninguno de los datos del empleado. Ya existe este Rut en el sistema"  
                        else:
                            estatusOk=" "
                            estatusError="No se insertaron ninguno de los datos del empleado. Error de validacion de datos " + causa

                        #creamos la data que representa una fila en el archivo de salida
                        if (estatusError == ". No se insertaron los siguientes datos"):
                            estatusError=""

                        dataR={
                            "rut":rutv,
                            "nombres":nombresV,
                            "apellidos":(" ".join([apellidoPaterno, apellidoMaterno])),
                            "estatus":estatusOk + " " + estatusError
                        }
                        resultados.append(dataR)       
                else:
                    break   


            if (len(resultados)>0):
                main_file = os.path.abspath(__file__)
                app_dir = os.path.dirname(main_file)+"/.."

                #creamos el archivo de salida
                archivoSalida = f"/{app_dir}/{ruta}/{uuid.uuid4()}.csv"

                # Abrir el archivo en modo de escritura
                with open(archivoSalida, 'w', newline='') as csvfile:
                    # Crear un escritor CSV
                    writer = csv.DictWriter(csvfile, fieldnames=resultados[0].keys())
                    
                    # Escribir la cabecera
                    writer.writeheader()
                    
                    # Escribir los datos
                    for row in resultados:
                        if (row is not None):
                            writer.writerow(row)
                        else:
                            break

                return ({"result":"1","estado":"archivo_procesado","fileResult":archivoSalida})            
                         
            else:
                return ({"result":"-2","estado":"archivo_no procesado, no se arrojpo resultados del procesamiento de los registros"})
        else:
            return ({"result":"-1","estado":"archivo_no permitido","Archivos Permitidos":list(permitedExtensionMassiveUsers)})