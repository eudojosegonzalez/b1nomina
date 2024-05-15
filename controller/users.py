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
import pdb

import base64
from PIL import Image


from middleware.error_handler import ErrorHandler

from fastapi import File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import openpyxl
from controller.validaciones_user import ValidationController
from controller.validaciones_user import ValidationController
from controller.contact_users import contactUserController
from controller.ubication_users import ubicationUserController
from controller.colacion_usuarios import ColacionUsuariosController
from controller.pic_users import PicUserController
from controller.cv_users import CVUserController
from controller.contrato_users import ContratoUserController
from controller.estatus_inscripcion_users import EstatusInscripcionUserController
from controller.datos_laborales import DatosLaboralesController
from controller.contact_users import contactUserController



'''from controller.datos_laborales import DatosLaboralesController
from controller.datos_pago import DatosPagoController
from controller.campos_adicionales_user import CamposUserController

from controller.usuarios_afc import UsuariosAFCController
from controller.usuarios_afp import UsuariosAFPController
from controller.usuarios_prevision_salud import UsuariosPrevisionSaludController'''

from controller.carga_masiva import CargaMasivaController



# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy import or_,and_
import datetime


#Importamos los modeloas necesarios
from models.user import Usuario as UsuarioModel
from models.historico_user import HistoricoUsuario as HistoricoUsuarioModel
from models.modulo import Modulo as ModuloModel
from models.datos_laborales import DatosLaborales as DatosLaboralesModel
from models.datos_pago import DatosPago as DatosPagoModel
from models.view_general_user import ViewGeneralUser
from models.view_general_user_modulos import viewGeneralUserModulo as viewGeneralUserModuloModel
from models.view_general_user3 import ViewGeneralUser3 as ViewGeneralUser3Model
from models.view_precarga_user import ViewPrecargaUser as ViewPrecargaUserModel
from models.contacto import Contacto as contactUserModel
from models.ubicacion import Ubicacion as UbicacionUserModel
from models.usuario_grupo import UsuariosGruposEmpleado as UsuariosGruposEmpleadoModel
from models.historico_usuario_grupo import HistoricoUsuariosGruposEmpleado as HistoricoUsuariosGruposEmpleadoModel
from models.usuario_sociedad import SociedadUsuario as SociedadUsuarioModel
from models.historico_usuario_sociedad import HistoricoSociedadUsuario as HistoricoSociedadUsuarioModel
from models.usuario_departamento import UsuariosDepartamentos as UsuariosDepartamentosModel
from models.historico_usuario_departamento import HistoricoUsuariosDepartamentos as HistoricoUsuariosDepartamentosModel
from models.view_usuarios_grupos_empleados import viewUsuariosGruposEmpleados as viewUsuariosGruposEmpleadosModel
from models.pic_users import  PicUsuarios as PicUsuariosModel
from models.view_profile_user import ViewProfileUser as ViewProfileUserModel
from models.contratados import Contratados as ContratadosModel
from models.historico_contratados import HistoricoContratados as HistoricoContratadosModel
from models.estatus_inscripcion import EstatusInscripcion as EstatusInscripcionModel
from models.view_profile_preuser import ViewProfilePreUser as ViewProfilePreUserModel
from models.usuario_afc import UsuariosAFC as UsuariosAFCModel
from models.usuario_afp import UsuariosAFP as UsuariosAFPModel
from models.usuario_prevision_salud import UsuariosPrevisionSalud as UsuariosPrevisionSaludModel
from models.colacion_usuarios import ColacionUsuarios as ColacionUsuariosModel
from models.bancarios_usuarios import BancariosUser as BancariosUserModel
from models.usuario_modulo import UsuarioModulo as UsuarioModuloModel
from models.cargos_usuarios import CargosUsuarios as CargosUsuariosModel
from models.files_users import ArchivosUsuarios as ArchivosUsuariosModel
from models.campos_adicioanles_usuarios import CamposUser as CamposUserModel
from models.usuario_sociedad import SociedadUsuario as SociedadUsuarioModel
from models.cargos_usuarios import CargosUsuarios as CargosUsuariosModel
from models.cv_users import CVUsuarios as CVUsuariosModel
from models.contrato_users import ContratoUsuarios  as ContratoUsuariosModel




from schemas.user import User as UserSchema
from schemas.usuarios_grupo import UsuariosGruposEmpleado as UsuariosGruposEmpleadoSchema
from schemas.usuarios_sociedad import UsuariosSociedad as UsuariosSociedadSchema
from schemas.preregistro_user import PreUser as PreUserSchema
from schemas.preregistro_user2 import PreUser2 as PreUser2Schema
from schemas.estatus_inscripcion import EstatusInscripcion as EstatusInscripcionSchema
from schemas.usuarios_departamentos import UsuariosDepartamentos as UsuariosDepartamentosSchema
from schemas.contratados import Contratados as ContratadosSchema
from schemas.datos_laborales_salario import DatosLaboralesSalario  as DatosLaboralesSalarioSchema
from schemas.datos_laborales_contrato import DatosLaboralesContrato as DatosLaboralesContratoSchema
from schemas.datos_laborales_puesto import DatosLaboralesPuesto as DatosLaboralesPuestoSchema
from schemas.datos_personales import DatosPersonales as DatosPersonalesSchema
from schemas.contact_ubication_user import ContactUbicationUser as ContactUbicationUserSchema

