'''
Este archivo contiene las funciones básicas para controlar los Contratos del usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    __tablename__="CVUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True)
    estado = Column(INTEGER, nullable=False)
    url = Column(TEXT, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
    
'''   
import os
import re
import uuid


from fastapi import File, UploadFile,  Request
from fastapi.staticfiles import StaticFiles


# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate



from sqlalchemy import or_,and_
import  datetime


#Importamos los modeloas necesarios
from models.contrato_users import ContratoUsuarios as ContratoUsuariosModel
from models.historico_contrato_users import HistoricoContratoUsuarios as HistoricoContratoUsuariosModel
from models.estatus_inscripcion import EstatusInscripcion as EstatusInscripcionModel
from models.historico_estatus_inscripcion import HistoricoEstatusInscripcion as  HistoricoEstatusInscripcionModel

from controller.estatus_inscripcion_users import EstatusInscripcionUserController

from schemas.estatus_inscripcion import EstatusInscripcion as EstatusInscripcionSchema

# esto representa los metodos implementados en la tabla
class ContratoUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    # funcion para crear el registro de historico del cv del usuario
    #@param contactUser: Modelo del registro de contaco del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_contrato_user (self, contratoUsuarios:ContratoUsuariosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()
        '''
        id = Column(BIGINT, primary_key=True, autoincrement=True)
        cv_user_id= Column(BIGINT, nullable=False)
        user_id = Column(BIGINT, nullable=False)
        estado = Column(INTEGER, nullable=False)
        url = Column(TEXT, nullable=True)
        created = Column (DateTime, nullable=False) #datetime NOT NULL,    
        updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
        creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
        updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
        fecha_registro=Column(DateTime, nullable=False)
        observaciones=Column(TEXT, nullable=False)        
        '''
        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoCVUser= HistoricoContratoUsuariosModel(
                cv_user_id=contratoUsuarios.id,                  
                user_id=contratoUsuarios.user_id,    
                estado=contratoUsuarios.estado,  
                url=contratoUsuarios.url,
                created=contratoUsuarios.created,
                updated=contratoUsuarios.updated,
                creator_user = contratoUsuarios.creator_user,
                updater_user=contratoUsuarios.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoCVUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})    


    #este metodo permite verificar si el estatus de inscricpion existe, ya sea para actualizacion o creación
    # si no existe el registro se crea con la variable estado
    # si existe se actualiza con la variable estado
    def verifica_estatus_inscripcion (self,userId: int, estado: int, creatorUserId:int):
        # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
        paso=20
        nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
        paso=21
        if (nRecordEstatus >0):
            #existe actualizamos
            paso=22
            result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,estado)
        else:
            #no existe creamos
            paso=23
            #llenamos el esquema de datos de estatus inscripcion
            estatusInscripcion=EstatusInscripcionSchema(
                user_id = userId,
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
                contrato=estado                           
            )
            
            result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)        
        
        return (result2)
    
    
    # metodo para subir el  cv de usuario al servidor
    # @params creatorUserId: usuario que subio el archivo
    # @params userId: usuario al que pertenece el archivo
    # @params file: archivo que se está subiendo al archivo
    def upload_contrato_user(self,creatorUserId,userId,file):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        paso=1
        
        try:
            # declaramos la ruta de almacenaje de las fotos del usuario    
            paso=2        
            ruta = os.getenv("FILE_USERS")

            #diccionario que contiene los tipos archivos permitidos
            paso=3
            permitedExtensionFilesUsers=  os.getenv("PERMITED_EXTENSION_FILES_USERS") 
            
            #tamaño de los archivos permitidos en Megabytes 
            #este valor esta expresado en Bytes = (n/1024/1024)Mb
            paso=4
            permitedSizeFilesUsers =  int(os.getenv("MAX_PERMITED_SIZE_FILES_USERS") ) 

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                paso=5
                return( {"result":"-3","error": str(e)})


        # Guarda el archivo en el directorio "files_users"
        try:
            paso=6
            slug = os.path.splitext(file.filename)[0]
        except ValueError as e:
            paso=7
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","error": str(e)})            

        # Reemplaza los caracteres no deseados por caracteres seguros
        paso=8
        safeFilename = re.sub(r"[^a-zA-Z0-9_-]", "_", slug)+str(uuid.uuid4())

        #path = os.path.join("files_users", file.filename)
        try:
            paso=9
            path = os.path.join(ruta, f"{safeFilename}.{file.filename.split('.')[-1]}")
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","cadenaError": f"Ocurrió el siguiente Error:{str(e)} Paso:{paso}"})            

        
        #devolvemos la extensión para verificr si se puede o no guardar el archivo
        paso=10
        fileExtension=file.filename.split('.')[-1]

        #determinamos el tamaño del archivo
        file_size = file.size

        #verificamos que no exceda el tamaño máximo permitido
        if (file_size > permitedSizeFilesUsers):
            paso=11
            # El archivo es demasiado grande
            return ({"result":"-2","estado":f"El archivo es demasiado grande, tamaño máximo permitido {(permitedSizeFilesUsers/1024/1024)}Mb"})

        if (fileExtension in permitedExtensionFilesUsers):
            try:
                #guardamos el archivo
                paso=12
                with open(path, "wb") as f:
                    f.write(file.file.read())

                # Guarda la ruta del archivo en la base de datos
                paso=13
                url = f"/{ruta}/{safeFilename}.{file.filename.split('.')[-1]}"

                # determinamos si el CV del usuario existe 
                paso=14
                nRecordFileUser=  self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).count()

                if (nRecordFileUser>0):
                    paso=15
                     # existe no podemos volver a crearlo
                    result =  self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).first()
                    paso=16
                    fileUser={
                        "id":result.id,
                        "user_id":result.user_id,
                        "estado":result.estado,
                        "url":result.url,
                        "created":result.created.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated":result.updated.strftime("%Y-%m-%d %H:%M:%S"),
                        "creator_user":result.creator_user,
                        "updater_user":result.updater_user 
                    }
                    return ({"result":"-4","estado":"Record Found", "ContratoUser":fileUser})
                else:
                    # no existe foto del usuario podemos crearla
                    # Crea un registro en la base de datos
                    paso=17
                    newFileUser = ContratoUsuariosModel (
                        user_id = userId,
                        estado=2,
                        url = url,
                        created = ahora,
                        updated = ahora,
                        creator_user = creatorUserId,
                        updater_user= creatorUserId                      
                    )
                    self.db.add(newFileUser)
                    self.db.commit()

                    # creamos un registro en el historico de fotos
                    paso=18
                    ContratoUserController.create_historico_contrato_user (self,newFileUser, "Creación de Contrato del usuario")                    

                    #devolvemos el resultado
                    paso=19
                    newContratoUserId=newFileUser.id
                    
                    paso=20
                    nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
                    paso=21
                    if (nRecordEstatus >0):
                        #existe actualizamos
                        paso=22
                        result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,1)
                    else:
                        #no existe creamos
                        paso=23
                        #llenamos el esquema de datos de estatus inscripcion
                        estatusInscripcion=EstatusInscripcionSchema(
                            user_id = userId,
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
                            contrato=1                            
                        )
                        
                        result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)
                    
                    return ({"result":"1","estado":"foto creada","newContratoUserId": newContratoUserId})
            except ValueError as e:
                    # ocurrio un error y devolvemos el estado
                    return( {"result":"-3","cadenaError": f"Ocurrió el siguiente Error:{str(e)} Paso:{paso}"})   
        else:
            return ({"result":"-1","estado":"archivo_no permitido","Archivos Permitidos":list(permitedExtensionFilesUsers)})
        

    # metodo para editar el  contrato de usuario al servidor
    # @params creatorUserId: usuario que subio el archivo
    # @params userId: usuario al que pertenece el archivo
    # @params file: archivo que se está subiendo al archivo
    def edit_contrato_user(self,creatorUserId,userId,file):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        paso=1
        
        main_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(main_file)+"/.."  

        try:
            # declaramos la ruta de almacenaje de las fotos del usuario    
            paso=2        
            ruta = os.getenv("FILE_USERS")

            #diccionario que contiene los tipos archivos permitidos
            paso=3
            permitedExtensionFilesUsers=  os.getenv("PERMITED_EXTENSION_FILES_USERS") 
            
            #tamaño de los archivos permitidos en Megabytes 
            #este valor esta expresado en Bytes = (n/1024/1024)Mb
            paso=4
            permitedSizeFilesUsers =  int(os.getenv("MAX_PERMITED_SIZE_FILES_USERS") ) 

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                paso=5
                return( {"result":"-3","error": str(e)})


        # Guarda el archivo en el directorio "files_users"
        try:
            paso=6
            slug = os.path.splitext(file.filename)[0]
        except ValueError as e:
            paso=7
            # ocurrio un error y devolvemos el estado
            return( {"result":"-3","error": str(e)})            

        # Reemplaza los caracteres no deseados por caracteres seguros
        paso=8
        safeFilename = re.sub(r"[^a-zA-Z0-9_-]", "_", slug)+str(uuid.uuid4())

        #path = os.path.join("files_users", file.filename)
        try:
            paso=9
            path = os.path.join(ruta, f"{safeFilename}.{file.filename.split('.')[-1]}")
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","cadenaError": f"Ocurrió el siguiente Error:{str(e)} Paso:{paso}"})            

        
        #devolvemos la extensión para verificr si se puede o no guardar el archivo
        paso=10
        fileExtension=file.filename.split('.')[-1]

        #determinamos el tamaño del archivo
        file_size = file.size

        #verificamos que no exceda el tamaño máximo permitido
        if (file_size > permitedSizeFilesUsers):
            paso=11
            # El archivo es demasiado grande
            return ({"result":"-5","estado":f"El archivo es demasiado grande, tamaño máximo permitido {(permitedSizeFilesUsers/1024/1024)}Mb"})

        if (fileExtension in permitedExtensionFilesUsers):
            try:
                #guardamos el archivo
                paso=12
                with open(path, "wb") as f:
                    f.write(file.file.read())

                # Guarda la ruta del archivo en la base de datos
                paso=13
                url = f"/{ruta}/{safeFilename}.{file.filename.split('.')[-1]}"

                # determinamos si el CV del usuario existe 
                paso=14
                nRecordFileUser=  self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).count()

                if (nRecordFileUser>0):
                    paso=15
                    #existe actualizamos el url                     
                    contratoUserExists =  self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).first()

                    archivoEliminar=app_dir+contratoUserExists.url

                    paso=16
                    #creamos el registro historico del contrato
                    result2=ContratoUserController.create_historico_contrato_user(self,contratoUserExists,'Actualizacion del contrato del usuario')

                    #actualizamos los datos
                    paso=17
                    contratoUserExists.url=url
                    contratoUserExists.updater_user=creatorUserId
                    contratoUserExists.updated=ahora

                    paso=18
                    self.db.commit()

                    paso=20
                    os.remove(archivoEliminar)          

                    paso=21
                    data=contratoUserExists.to_dict()          
                    paso=22
                    return ({"result":"1","estado":"Contrato Actualizado", "contratoUser":data})
                else:
                    return ({"result":"-1","estado":"El usuario no tieene contrato"})
                
            except ValueError as e:
                    # ocurrio un error y devolvemos el estado
                    return( {"result":"-3","cadenaError": f"Ocurrió el siguiente Error:{str(e)} Paso:{paso}"})   
        else:
            return ({"result":"-4","estado":"archivo_no permitido","permitidos":list(permitedExtensionFilesUsers)})        
        

    # metodo para consultar un archivo por Id
    # @params fileId: id del archivo del Usuario que se desea consultar
    def get_contrato_user(self, userId):

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).count()

        main_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(main_file)+"/.."

        '''
            Estructura de la tabla
            id	bigint(20) AI PK
            user_id	bigint(20)
            nombre	varchar(250)
            url	text
            created	datetime
            updated	datetime
            creator_user	bigint(20)
            updater_user	bigint(20)        
        '''
        if (nRecordFileUser>0):
            # Obtener la dirección del servidor.
            result= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).first()

            resultado={
                "id":result.id,
                "user_id":result.user_id,
                "estado":result.estado,
                "url":result.url,
                "created":result.created,
                "updated": result.updated,
                "creator_user":result.creator_user,
                "updater_user":result.updater_user,
                "absolute_path":"file://"+app_dir+result.url
            }
            if (result):
                return ({"result":"1","estado":"Contrato encontrada","resultado":resultado })                            
            else:
                return ({"result":"-1","estado":"Contrato no encontrada","userId":userId })   
        else:
            return ({"result":"-1","estado":"Contrato no encontrada","userId":userId })    


    # esta función permite la eliminación de un contrato de usuario
    # @param picId: Id que representa la clave primaria de la foto que se eliminará
    def delete_contrato_user(self,userId,creatorUserId):
        # buscamos el registro
        nRecordFileUser = self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).count()

        main_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(main_file)+"/.."        

        if (nRecordFileUser > 0):
            try:
                
                filePicExists= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).first()
                
                # creamos el historico de  la eliminacion
                ContratoUserController.create_historico_contrato_user(self,filePicExists,"Se eliminó un Contrato de Usuario")

                ruta_archivo=app_dir+"/"+filePicExists.url

                self.db.delete(filePicExists)
                self.db.commit()

                os.remove(ruta_archivo)
                
                # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
                paso=20
                nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
                paso=21
                if (nRecordEstatus >0):
                    #existe actualizamos
                    paso=22
                    result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,1)
                else:
                    #no existe creamos
                    paso=23
                    #llenamos el esquema de datos de estatus inscripcion
                    estatusInscripcion=EstatusInscripcionSchema(
                        user_id = userId,
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
                    
                    result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)
                        
                return ({"result":"1","estado":"Archivo eliminado"})                
            except OSError as error:
                return({"result":"-3","estado":f"Error al eliminar el archivo: {error} ruta {ruta_archivo}"})
        else:
            return ({"result":"-1","estado":"Archivo no encontrado" })  

        
    # metodo para descartar el Contrato del usuario
    # @params fileId: id del archivo del Usuario que se desea consultar
    def skip_contrato_user(self,userId,creatorUserId):
        ahora = datetime.datetime.now()

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).count()

        main_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(main_file)+"/.."

        '''
            Estructura de la tabla
            id	bigint(20) AI PK
            user_id	bigint(20)
            nombre	varchar(250)
            url	text
            created	datetime
            updated	datetime
            creator_user	bigint(20)
            updater_user	bigint(20)        
        '''
        if (nRecordFileUser>0):
            try:
                # Obtener la dirección del servidor.
                cvUsersExists= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).first()
                
                if (cvUsersExists):
                    # creamos el registro historico del CV
                    ContratoUserController.create_historico_contrato_user(self,cvUsersExists,"Se descartó del Contrato del usuario")
                    
                    # actualizamos el estado del cv
                    cvUsersExists.estado=3
                    cvUsersExists.url=''
                    cvUsersExists.updated=ahora
                    cvUsersExists.updater_user=creatorUserId
                    
                    #confirmamos los cambios en la Bd
                    self.db.add(cvUsersExists)
                    self.db.commit()                    
                    
                    resultado={
                        "id":cvUsersExists.id,
                        "user_id":cvUsersExists.user_id,
                        "estado":cvUsersExists.estado,
                        "url":cvUsersExists.url,
                        "created":str(cvUsersExists.created),
                        "updated": str(cvUsersExists.updated),
                        "creator_user":cvUsersExists.creator_user,
                        "updater_user":cvUsersExists.updater_user
                    }

                    # actualizamos el estatus del contrato del usuario (se coloca a 1 para indicar que no tiene contrato)
                # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
                paso=20
                nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
                paso=21
                if (nRecordEstatus >0):
                    #existe actualizamos
                    paso=22
                    result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,1)
                else:
                    #no existe creamos
                    paso=23
                    #llenamos el esquema de datos de estatus inscripcion
                    estatusInscripcion=EstatusInscripcionSchema(
                        user_id = userId,
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
                    
                    result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)
                
                    return ({"result":"1","estado":"Contrato descartado","resultado":resultado })                            
  
            except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})
        else:
            # se crea un registro de descarte de curriculum
            newFileUser = ContratoUsuariosModel (
                user_id = userId,
                estado=3,
                url = '',
                created = ahora,
                updated = ahora,
                creator_user = creatorUserId,
                updater_user= creatorUserId                      
                )
            self.db.add(newFileUser)
            self.db.commit()
            
            ContratoUserController.create_historico_contrato_user(self,newFileUser,"Descartar carga de Contrato usuario")
            
            resultado={
                "id":newFileUser.id,
                "user_id":newFileUser.user_id,
                "estado":newFileUser.estado,
                "url":newFileUser.url,
                "created":str(newFileUser.created),
                "updated": str(newFileUser.updated),
                "creator_user":newFileUser.creator_user,
                "updater_user":newFileUser.updater_user
        
            }           
            
            # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
            paso=20
            nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            paso=21
            if (nRecordEstatus >0):
                #existe actualizamos
                paso=22
                result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,1)
            else:
                #no existe creamos
                paso=23
                #llenamos el esquema de datos de estatus inscripcion
                estatusInscripcion=EstatusInscripcionSchema(
                    user_id = userId,
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
                    contrato=1                            
                )
                
                result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)             
        
        return ({"result":"1","estado":"Contrato descartado","resultado":resultado })           
        

   # metodo para activar el CV del usuario
    # @params fileId: id del archivo del Usuario que se desea consultar
    def activate_contrato_user(self,userId,creatorUserId):
        ahora = datetime.datetime.now()

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).count()

        main_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(main_file)+"/.."

        '''
            Estructura de la tabla
            id	bigint(20) AI PK
            user_id	bigint(20)
            nombre	varchar(250)
            url	text
            created	datetime
            updated	datetime
            creator_user	bigint(20)
            updater_user	bigint(20)        
        '''
        if (nRecordFileUser>0):
            try:
                # Obtener la dirección del servidor.
                cvUsersExists= self.db.query(ContratoUsuariosModel).filter(ContratoUsuariosModel.user_id==userId).first()
                
                if (cvUsersExists):
                    # creamos el registro historico del Contrato
                    ContratoUserController.create_historico_contrato_user(self,cvUsersExists,"Se activo el Contrato del usuario")
                    
                    # actualizamos el estado del cv
                    cvUsersExists.estado=1
                    cvUsersExists.url=''
                    cvUsersExists.updated=ahora
                    cvUsersExists.updater_user=creatorUserId
                    
                    #confirmamos los cambios en la Bd
                    self.db.add(cvUsersExists)
                    self.db.commit()                    
                    
                    resultado={
                        "id":cvUsersExists.id,
                        "user_id":cvUsersExists.user_id,
                        "estado":cvUsersExists.estado,
                        "url":cvUsersExists.url,
                        "created":str(cvUsersExists.created),
                        "updated": str(cvUsersExists.updated),
                        "creator_user":cvUsersExists.creator_user,
                        "updater_user":cvUsersExists.updater_user
                    }

                # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
                paso=20
                nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
                paso=21
                if (nRecordEstatus >0):
                    #existe actualizamos
                    paso=22
                    result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,0)
                else:
                    #no existe creamos
                    paso=23
                    #llenamos el esquema de datos de estatus inscripcion
                    estatusInscripcion=EstatusInscripcionSchema(
                        user_id = userId,
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
                    
                    result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)

                    return ({"result":"1","estado":"Contrato activado","resultado":resultado })                            
  
            except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})
        else:
            # se crea un registro de activacion de contrato
            newFileUser = ContratoUsuariosModel (
                user_id = userId,
                estado=1,
                url = '',
                created = ahora,
                updated = ahora,
                creator_user = creatorUserId,
                updater_user= creatorUserId                      
                )
            self.db.add(newFileUser)
            self.db.commit()
            
            ContratoUserController.create_historico_contrato_user(self,newFileUser,"Activar carga de Contrato usuario")
            
            resultado={
                "id":newFileUser.id,
                "user_id":newFileUser.user_id,
                "estado":newFileUser.estado,
                "url":newFileUser.url,
                "created":str(newFileUser.created),
                "updated": str(newFileUser.updated),
                "creator_user":newFileUser.creator_user,
                "updater_user":newFileUser.updater_user
        
            }            
            
            # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
            paso=20
            nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            paso=21
            if (nRecordEstatus >0):
                #existe actualizamos
                paso=22
                result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,0)
            else:
                #no existe creamos
                paso=23
                #llenamos el esquema de datos de estatus inscripcion
                estatusInscripcion=EstatusInscripcionSchema(
                    user_id = userId,
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
                
                result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)            
            
            return ({"result":"1","estado":"CV activado","resultado":resultado })         
        
        
    # metodo para crear el preregistro de los Contrato de los usuarios
    # @params userId: Usuario al que se le crea el preregistro de CV
    # @params creatorUserId: usuario del sistema que crea al registro
    def create_preregistro_contrato(self,userId,creatorUserId):
        paso=1
        ahora=datetime.datetime.now()
        try:
            paso=2
            '''
            id = Column(BIGINT, primary_key=True, autoincrement=True)
            user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True)
            url = Column(TEXT, nullable=False)
            created = Column (DateTime, nullable=False) #datetime NOT NULL,    
            updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
            creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
            updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 
            '''
            newContratoUser=ContratoUsuariosModel(
                user_id=userId,
                url='',
                created=ahora,
                updated=ahora,
                creator_user=creatorUserId,
                updater_user=creatorUserId
            )
            paso=3
            self.db.add(newContratoUser)
            paso=4
            self.db.commit()
            
            #creamos el registro historico del contrato
            paso=5
            ContratoUserController.create_historico_contrato_user(self,newContratoUser,"Se creo el preregistro del Contrato del usuario")

            # actualizamos el estatus del contrato del usuario (se coloca a 0 para indicar que no tiene contrato)
            paso=20
            nRecordEstatus=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            paso=21
            if (nRecordEstatus >0):
                #existe actualizamos
                paso=22
                result2=EstatusInscripcionUserController.update_estatus_contrato(self,userId,creatorUserId,0)
            else:
                #no existe creamos
                paso=23
                #llenamos el esquema de datos de estatus inscripcion
                estatusInscripcion=EstatusInscripcionSchema(
                    user_id = userId,
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
                
                result2=EstatusInscripcionUserController.create_estatus_inscripcion(self,estatusInscripcion,creatorUserId)
            
            return( {"result":"1","estado":"Se creo el preregistro del Contrato del usuario"})       
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})            