'''from schemas.user2 import UserMassive as UserMassiveSchema
from schemas.contact_user2 import ContactUserMassive as contactUserSchema
from schemas.ubicacion_user2 import UbicacionUserMassive as ubicacionUserSchema
from schemas.datos_laborales import DatosLaborales as DatosLaboralesSchema
from schemas.datos_pago import DatosPago as DatosPagoSchema
from schemas.campos_adicionales_user import CamposAdicionalesUser as CamposAdicionalesUserSchema

from schemas.usuarios_afc import UsuariosAFC as UsuariosAFCSchema
from schemas.usuarios_afp import UsuariosAFP as UsuariosAFPSchema
from schemas.usuarios_prevision_salud import UsuariosPrevicionSalud as UsuariosPrevicionSaludSchema
from schemas.colacion_usuarios import ColacionUser as ColacionUserSchema'''



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
        paso=1
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
            return( {"result":False,"cadenaError": f"Error {str(e)} paso {paso}"})            


    #metodo para guardar en el historico del usuario usuarios grupos
    #@params userUpdater: usuario que efectua la accion sobre el usuario
    #@params user: Registro de user para guardar en el historico
    #@params observacion: Observacion que se guradará en el historico del usuario como refencia de la acción efectuada        
    def create_history_user_group (self, usuarioGrupo:UsuariosGruposEmpleadoModel, observacion: str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()
        paso=1
        try:

            #creamos la instancia la nuevo registro del historico
            newHistoricoUserGrupo=HistoricoUsuariosGruposEmpleadoModel(
                usuarios_grupo_empleados_id=usuarioGrupo.id,     
                sociedad_id=usuarioGrupo.sociedad_id,
                grupo_empleados_id=usuarioGrupo.grupo_empleados_id,
                user_id=usuarioGrupo.user_id,
                created=usuarioGrupo.created,
                updated=usuarioGrupo.updated,
                creator_user = usuarioGrupo.creator_user,
                updater_user=usuarioGrupo.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            paso=2
            self.db.add(newHistoricoUserGrupo)
            paso=3
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"cadenaError": f"Error {str(e)} paso {paso}"})    

        
    #metodo para guardar en el historico de usuarios sociedads
    #@params userUpdater: usuario que efectua la accion sobre el usuario
    #@params userSociedad: Registro de UsuaruioSociedades para guardar en el historico
    #@params observacion: Observacion que se guradará en el historico del usuario como refencia de la acción efectuada        
    def create_history_user_society (self, userSociedad:SociedadUsuarioModel, observacion: str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()
        paso=1
        try:

            #creamos la instancia la nuevo registro del historico
            newHistoricoUserSociety=HistoricoSociedadUsuarioModel(
                sociedad_user_id=userSociedad.id,     
                sociedad_id=userSociedad.sociedad_id,
                user_id=userSociedad.user_id,
                created=userSociedad.created,
                updated=userSociedad.updated,
                creator_user = userSociedad.creator_user,
                updater_user=userSociedad.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            paso=2
            self.db.add(newHistoricoUserSociety)
            paso=3
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"cadenaError": f"Error {str(e)} paso {paso}"})            


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


    # metodo para consultar por Id al preusuario
    # @params userId: id del Usuario que se desea consultar
    def get_profile_preuser(self, userId):
        nrecord=self.db.query(ViewProfilePreUserModel).filter(ViewProfilePreUserModel.user_id==userId).count()
        if (nrecord > 0):
            result= self.db.query(ViewProfilePreUserModel).filter(ViewProfilePreUserModel.user_id==userId).first()


            # Convertir el resultado a un diccionario
            resultado_dict = result.to_dict()

            if (result):
                '''data={
                    "documento": result.rut,
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
                }'''
                
                data=resultado_dict
                return ({"result":"1","estado":"Usuario encontrado","data":data })   
            else:
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })                                       
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })   
        


    # metodo para consultar por Id los datos personales
    # @params userId: id del Usuario que se desea consultar
    def get_datos_personales(self, userId):
        paso=1
        try:
            paso=2
            nRecord=self.db.query(ViewProfileUserModel).filter(ViewProfileUserModel.id==userId).count()
            if (nRecord > 0):
                paso=3
                result= self.db.query(ViewProfileUserModel).filter(ViewProfileUserModel.id==userId).first()


                # Convertir el resultado a un diccionario
                paso=4
                resultado_dict = result.to_dict_personal_data()

                paso=5                    
                data=resultado_dict
                return ({"result":"1","estado":"Usuario encontrado","data":data })   
            else:
                paso=6
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })   
        
        except ValueError as e:
            return( {"result":"-3","cadenaError": f"Ocurrió un error que no pudo ser controlado {str(e)} paso {paso}"})        

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
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=preUser.documento


        # contamos si existe un rut identico en la base de datos 
        paso=2
        nRecordUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).count()


        # contamos si existe un rut identico en la base de datos 
        paso=3
        nRecordUserRutProvisiorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutV).count()        

        #verificamos si existe o no el rut y el rutprovisorio
        if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisiorio > 0)):
            # el rut ya existe
            paso=4
            userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()
            return ({"result":"-3","estado":"Este Documento ya existe en la Base de Datos, no puede volver a crearlo","user": userExistsUserRut})                
        

        # no existe el rut, procedemos a insertar el registro
        #generamos un user name aleatorio
        arregloNombres=preUser.nombres.split()
        arregloApellidos=preUser.apellidos.split()
        usernameV=arregloNombres[0]+"."+arregloApellidos[0]

        #area de valudacion
        rutOk=False
        nombresOk=False
        apellidosOk=False
        correoOk=False

        paso=5
        rutOk=ValidationController.validarRut(preUser.documento)
        paso=6
        nombresOk=ValidationController.validar_nombre(preUser.nombres)
        paso=7
        apellidosOk=ValidationController.validar_nombre(preUser.apellidos)
        paso=8
        correoOk=ValidationController.validarEmail(preUser.correo)

        if (rutOk and  nombresOk and apellidosOk  and correoOk):
            paso=9
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
                    activo=1,
                    created=ahora,
                    updated=ahora,
                    creator_user = 1,
                    updater_user=1 
                )
                paso=10
                self.db.add(newUser)
                self.db.commit()

                newUserId=newUser.id

                
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
                
            try:
                paso=11
                # creamos el registro de contacto
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
                paso=11
                self.db.add(newContactUser)
                self.db.commit()
                
                # ojo cambiar
                creatorUserId=1
               # creamos el preregistro de la foto
                paso=12
                result1=PicUserController.create_preregistro_pic(self,newUserId,creatorUserId)
                
                # creamos el preregistro del CV
                paso=13
                result2=CVUserController.activate_cv_user(self,newUserId,creatorUserId)
                      
                # creamos el preregiso del Contrato
                paso=14
                result3=ContratoUserController.activate_contrato_user(self,newUserId,creatorUserId)
                
                
                # creamos el preregistro del estatus de inscripcion
                paso=15
                estatusInscripcion = EstatusInscripcionSchema (
                    user_id=newUserId,
                    rut=1,
                    nombre=1,
                    apellido=1,
                    nacionalidad=1,
                    sexo=1,   
                    fecha_nac=1,
                    estado_civil=1,   
                    region=0,   
                    comuna=0,
                    direccion=0,   
                    telefono=1,
                    email=1,
                    tipo_contrato=0,   
                    termino=0,
                    fecha_contratacion=0,   
                    salario_base=0,
                    unidad_sueldo=0,   
                    monto_sueldo=0,
                    sociedad=0,   
                    sede=0,   
                    departamento=0,   
                    cargo=0,
                    grupo=0,   
                    modalidad=0,
                    dias_descanso=0,
                    nivel_estudio=0,
                    medio=0,   
                    banco=0,
                    tipo_cuenta=0,   
                    numero=0,
                    foto=0, 
                    cv=0,
                    contrato=0                
                )
                
                paso=16
                resutl4=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)                                

                return ({"result":"1","estado":"creado","newUserId":newUserId})

            except ValueError as e:
                return( {"result":"-1","estado": f"Error {str(e)} paso {paso}"})
 

        else:
            cadenaError="Error en los formatos de los siguientes datos:"
            if (not rutOk):
                cadenaError = cadenaError + " Rut invalido"        
            if (not nombresOk):
                cadenaError=cadenaError + " Nombres contiene caracateres inválidos"    
            if (not apellidosOk):
                cadenaError=cadenaError + " Apellidos contiene caracateres inválidos"  
            if (not correoOk):
                cadenaError=cadenaError + " El correo está mal formateado"                                        

            return ({"result":"-1","estado":f"Hay errores en sus datos {cadenaError}"})
        

    #metodo para insertar  los datos personales de preregistro del usuario   Formulario 2
    # @params preUser: esquema de los datos del usuario que se desea insertar       
    def create_pre_user2(self, preUser:PreUser2Schema, creatorUserId):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=preUser.documento


        # contamos si existe un rut identico en la base de datos 
        paso=2
        nRecordUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).count()


        # contamos si existe un rut identico en la base de datos 
        paso=3
        nRecordUserRutProvisiorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutV).count()        

        #verificamos si existe o no el rut y el rutprovisorio
        if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisiorio > 0)):
            # el rut ya existe
            paso=4
            userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()
            return ({"result":"-3","estado":"Este Documento ya existe en la Base de Datos, no puede volver a crearlo","user": userExistsUserRut})                
        

        # no existe el rut, procedemos a insertar el registro
        #generamos un user name aleatorio
        arregloNombres=preUser.nombres.split()
        arregloApellidos=preUser.apellidos.split()
        usernameV=arregloNombres[0]+"."+arregloApellidos[0]

        #area de valudacion
        rutOk=False
        nombresOk=False
        apellidosOk=False
        correoOk=False

        paso=5
        rutOk=ValidationController.validarRut(preUser.documento)
        paso=6
        nombresOk=ValidationController.validar_nombre(preUser.nombres)
        paso=7
        apellidosOk=ValidationController.validar_nombre(preUser.apellidos)
        paso=8
        correoOk=ValidationController.validarEmail(preUser.correo)

        if (rutOk and  nombresOk and apellidosOk  and correoOk):
            paso=9
            try:
                newUser=UsuarioModel(
                    rut=preUser.documento,
                    rut_provisorio="",
                    nombres = preUser.nombres.upper().strip(),
                    apellido_paterno = preUser.apellidos.upper().strip(),
                    apellido_materno = "",
                    fecha_nacimiento = preUser.fechaNacimiento,
                    sexo_id=preUser.genero,
                    estado_civil_id=preUser.estadoCivil,
                    nacionalidad_id=preUser.nacionalidad,
                    username=usernameV,
                    password=hash_password(usernameV),
                    activo=1,
                    created=ahora,
                    updated=ahora,
                    creator_user = creatorUserId,
                    updater_user=creatorUserId 
                )
                paso=10
                self.db.add(newUser)
                self.db.commit()

                newUserId=newUser.id
                
                paso=14
                # creamos el registro de contacto
                newContactUser=contactUserModel(
                    user_id=newUserId,
                    email=preUser.correo,
                    fijo=preUser.telefonoCelular,
                    movil=preUser.telefonoLocal,
                    created=ahora,
                    updated=ahora,
                    creator_user = creatorUserId,
                    updater_user=creatorUserId
                )
                
                paso=15
                self.db.add(newContactUser)
                self.db.commit()
                
                paso=16
                newUbicacionUser=UbicacionUserModel(
                    user_id=newUserId,
                    region_id=preUser.region,
                    comuna_id=preUser.localidad,
                    direccion=preUser.direccion,
                    created=ahora,
                    updated=ahora,
                    creator_user = creatorUserId,
                    updater_user=creatorUserId                    
                )
                paso=17
                self.db.add(newUbicacionUser)
                paso=18
                self.db.commit()                

                '''
                Esto se agrego para pode controlar el estatus de preinscripcion
                En la foto se crea un preregistro
                En el CV y contrato se usa el metodo activate, por que este metodo crea el registro si el mismo no existe
                Se trata de crear la url del documento en '' pero adiconalmente colocar el estatus de preinscripcion
                de estos elementos Foto, CV y contrato en 0 coo que no se ha subido nada
                '''
                # creamos el preregistro de la foto
                paso=19
                result1=PicUserController.create_preregistro_pic(self,newUserId,creatorUserId)
                
                # creamos el preregistro del CV
                paso=20
                result2=CVUserController.activate_cv_user(self,newUserId,creatorUserId)
                      
                # creamos el preregiso del Contrato
                paso=21
                result3=ContratoUserController.activate_contrato_user(self,newUserId,creatorUserId)
                
                # creamos el preregistro del estatus de inscripcion
                paso=22
                estatusInscripcion = EstatusInscripcionSchema (
                    user_id=newUserId,
                    rut=1,
                    nombre=1,
                    apellido=1,
                    nacionalidad=1,
                    sexo=1,   
                    fecha_nac=1,
                    estado_civil=1,   
                    region=0,   
                    comuna=0,
                    direccion=0,   
                    telefono=1,
                    email=1,
                    tipo_contrato=0,   
                    termino=0,
                    fecha_contratacion=0,   
                    salario_base=0,
                    unidad_sueldo=0,   
                    monto_sueldo=0,
                    sociedad=0,   
                    sede=0,   
                    departamento=0,   
                    cargo=0,
                    grupo=0,   
                    modalidad=0,
                    dias_descanso=0,
                    nivel_estudio=0,
                    medio=0,   
                    banco=0,
                    tipo_cuenta=0,   
                    numero=0,
                    foto=0, 
                    cv=0,
                    contrato=0                
                )
                paso=23
                resutl4=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)                

                return ({"result":"1","estado":"creado","newUserId":newUserId})

            except ValueError as e:
                return( {"result":"-1","estado": f"Error {str(e)} paso {paso}"})
 

        else:
            cadenaError="Error en los formatos de los siguientes datos:"
            if (not rutOk):
                cadenaError = cadenaError + " Rut invalido"        
            if (not nombresOk):
                cadenaError=cadenaError + " Nombres contiene caracateres inválidos"    
            if (not apellidosOk):
                cadenaError=cadenaError + " Apellidos contiene caracateres inválidos"  
            if (not correoOk):
                cadenaError=cadenaError + " El correo está mal formateado"                                        

            return ({"result":"-1","estado":f"Hay errores en sus datos {cadenaError}"})
        
        
    #metodo para insertar  los datos personales de preregistro del usuario   
    # @params preUser: esquema de los datos del usuario que se desea insertar       
    def update_pre_user(self, preUser:PreUser2Schema,userId, updateUser):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=preUser.documento

        # contamos si existe un rut identico en la base de datos pero de otro usuario
        paso=2
        nRecordUserRutDiferente = self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == rutV, UsuarioModel.id !=userId)).count()
        paso=3
        nRecordUserRut = self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == rutV, UsuarioModel.id ==userId)).count()

        # contamos si existe un rut identico en la base de datos 
        paso=4
        nRecordUserRutProvisiorioDiferente = self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut_provisorio == rutV,UsuarioModel.id !=userId)).count()        
        nRecordUserRutProvisiorio = self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut_provisorio == rutV,UsuarioModel.id ==userId)).count()        

        #validamos los datos personales
        rutOk=False
        nombreOk=False
        apellidoOk=False
        emailOk=False

        paso=5
        rutOk=ValidationController.validarRut(preUser.documento)
        paso=6
        nombreOk=ValidationController.validar_nombre(preUser.nombres)
        paso=7
        apellidoOk=ValidationController.validar_nombre(preUser.apellidos)
        paso=8
        emailOk=ValidationController.validarEmail(preUser.correo)

        if (rutOk and nombreOk and apellidoOk and emailOk):
            # verificamos que ese rut no este asignado a otra persona
            if ((nRecordUserRutDiferente !=0)):
                paso=9
                userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()

                return({"result":"-2","estado":"Este Documento ya existe en la Base de Datos, no puede volver a asignarlo a otro empleado", "user": userExistsUserRut }) 


            if ((nRecordUserRutProvisiorioDiferente !=0)):
                paso=10
                userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutV).first()

                return({"result":"-2","estado":"Este Documento ya existe en la Base de Datos, no puede volver a asignarlo a otro empleado", "user": userExistsUserRut }) 



            #verificamos si existe o no el rut y el rutprovisorio
            paso=11
            if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisiorio > 0)):

                # el rut ya existe actualizamos
                paso=12
                userExists = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()

                try:
                    paso=13
                    userExists.rut=preUser.documento,
                    userExists.rut_provisorio="",
                    userExists.nombres = preUser.nombres.upper().strip(),
                    userExists.apellido_paterno = preUser.apellidos.upper().strip(),
                    userExists.fecha_nacimiento = preUser.fechaNacimiento,
                    userExists.sexo_id=preUser.genero,
                    userExists.estado_civil_id=preUser.estadoCivil,
                    userExists.nacionalidad_id=preUser.nacionalidad,
                    userExists.updated=ahora,
                    userExists.updater_user=updateUser
                    
                    paso=14
                    self.db.commit()

                    # actualizamos los datos de contacto
                    # buscamos si existe los datos de contacto
                    paso=15
                    nRecordContacUser = self.db.query(contactUserModel).filter(contactUserModel.user_id==userId).count()
                    if (nRecordContacUser>0):
                        # creamos l esquema de los datos de contacto 

                        #existe Actualizamos
                        paso=16
                        contactUserExists = self.db.query(contactUserModel).filter(contactUserModel.user_id==userId).first()

                        # guardamos los datos historicos antes de guardar los cambio
                        paso=17
                        contactUserController.create_historico_contact_user(self,contactUserExists,"Actualizacion de los dtos de contacto del usuario")

                        contactUserExists.email=preUser.correo.lower().strip()
                        contactUserExists.movil=preUser.telefonoCelular
                        contactUserExists.fijo=preUser.telefonoLocal
                        contactUserExists.updated=ahora
                        contactUserExists.updater_user=updateUser   

                        paso=18
                        self.db.commit()      


                    else:
                        #no existe creamos
                        paso=19
                        newContactUser=contactUserModel(
                            user_id=userId,
                            email=preUser.correo.lower().strip(),
                            movil=preUser.telefonoCelular,
                            fijo=preUser.telefonoLocal,
                            created=ahora,
                            updated=ahora,
                            creator_user=updateUser,
                            updater_user=updateUser
                            )
                        
                        paso=20
                        self.db.add(newContactUser)
                        paso=21
                        self.db.commit()  

                        # guardamos los datos historicos despues de guardar los cambio
                        paso=22
                        contactUserController.create_historico_contact_user(self,newContactUser,"Creacion de los dtos de contacto del usuario")


                    # actualizamos los datos de ubicacion
                    # buscamos si existe los datos de ubicacion 
                    paso=23      
                    nRecordUbicationUser = self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==userId).count()

                    if (nRecordUbicationUser > 0):
                        #existe actualizamos
                        paso=24
                        ubicacionUserExists=self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==userId).first()

                        #guardamos los datos antes de actualizar en el historico
                        paso=25
                        ubicationUserController.create_historico_ubication_user(self,ubicacionUserExists,"Actualizacion de los datos de  ubicacion del usuario")

                        paso=26
                        ubicacionUserExists.region_id=preUser.region,
                        ubicacionUserExists.comuna_id=preUser.localidad,
                        ubicacionUserExists.direccion=preUser.direccion,
                        ubicacionUserExists.updated=ahora,
                        ubicacionUserExists.update_user=updateUser

                        paso=27
                        self.db.commit()  
                    else:
                        #no existe creamos el registro
                        paso=28
                        newUbicacionUser=UbicacionUserModel(
                            user_id = userId,
                            region_id =preUser.region,
                            comuna_id=preUser.localidad,
                            direccion =preUser.direccion,
                            created =ahora,    
                            updated = ahora,
                            creator_user= updateUser,   
                            updater_user=updateUser                  
                        )        

                        paso=29
                        self.db.add(newUbicacionUser)
                        paso=30
                        self.db.commit()  
                        # guardamos los datos historicos despues de guardar los cambio
                        paso=31
                        ubicationUserController.create_historico_ubication_user(self,newUbicacionUser,"Creacion de los datos de ubicacion del usuario")

                    
                    # creamos el preregistro del estatus de inscripcion
                    paso=32
                    estatusInscripcion = EstatusInscripcionSchema (
                        user_id=userId,
                        rut=1,
                        nombre=1,
                        apellido=1,
                        nacionalidad=1,
                        sexo=1,   
                        fecha_nac=1,
                        estado_civil=1,   
                        region=1,   
                        comuna=1,
                        direccion=1,   
                        telefono=1,
                        email=1,
                        tipo_contrato=0,   
                        termino=0,
                        fecha_contratacion=0,   
                        salario_base=0,
                        unidad_sueldo=0,   
                        monto_sueldo=0,
                        sociedad=0,   
                        sede=0,   
                        departamento=0,   
                        cargo=0,
                        grupo=0,   
                        modalidad=0,
                        dias_descanso=0,
                        nivel_estudio=0,
                        medio=0,   
                        banco=0,
                        tipo_cuenta=0,   
                        numero=0,
                        foto=0, 
                        cv=0,
                        contrato=0                
                    )
                    paso=10
                    resutl4=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,updateUser)                    
                    
                    return( {"result":"2","estado":"Datos Actualizados"}) 
                        
                except ValueError as e:
                    return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"}) 

            else:
                try:
                    paso=28
                    #no existe  se crea
                    usernameV=""

                    #conformamos el username
                    if (" " in (preUser.nombres).lower().strip()):
                        #dividir en arreglo
                        arreglo=((preUser.nombres).lower().strip()).split(" ")
                        elemento1=arreglo[0]
                    else:
                        #tomar el elemento completo
                        elemento1=(preUser.nombres).lower().strip()


                    if (" " in (preUser.apellidos).lower().strip()):
                        #dividir en arreglo
                        arreglo=((preUser.apellidos).lower().strip()).split(" ")
                        elemento2=arreglo[0]
                    else:
                        #tomar el elemento completo
                        elemento2=(preUser.apellidos).lower().strip()            

                    #encadenamois los elementos para crear el nombre del usuario
                    usernameV=elemento1+"."+elemento2

                    paso=29

                    newUser=UsuarioModel(
                        rut = preUser.documento,
                        nombres = preUser.nombres.strip().upper(),
                        apellido_paterno  = preUser.apellidos.strip().upper(),
                        apellido_materno  = "",
                        fecha_nacimiento = preUser.fechaNacimiento,
                        sexo_id = preUser.genero,
                        estado_civil_id = preUser.estadoCivil,
                        nacionalidad_id = preUser.nacionalidad,
                        username = usernameV,   
                        password = hash_password(usernameV),
                        activo = 1,
                        created = ahora,
                        updated = ahora,
                        creator_user= updateUser,
                        updater_user = updateUser
                    )

                    #guardamos el registro
                    paso=30
                    self.db.add(newUser)
                    paso=31
                    self.db.commit()  

                    #creamos el registro historico
                    paso=32
                    self.create_history_user(newUser,"Creacion de un usuario en el sistema")   

                    newUserId=newUser.id         

                    paso=200
                    nRecordEstatusInscripcion=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==newUserId).count()
                    if (nRecordEstatusInscripcion > 0):
                        #existe lo actualizamos
                        paso=201
                        EstatusInscripcionExits=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==newUserId).first()
                        EstatusInscripcionExits.rut=1
                        EstatusInscripcionExits.nombre=1
                        EstatusInscripcionExits.apellido=1
                        EstatusInscripcionExits.sexo=1
                        EstatusInscripcionExits.fecha_nac=1
                        EstatusInscripcionExits.estado_civil=1
                        
                        paso=202
                        self.db.commit()
                        
                    else:
                        #no existe lo creamos
                        paso=203
                        estatusInscripcion=EstatusInscripcionSchema(
                            user_id = newUserId,
                            rut=1,
                            nombre=1,
                            apellido=1,   
                            nacionalidad=1,
                            sexo=1,   
                            fecha_nac=1,
                            estado_civil=1,   
                            region=0,   
                            comuna=0,
                            direccion=0,   
                            telefono=0,
                            email=1,
                            tipo_contrato=0,   
                            termino=0,
                            fecha_contratacion=0,   
                            salario_base=0,
                            unidad_sueldo=0,   
                            monto_sueldo=0,
                            sociedad=0,   
                            sede=0,   
                            departamento=0,   
                            cargo=0,
                            grupo=0,   
                            modalidad=0,
                            dias_descanso=0,
                            nivel_estudio=0,
                            medio=0,   
                            banco=0,
                            tipo_cuenta=0,   
                            numero=0,
                            foto=0, 
                            cv=0,
                            contrato=0                            
                        )
                        paso=204
                        result=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,updateUser)                        
                        
                    #creamos los datos de contacto
                    # creamos el registro de contacto
                    paso=33
                    newContactUser=contactUserModel(
                        user_id=newUserId,
                        email=preUser.correo,
                        fijo=preUser.telefonoCelular,
                        movil=preUser.telefonoLocal,
                        created=ahora,
                        updated=ahora,
                        creator_user = updateUser,
                        updater_user=updateUser
                    )

                    paso=34
                    self.db.add(newContactUser)
                    paso=35
                    self.db.commit()    

                    # creamos el registro en el historico de contactos
                    paso=36
                    contactUserController.create_historico_contact_user(self,newContactUser,"Se creo un dato de comtacto en el sistema")        
                
                    #actualizamos el estatus de inscripcion
                    paso=400
                    EstatusInscripcionExits.telefono=1
                    EstatusInscripcionExits.email=1
                    paso=401
                    self.db.commit()
                    
                    #creamos el registro de ubicacion
                    newUbicacionUser=UbicacionUserModel(
                        user_id = newUserId,
                        region_id = preUser.region,
                        comuna_id = preUser.localidad,
                        direccion = preUser.direccion,
                        created = ahora,
                        updated = ahora,
                        creator_user= updateUser,
                        updater_user = updateUser
                    )
                    paso=37
                    self.db.add(newUbicacionUser)
                    paso=38
                    self.db.commit()  

                    #creamos el historico de ubicacion del usuario
                    paso=39
                    ubicationUserController.create_historico_ubication_user(self,newUbicacionUser,"Se creo un registro de ubicacion de usuarios en el sistema")


                    #actalizamos el estatus de inscripcion del usuario
                    paso=500
                    EstatusInscripcionExits.region=1
                    EstatusInscripcionExits.comuna=1
                    EstatusInscripcionExits.direccion=1
                    paso=501
                    self.db.commit()

                    
                    
                    return( {"result":"1","estado":"Datos Creados","newUserId":newUserId})  

                except ValueError as e:
                    return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})
            
        else:
            cadenaError="Existen errores de formatro en los datos:"
            if (not rutOk):
                cadenaError=cadenaError + " El Documento está mal formateado"

            if (not nombreOk):
                cadenaError=cadenaError + " El Nombre tiene caracteres inválidos"
            
            if (not apellidoOk):
                cadenaError=cadenaError + " El apellido tiene caracteres inválidos"

            if (not emailOk):
                cadenaError=cadenaError + " El Email esta mal formateado"

            return( {"result":"-1","cadenaError":cadenaError})               


    #metodo para insertar  los datos personales de preregistro del usuario   
    # @params preUser: esquema de los datos del usuario que se desea insertar      
    # @params idUser: id del userr que se esta actualizando
    # @params userUpdater: id del usuario que ejecuta la actualizacion                          
    def update_preuser2(self, idUser,userUpdater, preUser:PreUserSchema):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el rut o el rut provisiorio ya existen
        rutV=preUser.documento

        # verificamos is el usuario existe 
        paso=2
        nRecordUserExist=self.db.query(UsuarioModel).filter(UsuarioModel.id == idUser).count()

        if (nRecordUserExist):

            # contamos si existe un rut identico en la base de datos con otro id
            paso=3
            nRecordUserRut = self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == rutV ,UsuarioModel.id != idUser)).count()


            # contamos si existe un rut identico en la base de datos 
            paso=4
            nRecordUserRutProvisiorio = self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut_provisorio == rutV ,UsuarioModel.id != idUser)).count()        

            #verificamos si existe o no el rut y el rutprovisorio
            if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisiorio > 0)):
                # el rut ya existe
                paso=5
                userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()
                return ({"result":"-1","estado":"Este Documento ya existe en la Base de Datos, no puede volver a asignarlo a otro empleado","user": userExistsUserRut})                

            #area de validacion
            rutOk=False
            nombresOk=False
            apellidosOk=False
            correoOk=False

            paso=6
            rutOk=ValidationController.validarRut(preUser.documento)
            paso=7
            nombresOk=ValidationController.validar_nombre(preUser.nombres)
            paso=8
            apellidosOk=ValidationController.validar_nombre(preUser.apellidos)
            paso=9
            correoOk=ValidationController.validarEmail(preUser.correo)

            if (rutOk and  nombresOk and apellidosOk  and correoOk):
                try:
                    paso=10
                    userExistsUser=self.db.query(UsuarioModel).filter(UsuarioModel.id == idUser).first()
                
                    userExistsUser.rut=preUser.documento,
                    userExistsUser.nombres = preUser.nombres.upper().strip(),
                    userExistsUser.apellido_paterno = preUser.apellidos.upper().strip(),
                    userExistsUser.updated=ahora,
                    userExistsUser.updater_user=userUpdater
                    
                    paso=11
                    self.db.commit()

                except ValueError as e:
                    return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})
                        
                    
                try:
                    paso=12
                    #pdb.set_trace()
                    # actualizamos  el registro de contacto
                    # verificamos que el contacto exista
                    nRecordContact=self.db.query(contactUserModel).filter(contactUserModel.user_id==idUser).count()
                    if (nRecordContact >0 ):
                        userContactExist=self.db.query(contactUserModel).filter(contactUserModel.user_id==idUser).first()
                        paso=13
                        userContactExist.email=preUser.correo
                        paso=14
                        userContactExist.updated=ahora
                        paso=15
                        userContactExist.updater_user=userUpdater
                        
                    else:
                        paso=17
                        userContactExist=contactUserModel(
                            user_id =idUser,
                            email = preUser.correo,
                            fijo = '',
                            movil = '',
                            created = ahora, 
                            updated = ahora,
                            creator_user= userUpdater, 
                            updater_user = userUpdater                             
                        )
                        paso=18
                        self.db.add(userContactExist)
                    
                    paso=19    
                    self.db.commit()
                    
                    # actualizamos el estatus de inscripcion
                    paso=20
                    nrecordEstatusInscripcion=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==idUser).count()
                    if (nrecordEstatusInscripcion > 0):
                        paso=21
                        #existe lo actualizamos
                        estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==idUser).first()
                        paso=22
                        estatusInscripcionExists.email=1
                        paso=23
                        estatusInscripcionExists.updated=ahora
                        paso=24
                        estatusInscripcionExists.updater_user=userUpdater
                        paso=25
                        self.db.commit()
                        
                    else:
                        # no existe lo creamos
                        #creamos el eschema de datos
                        paso=26
                        estatusInscripcion=EstatusInscripcionSchema(
                            user_id = idUser,
                            rut=1,
                            nombre=1,
                            apellido=1,   
                            nacionalidad=0,
                            sexo=0,   
                            fecha_nac=0,
                            estado_civil=0,   
                            region=0,   
                            comuna=0,
                            direccion=0,   
                            telefono=0,
                            email=1,
                            tipo_contrato=0,   
                            termino=0,
                            fecha_contratacion=0,   
                            salario_base=0,
                            unidad_sueldo=0,   
                            monto_sueldo=0,
                            sociedad=0,   
                            sede=0,   
                            departamento=0,   
                            cargo=0,
                            grupo=0,   
                            modalidad=0,
                            dias_descanso=0,
                            nivel_estudio=0,
                            medio=0,   
                            banco=0,
                            tipo_cuenta=0,   
                            numero=0,
                            foto=0, 
                            cv=0,
                            contrato=0                            
                        )
                        paso=27
                        
                        result=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,userUpdater)
                        
                    return ({"result":"1","estado":"Actualizado"})
                                                
                except ValueError as e:
                    return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})

            else:
                cadenaError="Error en los formatos de los siguientes datos:"
                if (not rutOk):
                    cadenaError = cadenaError + " Rut invalido"        
                if (not nombresOk):
                    cadenaError=cadenaError + " Nombres contiene caracateres inválidos"    
                if (not apellidosOk):
                    cadenaError=cadenaError + " Apellidos contiene caracateres inválidos"  
                if (not correoOk):
                    cadenaError=cadenaError + " El correo está mal formateado"                                        

                return ({"result":"-2","estado":f"Hay errores en sus datos {cadenaError}"})        
        else:
            # usuario no encontrado
            return ({"result":"-3","estado":"Usuario no existe"}) 
    

    #metodo para insertar  los datos personales del usuario   
    # @params usuario: esquema de los datos del usuario que se desea insertar       
    def create_user(self, usuario:UserSchema, creatorUserId):
        #validaciones de los datos 
        rutOk=False
        rutProvisorioOk=False
        nombreOk=False
        apellidoPaternoOk=False
        apellidoMaternoOk=False

        #validamos el rut
        paso=0   
        rutOk=ValidationController.validarRut(usuario.rut)
        
        #validamos el rutprovisorio
        if (len(usuario.rut_provisorio.strip())>0):
            rutProvisorioOk=ValidationController.validarRut(usuario.rut_provisorio)
        else:
            rutProvisorioOk=True    
        
        #validamos el nombre
        paso=1
        nombreOk=ValidationController.validar_nombre(usuario.nombres.strip().upper())
        
        #validamos el apellido paterno
        paso=2
        apellidoPaternoOk=ValidationController.validar_nombre(usuario.apellido_paterno.strip().upper())
        
        #validamos el apellido materno
        paso=3
        if (len(usuario.apellido_materno.strip())>0):
            apellidoMaternoOk=ValidationController.validar_nombre(usuario.apellido_materno.strip().upper())
        else:
            apellidoMaternoOk=True    

        #validamos que los datos primarios esten validados
        paso=4
        if (rutOk and nombreOk and apellidoPaternoOk and apellidoMaternoOk and rutProvisorioOk):
            #obtenemos la fecha/hora del servidor
            ahora=datetime.datetime.now()
            
            # buscamos si el rut o el rut provisiorio ya existen
            rutV=usuario.rut
            rutProvisorio=usuario.rut_provisorio.strip()
            userName=usuario.username

            # contamos si existe un username identico en la base de datos
            paso=5
            nRecordUserName = self.db.query(UsuarioModel).filter(UsuarioModel.username == userName).count()  

            # contamos si existe un rut identico en la base de datos 
            paso=6
            nRecordUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).count()

            # inicializamos el arreglo userExistsUserRutProvisorio para determiniar si hay rut provisiior en la base de dtos
            userExistsUserRutProvisorio=[]
            
            # verificamos que se haya suministrado un rut provisorio
            nRecordUserRutProvisorio=0
            if (len(rutProvisorio)>0):
                # contamos si hay un rut provisiorio en la base de datos que coincida con el sumnistrado por el usuario
                paso=7
                nRecordUserRutProvisorio = self.db.query(UsuarioModel).filter(UsuarioModel.rut_provisorio == rutProvisorio).count() 
                

            if (nRecordUserName > 0):
                # el username esta ocupado
                paso=8
                userExistsUserName = self.db.query(UsuarioModel).filter(UsuarioModel.username == userName).first()  
                return ({"result":"-2","estado":"Username ya existe, no puede volver a crearlo","userId": userExistsUserName.id,"userName":userExistsUserName.username })


            if ((nRecordUserRut > 0 ) or (nRecordUserRutProvisorio > 0)):
                # el rut ya existe
                paso=9
                userExistsUserRut = self.db.query(UsuarioModel).filter(UsuarioModel.rut == rutV).first()
                return ({"result":"-3","estado":"Este Rut ya existe en la Base de Datos, no puede volver a crearlo","userId": userExistsUserRut.id,"rut":rutV })                
            

            # no existe el rut, procedemos a insertar el registro
            try:
                paso=10
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
                    activo=1,
                    created=ahora,
                    updated=ahora,
                    creator_user = creatorUserId,
                    updater_user=creatorUserId 
                )
                paso=2
                self.db.add(newUser)
                paso=3
                self.db.commit()

                #insertamos el registro en el historico
                paso=4
                self.create_history_user (newUser, "Creación del Usuario")      
                
                paso=5
                newUserId=newUser.id

                # creamos el preregistro de la foto
                paso=6
                result1=PicUserController.create_preregistro_pic(self,newUserId,creatorUserId)
                
                # creamos el preregistro del CV
                paso=7
                result2=CVUserController.activate_cv_user(self,newUserId,creatorUserId)
                      
                # creamos el preregiso del Contrato
                paso=8
                result3=ContratoUserController.activate_contrato_user(self,newUserId,creatorUserId)
                
                # creamos el preregistro del estatus de inscripcion
                paso=9
                estatusInscripcion = EstatusInscripcionSchema (
                    user_id=newUserId,
                    rut=1,
                    nombre=1,
                    apellido1=1,
                    nacionalidad=1,
                    sexo=1,   
                    fecha_nac=1,
                    estado_civil=1,   
                    region=0,   
                    comuna=0,
                    direccion=0,   
                    telefono=0,
                    email=0,
                    tipo_contrato=0,   
                    termino=0,
                    fecha_contratacion=0,   
                    salario_base=0,
                    unidad_sueldo=0,   
                    monto_sueldo=0,
                    sociedad=0,   
                    sede=0,   
                    departamento=0,   
                    cargo=0,
                    grupo=0,   
                    modalidad=0,
                    dias_descanso=0,
                    nivel_estudio=0,
                    medio=0,   
                    banco=0,
                    tipo_cuenta=0,   
                    numero=0,
                    foto=0, 
                    cv=0,
                    contrato=0                
                )
                paso=10
                resutl4=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)
                
                return ({"result":"1","estado":"creado","newUserId":newUserId})
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
        
        else:
            cadenaError="Existen errores de formatro en los datos:"
            if (not rutOk):
                cadenaError=cadenaError + " El Rut está mal formateado"
            if (not rutProvisorioOk):
                cadenaError=cadenaError + " El Rut Provisorio está mal formateado"                    

            if (not nombreOk):
                cadenaError=cadenaError + " El Nombre tiene caracteres inválidos"
            
            if (not apellidoPaternoOk):
                cadenaError=cadenaError + " El apellido Paterno tiene caracteres inválidos"

            if (not apellidoMaternoOk):
                cadenaError=cadenaError + " El apellido Materno tiene caracteres inválidos"                    

            return( {"result":"-6","cadenaError":cadenaError}) 


        
    # metodo para actualizar datos personales del usuario
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def update_user(self, user_updater: int, data : UserSchema , userId):
        try:       
            #validaciones de los datos 
            rutOk=False
            rutProvisorioOk=False
            nombreOk=False
            apellidoPaternoOk=False
            apellidoMaternoOk=False

            #validamos el rut
            paso=0   
            rutOk=ValidationController.validarRut(data.rut)
            
            #validamos el rutprovisorio
            if (len(data.rut_provisorio.strip())>0):
                rutProvisorioOk=ValidationController.validarRut(data.rut_provisorio)
            else:
                rutProvisorioOk=True    
            
            #validamos el nombre
            paso=1
            nombreOk=ValidationController.validar_nombre(data.nombres.strip().upper())
            
            #validamos el apellido paterno
            paso=2
            apellidoPaternoOk=ValidationController.validar_nombre(data.apellido_paterno.strip().upper())
            
            #validamos el apellido materno
            paso=3
            if (len(data.apellido_materno.strip())>0):
                apellidoMaternoOk=ValidationController.validar_nombre(data.apellido_materno.strip().upper())
            else:
                apellidoMaternoOk=True    

            #validamos que los datos primarios esten validados
            paso=4
            if (rutOk and nombreOk and apellidoPaternoOk and apellidoMaternoOk and rutProvisorioOk):
                paso=5
                nRecordUser = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).count()
                if (nRecordUser>0):

                    #verificamos que ese usuario no este siendo usado por otro
                    paso=7
                    nRecordUsername=self.db.query(UsuarioModel).filter(and_(UsuarioModel.username == data.username, UsuarioModel.id != userId)).count()

                    #verificamos que ese rut no este registrado en el sistema
                    paso=10
                    nRecordRut=self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == data.rut,UsuarioModel.id != userId)).count() 

                    #verificamos que ese rut_provisorio no este registrado en el sistema
                    nRecordRutProvisorio=0
                    paso=12
                    if (data.rut_provisorio!=""):
                        nRecordRutProvisorio=self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut_provisorio==data.rut_provisorio, UsuarioModel.id != userId) ).first()  


                    if (nRecordUsername > 0):
                        # se el rut ya esta siendo usado por otra persona
                        #buscamos el id de este dato que existe 
                        paso=14
                        userExists=self.db.query(UsuarioModel).filter(and_(UsuarioModel.username == data.username, UsuarioModel.id != userId)).first()
                        return ({"result":"-2","estado":"Este Username ya esta siendo ocupado en el sistema","UserId": userExists.id})     
                    elif (nRecordRut > 0):    
                        # se el rut ya esta siendo usado por otra persona
                        #buscamos el id de este dato que existe 
                        paso=15
                        userExists=self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == data.rut,UsuarioModel.id != userId)).first()
                        return ({"result":"-4","estado":"Este RUT ya esta registrado a nombre de otro usuario","UserId":userExists.id})        
                    elif (nRecordRutProvisorio > 0):    
                        # se el rut ya esta siendo usado por otra persona
                        #buscamos el id de este dato que existe 
                        paso=16
                        userExists=self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == data.rut,UsuarioModel.id != userId)).first()
                        return ({"result":"-5","estado":"Este RUT Provisorio ya esta registrado a nombre de otro usuario","UserId": nRecordRutProvisorio})                                                            
                    else:
                        paso=6
                        userExists =self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()


                        # ojo crear una funcion de uso privado para insertar los datos en el historico
                        # creamos un registro en el historico del usuario
                        paso=17
                        self.create_history_user(userExists,"Actualización de la data personal del usuario")                    

                        if (userExists.rut != data.rut):
                            userExists.rut=data.rut
                        if (userExists.rut_provisorio==data.rut_provisorio):
                            userExists.rut_provisorio=data.rut_provisorio
                        userExists.apellido_paterno=data.apellido_paterno.upper().strip()
                        userExists.apellido_materno=data.apellido_materno.upper().strip()
                        userExists.nombres=data.nombres.upper().strip()
                        userExists.fecha_nacimiento=data.fecha_nacimiento
                        userExists.sexo_id=data.sexo_id
                        userExists.estado_civil_id=data.estado_civil_id
                        userExists.nacionalidad_id=data.nacionalidad_id
                        if (userExists.username != data.username):
                            userExists.username=data.username.strip().lower()
                        userExists.activo=data.activo
                        userExists.updated=datetime.datetime.now()
                        userExists.updater_user=user_updater

                        paso=18
                        self.db.commit()
                        # se actualizó la data personal del usuario
                        data={
                            "id": userExists.id,
                            "rut": userExists.rut,
                            "rut_provisorio": userExists.rut_provisorio,                    
                            "nombres": userExists.nombres,
                            "apellido_paterno" : userExists.apellido_paterno,
                            "apellido_materno" :  userExists.apellido_materno,
                            "fecha_nacimiento": userExists.fecha_nacimiento,
                            "sexo_id":userExists.sexo_id,
                            "estado_civil_id":userExists.estado_civil_id,
                            "nacionalidad_id":userExists.nacionalidad_id,
                            "username":userExists.username,
                            "activo":userExists.activo
                        }
                        return ({"result":"1","estado":"Usuario Actualizado","data":data})
                else:
                    # no existe el ID del usuario
                    return ({"result":"-1","estado":"Usuario no encontrado","UserId":id})
            else:
                cadenaError="Existen errores de formatro en los datos:"
                if (not rutOk):
                    cadenaError=cadenaError + " El Rut está mal formateado"
                if (not rutProvisorioOk):
                    cadenaError=cadenaError + " El Rut Provisorio está mal formateado"                    

                if (not nombreOk):
                    cadenaError=cadenaError + " El Nombre tiene caracteres inválidos"
                
                if (not apellidoPaternoOk):
                    cadenaError=cadenaError + " El apellido Paterno tiene caracteres inválidos"

                if (not apellidoMaternoOk):
                    cadenaError=cadenaError + " El apellido Materno tiene caracteres inválidos"                    

                return( {"result":"-6","cadenaError":cadenaError})    
        
        except ValueError as e:
            return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}" })        

    
    #metodo para actualizar datos personales del usuario
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    # @params userId: id del usuario que se esta actualizando    
    def update_user_datos_personales (self, user_updater: int, data : DatosPersonalesSchema , userId):
        try:       
            #validaciones de los datos 
            rutOk=False
            nombreOk=False
            apellidoPaternoOk=False

            #validamos el rut
            paso=0   
            rutOk=ValidationController.validarRut(data.rut)
            
            #validamos el nombre
            paso=1
            nombreOk=ValidationController.validar_nombre(data.nombres.strip().upper())
            
            #validamos el apellido paterno
            paso=2
            apellidoPaternoOk=ValidationController.validar_nombre(data.apellido_paterno.strip().upper())
            

            #validamos que los datos primarios esten validados
            paso=4
            if (rutOk and nombreOk and apellidoPaternoOk ):
                paso=5
                nRecordUser = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).count()
                if (nRecordUser>0):

                    #verificamos que ese rut no este registrado en el sistema
                    paso=10
                    nRecordRut=self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == data.rut,UsuarioModel.id != userId)).count() 

                    if (nRecordRut > 0):    
                        # se el rut ya esta siendo usado por otra persona
                        #buscamos el id de este dato que existe 
                        paso=15
                        userExists=self.db.query(UsuarioModel).filter(and_(UsuarioModel.rut == data.rut,UsuarioModel.id != userId)).first()
                        return ({"result":"-4","estado":"Este RUT ya esta registrado a nombre de otro usuario","UserId":userExists.id})        
                    else:
                        paso=6
                        userExists =self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()


                        # ojo crear una funcion de uso privado para insertar los datos en el historico
                        # creamos un registro en el historico del usuario
                        paso=17
                        self.create_history_user(userExists,"Actualización de la data personal del usuario")                    

                        if (userExists.rut != data.rut):
                            userExists.rut=data.rut
                        userExists.apellido_paterno=data.apellido_paterno.upper().strip()
                        userExists.nombres=data.nombres.upper().strip()
                        userExists.fecha_nacimiento=data.fecha_nacimiento
                        userExists.sexo_id=data.sexo_id
                        userExists.estado_civil_id=data.estado_civil_id
                        userExists.nacionalidad_id=data.nacionalidad_id
                        userExists.updated=datetime.datetime.now()
                        userExists.updater_user=user_updater

                        paso=18
                        self.db.commit()
                        # se actualizó la data personal del usuario
                        '''                        
                        data={
                            "id": userExists.id,
                            "rut": userExists.rut,
                            "rut_provisorio": userExists.rut_provisorio,                    
                            "nombres": userExists.nombres,
                            "apellido_paterno" : userExists.apellido_paterno,
                            "apellido_materno" :  userExists.apellido_materno,
                            "fecha_nacimiento": userExists.fecha_nacimiento,
                            "sexo_id":userExists.sexo_id,
                            "estado_civil_id":userExists.estado_civil_id,
                            "nacionalidad_id":userExists.nacionalidad_id,
                            "username":userExists.username,
                            "activo":userExists.activo
                        }'''
                        paso=20
                        data=userExists.to_dict_personal_data()
                        
                        return ({"result":"1","estado":"Usuario Actualizado","data":data})
                else:
                    # no existe el ID del usuario
                    return ({"result":"-1","estado":"Usuario no encontrado","UserId":id})
            else:
                cadenaError="Existen errores de formatro en los datos:"
                if (not rutOk):
                    cadenaError=cadenaError + " El Rut está mal formateado"

                if (not nombreOk):
                    cadenaError=cadenaError + " El Nombre tiene caracteres inválidos"
                
                if (not apellidoPaternoOk):
                    cadenaError=cadenaError + " El apellido Paterno tiene caracteres inválidos"


                return( {"result":"-6","cadenaError":cadenaError})    
        
        except ValueError as e:
            return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}" })
        

    # esta funcion permite actualizar los datos de contacto y ubicacion
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: escquema de datos del usuario que incluye Datos de contacto y ubicacion
    # @params userId: id del usuario que se esta actualizando
    def update_user_datos_contacto_ubicacion (self,user_updater: int, data : ContactUbicationUserSchema , userId):
        paso=1
        ahora=datetime.datetime.now()
        try:
            # buscamos el registro de contacto
            paso=2
            nRecord=self.db.query(ViewProfileUserModel).filter(ViewProfileUserModel.id==userId).count()
            
            if (nRecord>0):
                paso=3
                # buscamos los datos de contacto para actualizar
                nContactExists=self.db.query(contactUserModel).filter(contactUserModel.user_id==userId).count()
                if (nContactExists > 0):
                    paso=3
                    # existen datos de contacto actualizamos
                    # guardamos en en historico de contacto
                    ContactExists=self.db.query(contactUserModel).filter(contactUserModel.user_id==userId).first()
                    
                    # creamos el historico de contacto
                    
                    paso=4
                    result2=contactUserController.create_historico_contact_user(self,ContactExists,"Actualización de registros de contacto del usuario")
                    
                    '''
                    {
                    "comuna_id": 1101,
                    "direccion": "prueba de dirección",
                    "email": "example@micorreo.com",
                    "fijo": "226656168",
                    "movil": "939024766",
                    "region_id": 1
                    }                    
                    '''
                    ContactExists.movil=data.movil
                    ContactExists.fijo=data.fijo
                    ContactExists.email=data.email
                    
                    # confiramos los datos
                    paso=5
                    self.db.commit()
                    
                else:
                    # no existen lo creamos  
                    paso=6
                    newContacto=contactUserModel(
                        user_id=userId,
                        email=data.email,
                        fijo=data.fijo,
                        movil=data.movil,
                        created=ahora,
                        updated=ahora,
                        creator_user=user_updater,
                        updater_user=user_updater
                    )
                    
                    # confirmamos el registro
                    paso=7
                    self.db.add(newContacto)
                    paso=8
                    self.db.commit()
                    
                    # creamos el historico
                    paso=9
                    result2=contactUserController.create_historico_contact_user(self,newContacto,"Creación de registros de contacto del usuario")
                
                # actualizamos el estatus de inscripcion
                # verificamos el estatus de inscripcion
                paso=10
                nRecordEstatusInscripcion=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
                if (nRecordEstatusInscripcion > 0):
                    paso=11
                    result3=EstatusInscripcionUserController.update_estatus_contacto(self,userId,user_updater,1)
                else:
                    # creamos el estatus de inscripcion
                    paso=12
                    estatusInscripcion=EstatusInscripcionSchema(
                        user_id = userId,
                        rut=1,
                        nombre=1,
                        apellido=1,   
                        nacionalidad=1,
                        sexo=1,   
                        fecha_nac=1,
                        estado_civil=1,   
                        region=0,   
                        comuna=0,
                        direccion=0,   
                        telefono=1,
                        email=1,
                        tipo_contrato=0,   
                        termino=0,
                        fecha_contratacion=0,   
                        salario_base=0,
                        unidad_sueldo=0,   
                        monto_sueldo=0,
                        sociedad=0,   
                        sede=0,   
                        departamento=0,   
                        cargo=0,
                        grupo=0,   
                        modalidad=0,
                        dias_descanso=0,
                        nivel_estudio=0,
                        medio=0,   
                        banco=0,
                        tipo_cuenta=0,   
                        numero=0,
                        foto=0, 
                        cv=0,
                        contrato=0                            
                    )
                    paso=13
                    result3=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,user_updater)                        
                            
                # buscamos los datos de ubicacion para actualizar  
                paso=40
                nUbicacionExists=self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==userId).count()
                
                if (nUbicacionExists>0):
                    paso=41
                    # existe se actualiza
                    ubicationUser=self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==userId).first()
                    
                    paso=42
                    #creamos el historico
                    result4=ubicationUserController.create_historico_ubication_user(self,ubicationUser,"Actualizacion de la data de ubicación del usuario")
                    
                    paso=43
                    ubicationUser.region_id=data.region_id
                    ubicationUser.comuna_id=data.comuna_id
                    ubicationUser.direccion=data.direccion
                    
                    #confirmamos los cambios
                    paso=43
                    self.db.commit()
                    
                else:
                    # no existese crea  
                    paso=44
                    newUbicationUser = UbicacionUserModel(
                        user_id=userId,
                        region_id=data.region_id,
                        comuna_id=data.comuna_id,
                        direccion=data.direccion_id,
                        updater_user=user_updater,
                        creator_user=user_updater,
                        created=ahora,
                        updated=ahora
                    )
                    
                    paso=45
                    # confirmamos el registro
                    self.db.add(newUbicationUser)
                    self.db.commit()
                    
                    #creamos el registro historico
                    result6=ubicationUserController.create_historico_ubication_user(self,newUbicationUser,"Creacion del registro de ubicación del usuario")
                    

                # actualizamos el estatus de inscripcion ubicacion del usuario
                paso=44
                result7=EstatusInscripcionUserController.update_estatus_ubicacion(self,userId,user_updater,1)                    
                
                return( {"result":"1","estado":"Se actualizo la data del usuario" })
            
            else:
                return( {"result":"-1","estado":"No se consigio al usuario" })    
            
  
        except ValueError as e:
            return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}" })            
    

    #metodo para activar al usuario del sistema
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def activate_user (self, user_updater: int, userId:int  ):
        try:       
            #verificamos que el usuario exista
            paso=1
            nRecordUser=self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).count()
            
            if (nRecordUser > 0):
                paso=2
                # extremos los datos para guardar en el historico
                user = self.db.query(UsuarioModel).filter(UsuarioModel.id==userId).first()

                # creamos un registro en el historico del usuario
                paso=3
                self.create_history_user(user,"Activacion del Usuario")    

                paso=4
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
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})
        

    #metodo para desactivar al usuario del sistema
    # @params user_updater: Id del usuario que  actualizará los datos
    # @params data: esquema que representa los datos del usuario
    def deactivate_user (self, user_updater: int, userId:int ):
        try:       
            #verificamos que el usuario exista
            paso=1
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
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})
                

    #metodo para actualizar la clave de acceso del usuario
    # @params userId: Id del usuario al que se actualizará la contraseña
    # @params user_updater: Id del usuario que  actualizará la clave
    # @params password: Nueva clave del usuario que se actualizará
    def update_password_user (self, userId : int, user_updater : int, password : str):
        paso=1
        try:       
            nRecordUser=self.db.query(UsuarioModel).filter(UsuarioModel.id == userId).count()
        except ValueError as e:
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})
        
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
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})                
         
        else:
            # no existe el ID del usuario
            return ({"result":"-1","estado":"Usuario no encontrado","UserId":userId})


    # metodo para determinar si un usuario tiene liquidaciones
    # @params id : Id del usuario que se verificará si tiene o no liquidaciones
    def verifica_liquidaciones (userId):
        return (False)

    # metodo para eliminar los datos personales del usuario 
    # @params id : Id del prospectro que se eliminará
    # @params creatorUserId : usuario del sistema que ejecuta la eliminacion del prospecto
    def delete_prospecto (self, id : int, creatorUserId: int):

        # borramos de tabl de UsuariosGrupo de Empleados
        try:
            paso=1
            tieneLiquidaciones=userController.verifica_liquidaciones (id)
            if ( tieneLiquidaciones):
                # tiene liquidaciones no podemos eliminar
                return( {"result":"-1","estado":"El prospecto no puede ser eliminado por que tiene liquidaciones"})
            else:
                # verificamos que exista 
                nRecord=self.db.query(UsuarioModel).filter(UsuarioModel.id==id).count()
                # no tiene liquidaciones podemos eliminar  
                '''
                delete from b1.UsuariosGruposEmpleado where user_id > '250';
                delete from b1.DatosPago where user_id > '250';
                delete from b1.DatosLaborales where user_id > '250';
                delete
                from b1.Contacto where user_id > '250';
                delete from b1.FotosUsuarios where user_id > '250';
                -------------------
                delete from b1.UsuariosAFC where user_id > '250';
                delete from b1.UsuariosAFP where user_id > '250';
                delete from b1.UsuariosDepartamentos where user_id > '250';
                delete from b1.UsuariosGruposEmpleado where user_id > '250';
                ----------------------------------------
                delete from b1.UsuariosPrevisionSalud where user_id > '250';
                delete from b1.ColacionUsuarios where user_id > '250';
                delete from b1.BancariosUser where user_id > '250';
                delete from b1.Ubicacion where user_id > '250';
                -------------------------------------------
                delete from b1.UsuarioModulo where user_id > '250';
                delete FROM b1.CargosUsuario where user_id > '250';
                delete FROM b1.ArchivosUsuarios where user_id > '250';
                delete FROM b1.CamposUser where user_id > '250';
                delete from b1.SociedadUsuario where user_id > '250';
                delete FROM b1.CargosUsuario where user_id > '250';
                delete FROM b1.CVUsuarios where user_id > '250';
                delete FROM b1.ContratoUsuarios where user_id > '250';
                delete FROM b1.Contratados where user_id > '250';
                delete FROM b1.EstatusInscripcion where user_id > '250';
                delete from b1.Usuario where id > '250'        
                '''     
                if (nRecord > 0):
                    paso=2
                    result1= self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==id).delete()
                    paso=3
                    result2= self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id==id).delete()
                    paso=4
                    result3= self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==id).delete()                
                    paso=5
                    result4= self.db.query(contactUserModel).filter(contactUserModel.user_id==id).delete()
                    paso=6
                    result5= self.db.query(PicUsuariosModel).filter(PicUsuariosModel.user_id==id).delete()   
                    paso=7
                    result6= self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id==id).delete()
                    paso=8
                    result7= self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id==id).delete()                
                    paso=9
                    result8= self.db.query(UsuariosDepartamentosModel).filter(UsuariosDepartamentosModel.user_id==id).delete()
                    paso=10
                    result9= self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id==id).delete()   
                    paso=11
                    result10= self.db.query(ColacionUsuariosModel).filter(ColacionUsuariosModel.user_id==id).delete()
                    paso=12
                    result11= self.db.query(BancariosUserModel).filter(BancariosUserModel.user_id==id).delete()                
                    paso=13
                    result12= self.db.query(UbicacionUserModel).filter(UbicacionUserModel.user_id==id).delete()
                    paso=14
                    result13= self.db.query(UsuarioModuloModel).filter(UsuarioModuloModel.user_id==id).delete()   
                    paso=15
                    result14= self.db.query(CargosUsuariosModel).filter(CargosUsuariosModel.user_id==id).delete()
                    paso=16
                    result15= self.db.query(ArchivosUsuariosModel).filter(ArchivosUsuariosModel.user_id==id).delete()                
                    paso=17
                    result16= self.db.query(CamposUserModel).filter(CamposUserModel.user_id==id).delete()
                    paso=18
                    result17= self.db.query(SociedadUsuarioModel).filter(SociedadUsuarioModel.user_id==id).delete()   
                    paso=19
                    result18= self.db.query(CargosUsuariosModel).filter(CargosUsuariosModel.user_id==id).delete()
                    paso=20
                    result19= self.db.query(CVUsuariosModel).filter(CVUsuariosModel.user_id==id).delete()                
                    paso=21
                    result20= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==id).delete()
                    paso=22
                    result21= self.db.query(ContratadosModel).filter(ContratadosModel.user_id==id).delete()   
                    paso=23
                    result22= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==id).delete()

                    paso=29
                    userExists=self.db.query(UsuarioModel).filter(UsuarioModel.id==id).first()
                    paso=30
                    # creamos el histórico del usuario
                    userController.create_history_user(self,userExists,"Eliminación del prospecto de la Base de Datos")                
                    paso=31
                    result28 = self.db.query(UsuarioModel).filter(UsuarioModel.id==id).delete()
                    paso=32
                    self.db.commit()
                    paso=33
                    return( {"result":"1","estado":"Prospecto eliminado"}) 
                else:
                     return( {"result":"-1","estado":"Prospecto no existe"})
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})     
                       

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
        paso=1
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
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})


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


    # metodo para consultar por Id si el usuario tiene o no una foto
    # @params userId: id del Usuario que se desea consultar
    def get_user_have_pic(self, userId):
        #buscamos si el usuario tiene una foto
        nRcecordPicUser=self.db.query(PicUsuariosModel).filter(PicUsuariosModel.user_id==userId).count()

        if (nRcecordPicUser > 0):
            return ({"result":"1","estado":"1"})                            
        else:
            return ({"result":"0","estado":0 })   
        

    # metodo para consultar por Id perfil del usuario
    # @params userId: id del Usuario que se desea consultar
    def get_user_profile(self, userId):
        #buscamos si el usuario tiene una foto
        try:
            paso=1
            nRecordUser=self.db.query(ViewProfileUserModel).filter(ViewProfileUserModel.id==userId).count()

            if (nRecordUser > 0):
                paso=2
                result=self.db.query(ViewProfileUserModel).filter(ViewProfileUserModel.id==userId).first()

                if (result.foto !=''):
                    paso=3
                    main_file = os.path.abspath(__file__)
                    paso=4
                    app_dir = os.path.dirname(main_file)+"/.."
                    paso=5
                    ruta=app_dir+result.foto
                    paso=6

                    '''with open(ruta, "rb") as image_file:
                        paso=7
                        imagen = Image.open(image_file)
                        paso=8
                        imagen_base64 = base64.b64encode(imagen.tobytes())
                        '''
                        
                    # Abre la imagen y la convierte a bytes
                    with Image.open(ruta) as img:
                        # Crea un buffer de bytes y guarda la imagen en él
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        # Obtiene los bytes de la imagen
                        img_byte_arr =buffered.getvalue()

                    # Convierte los bytes a una cadena base64
                    imagen_base64 = "data:image/png;base64," +  str(base64.b64encode(img_byte_arr).decode('utf-8'))                        
                else:
                    imagen_base64=""
                            
                paso=9
                if (result.unidad_sueldo=="1"):
                    unidadSueldoT="$"
                else:
                    unidadSueldoT="UF"
                    
                paso=10
                if (result.periodo_salario == "1"):
                    periodoSueltoTxt="Quincenal"
                elif (result.periodo_salario == "2"):
                    periodoSueltoTxt="Mensual"
                else:
                    periodoSueltoTxt="A Término"
                         
                paso=11
                    
                data={
                    "user_id": result.id,
                    "rut": result.rut  ,
                    "rut_provisorio": result.rut_provisorio  ,
                    "Nacionalidad": result.Nacionalidad  ,
                    "nombres": result.nombres  ,
                    "apellido_paterno": result.apellido_paterno  ,
                    "apellido_materno": result.apellido_materno  ,
                    "fecha_nacimiento": result.fecha_nacimiento  ,
                    "sexo_id": result.sexo_id  ,
                    "estado_civil_id": result.estado_civil_id  ,
                    "descripcion_estado_civil":result.descripcion_estado_civil,
                    "nacionalidad_id": result.nacionalidad_id  ,
                    "username": result.username  ,
                    "activo": result.activo  ,

                    "email": result.email  ,
                    "fijo": result.fijo  ,
                    "movil": result.movil  ,
                    "region_id": result.region_id  ,
                    "comuna_id": result.comuna_id  ,
                    "direccion": result.direccion  ,
                    "nomregion": result.nomregion  ,
                    "orden": result.orden  ,
                    "nomcomuna": result.nomcomuna  ,

                    "sociedad_id": result.sociedad_id  ,
                    "sede_id": result.sede_id  ,
                    "departamento_id": result.departamento_id  ,
                    "nomdepartamento": result.nomdepartamento  ,
                    "grupo_id": result.grupo_empleados_id  ,
                    "nombre_grupo": result.nombre_grupo  ,
                    "nombre_sede": result.nombre_sede  ,

                    "salario_base": result.salario_base  ,
                    "periodo_sueldo": result.periodo_salario ,
                    "periodo_sueldo_caracter": periodoSueltoTxt ,
                    "unidad_sueldo":result.unidad_sueldo,
                    "unidad_sueldo_caracater":unidadSueldoT,
                    "dias_descanso": result.dias_descanso ,  
                    "tipo_contrato_id": result.tipo_contrato_id,
                    "tipo_contrato": result.tipo_contrato,
                    "termino_contrato": result.termino_contrato_id ,
                    "fecha_inicio": result.fecha_inicio  ,
                    "fecha_fin": result.fecha_fin ,
                    "hora_ingreso": result.hora_ingreso  ,
                    "hora_egreso": result.hora_egreso  ,
                    "modalidad": result.modalidad  ,   
                    "jefatura": result.jefatura ,
                    "nivel_estudio": result.nivel_estudio,    
                    "nivel_estudio_id": result.nivel_estudio_id,    

                    "cargo": result.cargo  ,
                    "cargo_id": result.cargo_id,

                    "banco_id": result.banco_id  ,
                    "numero_cuenta": result.numero_cuenta  ,
                    "en_uso": result.en_uso  ,
                    "terceros": result.terceros  ,
                    "rut_tercero": result.rut_tercero  ,
                    "nombre_tercero": result.nombre_tercero  ,
                    "email_tercero": result.email_tercero  ,
                    "vacaciones_acumuladas": result.vacaciones_acumuladas  ,
                    "nombre_banco": result.nombre_banco ,
                    "medio_pago": result.medio_pago ,
                    "tipo_cuenta": result.tipo_cuenta  ,
                    
                    "foto": imagen_base64
                }
                
                return ({"result":"1","estado":"Perfil Encontrado","data":data})                            
            else:
                return ({"result":"-2","estado":"El usuario no tiene perfil" })   
        except ValueError as e:
            # ocurrió un error devolvemos el error
            return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso} archiv {ruta}"})


    #metodo para consultar los datos Laborales por user_id
    def get_datos_laborales_userid(self,userId:int):
        paso=1
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
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
            

    #metodo para consultar los datos de Pago por user_id
    def get_datos_pago_userid(self,userId:int):
        paso=1
        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este usuario
            try:
                DatosPagoExits = self.db.query(DatosPagoModel).filter(DatosPagoModel.user_id == userId).first()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los Datos de Pago","data":DatosPagoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})


    #metodo para consultar los datos de Pago por user_id
    def get_datos_colacion(self,userId:int):
        paso=1
        result=ColacionUsuariosController.get_colacion_user(self,userId)
        
        if (result is not None):
            if (result['result']=="1"):
                # hay datos que mostrar
                data=result['data']
                return ({"result":"1","estado":"Se consiguieron los Datos de Colacion","data":data})
            elif (result['result']=="-2"):
                #no hay datos que mostrar
                return ({"result":"-2","estado":"Este usuario, no tiene datos de colacion"})
            else:
                return({"result":"-3","estado":"Ocurrio un error que no pudo ser controlado"})
        else:
            return({"result":"-3","estado":"Ocurrio un error que no pudo ser controlado"})             
  

    # metodo que permite asignar un usuario a una sociedad 
    def asignate_user_society(self,usuarioSociedad:UsuariosSociedadSchema, userCreatorId : int):
        ahora=datetime.datetime.now()
        
        paso=1
        userId=usuarioSociedad.user_id
        sociedadId=usuarioSociedad.sociedad_id
        
        paso=2
        #buscamos si el usuario no esta asociado es esta sociedad
        nRecord = self.db.query(SociedadUsuarioModel).filter(and_(SociedadUsuarioModel.user_id==userId,SociedadUsuarioModel.sociedad_id==sociedadId)).count()

        if (nRecord > 0):
            paso=3
            # existe no lo podemos volver a asignar
            return ({"result":"-1","estado":"Ya existe una asociacion entre el usuario y la sociedad, no la puede volver a crear","UserId":userId})
        else:
            try:
                paso=4
                # se puede crear
                '''
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `sociedad_id` bigint(20) NOT NULL,  
                `user_id` bigint(20) DEFAULT NULL,
                `created` datetime NOT NULL,
                `updated` datetime NOT NULL,
                `creator_user` bigint(20) NOT NULL,
                `updater_user` bigint(20) NOT NULL,            
                '''
                newSociedadUsuario=SociedadUsuarioModel (
                    sociedad_id=sociedadId,
                    user_id=userId,
                    created=ahora,
                    updated=ahora,
                    creator_user= userCreatorId,
                    updater_user=userCreatorId
                )
                
                paso=5
                
                #confirmamos el registro
                self.db.add(newSociedadUsuario)
                self.db.commit()
                
                #creamos el registro historico
                paso=6
                userController.create_history_user_society(self,newSociedadUsuario,"Creacion de un registro en Usuarios Sociedades en el sistema")
            
                # actualizamos el estatus de sociedad en el estatus de isncripciopn del usuario
                paso=7
                result1=EstatusInscripcionUserController.update_estatus_sociedad(self,userId,userCreatorId,1)
                
                return ({"result":"1","estado":"Se creo el registro Usuarios Sociedad","data":newSociedadUsuario})                
            
            except ValueError as e:
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})            
            

    # metodo que permite asignar un usuario a un departamento
    def asignate_user_departament(self, usuarioDepartamento:UsuariosDepartamentosSchema, creatorUserId):
        ahora=datetime.datetime.now()
        
        paso=1
        userId=usuarioDepartamento.user_id
        sociedadId=usuarioDepartamento.sociedad_id
        sedeId=usuarioDepartamento.sede_id
        
        paso=2
        #buscamos si el usuario no esta asociado es esta sociedad
        nRecord = self.db.query(UsuariosDepartamentosModel).filter(and_(UsuariosDepartamentosModel.user_id==userId,
                                                                        UsuariosDepartamentosModel.sociedad_id==sociedadId,
                                                                        UsuariosDepartamentosModel.sede_id==sedeId)).count()

        if (nRecord > 0):
            paso=3
            # existe no lo podemos volver a asignar
            return ({"result":"-1","estado":"Ya existe una asociacion entre el Usuario y el Departamento, no la puede volver a crear","UserId":userId})
        else:
            try:
                paso=4
                # se puede crear
                '''
                id = Column(BIGINT, primary_key=True, autoincrement=True)
                sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
                sede_id = Column(BIGINT,  ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
                departamento_id = Column(BIGINT,  ForeignKey("Departamentos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
                user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
                created = Column (DateTime, nullable=False) #datetime NOT NULL,    
                updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
                creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
                updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,         
                '''
                newUsuarioDepartamento=UsuariosDepartamentosModel (
                    sociedad_id=sociedadId,
                    sede_id=sedeId,
                    departamento_id=usuarioDepartamento.departamento_id,
                    user_id=userId,
                    created=ahora,
                    updated=ahora,
                    creator_user= creatorUserId,
                    updater_user=creatorUserId
                )
                
                paso=5
                
                #confirmamos el registro
                self.db.add(newUsuarioDepartamento)
                self.db.commit()
                
                #creamos el registro historico
                paso=6
                userController.create_history_user_society(self,newUsuarioDepartamento,"Creacion de un registro en Usuarios Departamentos en el sistema")
            
                # actualizamos el estatus de sociedad en el estatus de isncripciopn del usuario
                paso=7
                result1=EstatusInscripcionUserController.update_estatus_departamento(self,userId,creatorUserId,1)
                
                return ({"result":"1","estado":"Se creo el registro Usuarios Departamento","data":newUsuarioDepartamento})                
            
            except ValueError as e:
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})         
          

    # metod que permite asignar un usuario a un grupo
    # @params userGroup : Esquema de datos que permitye registrar una asginacion de usuarios a un grupo
    # @params userUpdater: id del Usuario que efectua la  asignacion a un grupo            
    # @params idGroup: id del Grupo al cual se asi8gna el empleado            
    def asignate_user_group(self,userGroup: UsuariosGruposEmpleadoSchema, userCreator):
        # buscamos si existe una asginacion  previa
        paso=1
        userId=userGroup.user_id

        paso=2
        nRecordUserGroup=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==userId).count()

        if (nRecordUserGroup > 0):
            # esta asignado a un grupo no puede volver a crearlo
            #devolvemos el grupo al cual esta asignado
            userGroupExists=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==userId).first()
            return ({"result":"-2","estado":"Este empleado ya esta asignado a un grupo de empleados","data":userGroupExists})
        else:
            # puede crear el registro
            try:
                paso=3
                newUserGroup = UsuariosGruposEmpleadoModel(
                    sociedad_id=userGroup.sociedad_id,
                    user_id=userGroup.user_id,
                    grupo_empleados_id=userGroup.grupo_empleados_id,
                    created=datetime.datetime.now(),
                    updated=datetime.datetime.now(),
                    creator_user=userCreator,
                    updater_user=userCreator
                )

                paso=4
                self.db.add(newUserGroup)
                paso=5
                self.db.commit()  

                #creamos el historico del usuariso grupos 
                paso=6
                self.create_history_user_group(newUserGroup,"Asignacion de un usuario a un grupo")  
                
                result1=EstatusInscripcionUserController.update_estatus_grupo(self,userId,userCreator,1)

                return( {"result":"1","estado":"Usuario asignado a un grupo"})  

            except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})                
   

    # metod que permite consultar a que grupo está asignado un usuario
    # @params userId : Id del usuario que se está consultand
    def get_user_group(self,userId):
        # buscamos si existe una asginacion  previa
        try:
            paso=2
            nRecordUserGroup=self.db.query(viewUsuariosGruposEmpleadosModel).filter(viewUsuariosGruposEmpleadosModel.user_id==userId).count()

            if (nRecordUserGroup > 0):
                paso=3
                #devolvemos el grupo al cual esta asignado
                userGroupExists=self.db.query(viewUsuariosGruposEmpleadosModel).filter(viewUsuariosGruposEmpleadosModel.user_id==userId).first()
                return ({"result":"1","estado":"Este empleado ya esta asignado a un grupo de empleados","data":userGroupExists})
            else:
                return( {"result":"-1","estado":"No encontrado"})  

        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})           


    #metodo para actualizar el grupo al cual pertence un usuario
    # @params userId: Id del usuario que se actualizara
    # @updaterUserId: id del usuario que está actulizando
    # @idGroup: Id del grup al acual se movera el usuario
    def update_user_group (self,updaterUserId,idGroup,id):
        # buscamos si existe una asginacion  previa
        paso=1
        userId=id

        paso=2
        nRecordUserGroup=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==userId).count()

        if (nRecordUserGroup== 0):
            # no esta asignado a un grupo, no puede actuslizarlo
            return ({"result":"-2","estado":"Este empleado no esta asignado a un grupo de empleados"})
        else:
            # esta asignado se puede actulizar
            try:
                # ubicamos el registro de usuarios grupo actual
                paso=3
                usuarioGroupExists=self.db.query(UsuariosGruposEmpleadoModel).filter(UsuariosGruposEmpleadoModel.user_id==userId).first()

                #creamos el historico del usuariso grupos 
                paso=4
                self.create_history_user_group(usuarioGroupExists,"Actualizacion de un usuario a un nuevogrupo")  

                #actualizamos el registro    
                paso=5
                usuarioGroupExists.grupo_empleados_id=idGroup
                usuarioGroupExists.updater_user=updaterUserId
                usuarioGroupExists.updated=datetime.datetime.now()              
                
                # confirmamos los cambios
                paso=6
                self.db.commit()  
                '''
                sociedad_id=usuarioGrupo.sociedad_id,
                grupo_empleados_id=usuarioGrupo.grupo_empleados_id,
                user_id=usuarioGrupo.user_id,
                created=usuarioGrupo.created,
                updated=usuarioGrupo.updated,
                creator_user = usuarioGrupo.creator_user,
                updater_user=usuarioGrupo.updater_user,                
                '''
                data={
                    "id":usuarioGroupExists.id,
                    "sociedad_id":usuarioGroupExists.sociedad_id,
                    "grupo_empleados_id":usuarioGroupExists.grupo_empleados_id,
                    "user_id":usuarioGroupExists.user_id,
                    "created":usuarioGroupExists.created,
                    "updated":usuarioGroupExists.updated,
                    "creator_user":usuarioGroupExists.creator_user,
                    "updater_user":usuarioGroupExists.updater_user
                }

                return( {"result":"1","estado":"Usuario asignado a un nuevo grupo","data":data})  

            except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})         
        

    # metodo para subir datos masivos de usuarios al servidor
    # @params creatorUserId: usuario que subio el archivo
    # @params file: archivo que se está subiendo al archivo
    async def upload_massive_user(self,sociedadId,creatorUserId,file):
        try:
            result= await CargaMasivaController.upload_massive_user(self,sociedadId,creatorUserId,file)
            return (result)
        
        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            cadenaError=result['cadenaError']
            return( {"result":"-3","cadenaError": f"Error {cadenaError}"})      
                 

    # este medio permite obtener el avance de un usuario
    # @params userId: Id del usuario que se esta consultando
    def get_avance (self,userId):
        try:
            result=EstatusInscripcionUserController.avance_inscripcion(self,userId)
            if (result["result"]=="1"):
                return({"result":"1","avance": result['avance']}) 
            elif(result["result"]=="-1"):
                return({"result":"-1","estado": f"{result['estado']}"}) 
        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","cadenaError": f"Error {str(e)}"})         


    # esta funcin permite contratar los usuarios
    # @params contratado: Eschema de datos de la tabla contratados
    # creatorUserId: Id del usuario que esta contratando a la persona
    def contratar_user (self,contratado:ContratadosSchema,creatorUserId):
        ahora=datetime.datetime.now()
        
        try:
            # buscamos si existe el registro de contratados
            paso=1
            userId=contratado.user_id
            
            paso=2
            nRecord=self.db.query(ContratadosModel).filter(ContratadosModel.user_id==userId).count()
            
            if (nRecord > 0):
                #existe no se puede recontratar 
                data=self.db.query(ContratadosModel).filter(ContratadosModel.user_id==userId).first()
                return( {"result":"-1","estado": "El usuario ya esta contratado, no puede volver a contratarlo","data":data}) 
            else:
                # no existe se puede contratar
                
                '''
                verficamos en latabla de Extatus inscrpcion si cumple con los requisitos minimos
                Debe tener
                    Datos Personales
                    Datos De pago
                    Datos Laborales

                como calcular el avance
                    sumamos las columnas de EstatusInscripcion
                    de las cuales solo tomaremos en cuenta las siguientes
                    (7) rut,nombre,apellido,nacionalidad,sexo,fecha_nac,estado_civil
                    (3) region,comuna,direccion,
                    (2) telefono,email,
                    (6) tipo_contrato,termino,fecha_contratacion,salario_base,unidad_sueldo,monto_sueldo,
                    (8) sociedad,sede,departamento,cargo,grupo,modalidad,dias_descanso,nivel_estudio,
                    (6) medio,banco,tipo_cuenta,numero,foto,cv 
                    -----
                    32 
                    avance = suma * 100 / 32          
                '''                
                
                paso=3
                nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
                
                if (nRecordEstatus > 0):
                    # verificamos el avance
                    result2=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()
                    
                    '''
                    como calcular el avance
                    sumamos las columnas de EstatusInscripcion
                    de las cuales solo tomaremos en cuenta las siguientes
                    (7) -> 7 rut,nombre,apellido,nacionalidad,sexo,fecha_nac,estado_civil
                    (3) -> 3 region,comuna,direccion,
                    (2) -> 1  telefono,email,
                    (9) tipo_contrato,termino,fecha_contratacion,salario_base,unidad_sueldo,monto_sueldo,modalidad,dias_descanso,nivel_estudio
                    (5) -> 1 sociedad,sede,departamento,cargo,grupo
                    (4) -> 1 medio,banco,tipo_cuenta,numero,
                    # foto,cv ignorados
                    -----
                    32 
                    avance = suma * 100 / 32          
                    
                    Obligatorios
                    (7) rut,nombre,apellido,nacionalidad,sexo,fecha_nac,estado_civil
                    (3) region,comuna,direccion,
                    (1) telefono
                    (9) tipo_contrato,termino,fecha_contratacion,salario_base,unidad_sueldo,monto_sueldo,modalidad,dias_descanso,nivel_estudio
                    (1) sociedad
                    (1) medio
                    -----
                    22
                    '''     
                    #datos personales
                    avance=0
                    avance=int(result2.rut)+int(result2.nombre)+int(result2.apellido)+int(result2.nacionalidad)+int(result2.sexo)
                    avance+=int(result2.fecha_nac)+int(result2.estado_civil)
                    # datos de ubicacion
                    avance+=int(result2.region)+int(result2.comuna)+int(result2.direccion)
                    #datos de contacto
                    avance+=int(result2.telefono)
                    #datos de contrato
                    avance+=int(result2.tipo_contrato)+int(result2.termino)+int(result2.fecha_contratacion)
                    avance+=int(result2.salario_base)+int(result2.unidad_sueldo)+int(result2.monto_sueldo)
                    avance+=int(result2.modalidad)+int(result2.dias_descanso)+int(result2.nivel_estudio)
                    #datos de puesto de trabajo
                    avance+=int(result2.sociedad)
                    #datos de pago
                    avance+=int(result2.medio)
                    
                    if (avance >= 22):
                        # cumple con los requisitos minimos
                        newContratado= ContratadosModel(
                            sociedad_id=contratado.sociedad_id,
                            user_id=contratado.user_id,
                            estado=1,
                            created=ahora,
                            updated=ahora,
                            creator_user=creatorUserId,
                            updater_user=creatorUserId
                        )
                        paso=4
                        self.db.add(newContratado)
                        paso=5
                        self.db.commit()  
                        
                        # creamos el historico de contratados
                        newHistoricoContratado = HistoricoContratadosModel(
                            contratados_id=newContratado.id,
                            sociedad_id=contratado.sociedad_id,
                            user_id=contratado.user_id,
                            estado=1,
                            created=ahora,
                            updated=ahora,
                            creator_user=creatorUserId,
                            updater_user=creatorUserId,
                            fecha_registro=ahora,
                            observaciones="Contratacion del un usuario "+ str(contratado.user_id)                   
                        )  
                        
                        paso=6
                        self.db.add(newHistoricoContratado)
                        paso=7
                        self.db.commit()                                

                        data={
                            "id":newContratado.id,
                            "sociedad_id":newContratado.sociedad_id,
                            "user_id":newContratado.user_id,
                            "estado":newContratado.id,
                            "created":newContratado.created,
                            "updated":newContratado.updated,
                            "creator_user":newContratado.creator_user,
                            "updater_user":newContratado.updater_user
                        }
                        return( {"result":"1","estado": "Usuario Contratado", "data":data})                         
                    else:
                        # no cumple con los requsitos minimos
                        data = {}
                        if (result2.rut != 1):
                            data['rut']='falta'

                            
                        if (result2.nombre != 1):
                            data['nombre']='falta'


                        if (result2.apellido != 1):
                            data['apellido']='falta'


                        if (result2.nacionalidad != 1):
                            data['nacionalidad']='falta'


                        if (result2.sexo != 1):
                            data['sexo']='falta'

                            
                        if (result2.fecha_nac != 1):
                            data['fecha_nac']='falta'


                        if (result2.estado_civil != 1):
                            data['estado_civil']='falta'


                        if (result2.region != 1):
                            data['region']='falta'


                        if (result2.comuna != 1):
                            data['comuna']:'falta'

                            
                        if (result2.direccion != 1):
                            data['direccion']='falta'


                        if (result2.telefono != 1):
                            data['telefono']='falta'


                        if (result2.tipo_contrato != 1):
                            data['tipo_contrarto']='falta'
                            

                        if (result2.termino != 1):
                            data['termino']='falta'
   
                            
                        if (result2.fecha_contratacion != 1):
                            data['fecha_contratacion']='falta'
   
                        
                        if (result2.salario_base != 1):
                            data['salario_base']='falta'
                             
                                                
                        if (result2.unidad_sueldo != 1):
                            data['unidad_sueldo']='falta'
     
                            
                        if (result2.monto_sueldo != 1):
                            data['monto_sueldo']='falta'
   
                            
                        if (result2.modalidad != 1):
                            data['modalidad']='falta'
      
                            
                        if (result2.dias_descanso != 1):
                            data['dias_descanso']='falta'
   
                            
                        if (result2.nivel_estudio != 1):
                            data['nivel_estudio']='falta'
                                                                                                                                                            

                        if (result2.sociedad != 1):
                            data['sociedad']='falta'
 
                            
                        if (result2.medio != 1):
                            data['medio']='falta'
                             

                        return( {"result":"-4","estado": "No se cumple con la data mínima necesaria para contratarlo","data":data}) 
                        
                else:
                    return( {"result":"-2","estado": "No se pudo verificar el estatus de inscripcion del Usuario"}) 
                
 

        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","cadenaError": f"Error {str(e)} Paso: {paso}"})                     


    # metodo para actualizar los datos de salario de laborales del primer formulario de perfil del usuario 
    # @params idUser: id del userr que se esta actualizando
    # @params laboralesA: esquema de datos laborales del formulario 1
    # @params userUpdater: id del usuario que ejecuta la actualizacion                          
    def update_laborales_salario(self, idUser,userUpdater, laboralesA:DatosLaboralesSalarioSchema):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si existen los datos laborales del suaurio
        try:
            paso=2
            nRecord=self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==idUser).count()
            if (nRecord>0):
                # obtenemos el registro para actualizar
                paso=3
                datosLaboralesExists=self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==idUser).first()
                
                #creamos el registro historico de datos laborales 
                paso=4
                DatosLaboralesController.create_historico_datos_laborales(self,datosLaboralesExists,"Actualizacion de los datos laborlaes del usuario")
                
                paso=5
                    
                datosLaboralesExists.periodo_salario=laboralesA.salario_base
                datosLaboralesExists.salario_base=laboralesA.monto_sueldo
                datosLaboralesExists.unidad_sueldo=laboralesA.unidad_sueldo
                datosLaboralesExists.updated=ahora
                datosLaboralesExists.updater_user=userUpdater
                
                paso=6
                self.db.commit()
                
                return( {"result":"1","estado": "Data laboral actualizada"})  
                
            else:
                
                return( {"result":"-1","estado": "No existe datos laborales del empleado, debe crearlos"})                     

        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","cadenaError": f"Error {str(e)} Paso: {paso}"})          
  
  
    # metodo para actualizar los datos de salario de laborales del primer formulario de perfil del usuario 
    # @params idUser: id del userr que se esta actualizando
    # @params laboralesA: esquema de datos laborales del formulario 2
    # @params userUpdater: id del usuario que ejecuta la actualizacion                          
    def update_laborales_contrato(self, idUser,userUpdater, laboralesA:DatosLaboralesContratoSchema):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si existen los datos laborales del suaurio
        try:
            paso=2
            nRecord=self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==idUser).count()
            if (nRecord>0):
                # obtenemos el registro para actualizar
                paso=3
                datosLaboralesExists=self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==idUser).first()
                
                #creamos el registro historico de datos laborales 
                paso=4
                DatosLaboralesController.create_historico_datos_laborales(self,datosLaboralesExists,"Actualizacion de los datos laborlaes del usuario")
                
                paso=5
                '''
                    "tipo_contrato":1,
                    "termino_contrato":1,
                    "fecha_inicio":'2024-01-01',
                    "fecha_fin":'1990-01-01',
                    "dias_descanso":"1",
                    "nivel_estudio_id":1,
                    "hora_ingreso" : "08:00",
                    "hora_egreso" : "18:00",    
                    "jefatura":0                  
                '''
                datosLaboralesExists.tipo_contrato=laboralesA.tipo_contrato
                datosLaboralesExists.termino_contrato=laboralesA.termino_contrato
                datosLaboralesExists.fecha_inicio=laboralesA.fecha_inicio
                datosLaboralesExists.fecha_fin=laboralesA.fecha_fin
                datosLaboralesExists.dias_descanso=laboralesA.dias_descanso
                datosLaboralesExists.nivel_estudio_id=laboralesA.nivel_estudio_id
                datosLaboralesExists.hora_ingreso=laboralesA.hora_ingreso
                datosLaboralesExists.hora_egreso=laboralesA.hora_egreso
                datosLaboralesExists.jefatura=laboralesA.jefatura
                datosLaboralesExists.updated=ahora
                datosLaboralesExists.updater_user=userUpdater
                
                paso=6
                self.db.commit()
                
                return( {"result":"1","estado": "Data laboral actualizada"})  
                
            else:
                
                return( {"result":"-1","estado": "No existe datos laborales del empleado, debe crearlos"})                     

        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","cadenaError": f"Error {str(e)} Paso: {paso}"})  
        

    # metodo para actualizar los datos de puesto de laborales del primer formulario de perfil del usuario 
    # @params idUser: id del userr que se esta actualizando
    # @params laboralesA: esquema de datos laborales del formulario 3
    # @params userUpdater: id del usuario que ejecuta la actualizacion                          
    def update_laborales_puesto(self, idUser,userUpdater, laboralesA:DatosLaboralesPuestoSchema):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si existen los datos laborales del suaurio
        try:
            paso=2
            nRecord=self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==idUser).count()
            if (nRecord>0):
                # obtenemos el registro para actualizar
                paso=3
                datosLaboralesExists=self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id==idUser).first()
                
                #creamos el registro historico de datos laborales 
                paso=4
                DatosLaboralesController.create_historico_datos_laborales(self,datosLaboralesExists,"Actualizacion de los datos laborlaes del usuario")
                
                paso=5
                '''
                    "sede_id": 1,                    
                    "departamento_id": 1,                    
                    "grupo_id":1,
                    "cargo_id":1,
                    "modalidad":0,           
                '''
                datosLaboralesExists.sede_id=laboralesA.sede_id
                datosLaboralesExists.departamento_id=laboralesA.departamento_id
                datosLaboralesExists.grupo_id=laboralesA.grupo_id
                datosLaboralesExists.cargo_id=laboralesA.cargo_id
                datosLaboralesExists.modalidad=laboralesA.modalidad

                datosLaboralesExists.updated=ahora
                datosLaboralesExists.updater_user=userUpdater
                
                paso=6
                self.db.commit()
                
                return( {"result":"1","estado": "Data laboral actualizada"})  
                
            else:
                
                return( {"result":"-1","estado": "No existe datos laborales del empleado, debe crearlos"})                     

        except ValueError as e:
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","cadenaError": f"Error {str(e)} Paso: {paso}"})  