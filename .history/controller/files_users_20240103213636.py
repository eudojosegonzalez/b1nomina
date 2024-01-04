'''
Este archivo contiene las funciones básicas del CRUD del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
 
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
from models.files_users import ArchivosUsuarios as ArchivosUsuariosModel



# esto representa los metodos implementados en la tabla
class FilesUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    # metodo para subir archivos de usuarios al servidor
    # @params creatorUserId: usuario que subio el archivo
    # @params userId: usuario al que pertenece el archivo
    # @params file: archivo que se está subiendo al archivo
    def upload_file_user(self,creatorUserId,userId,file):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        try:
            # declaramos la ruta de almacenaje de archivos
            ruta = os.getenv("FILE_USERS")

            #diccionario que contiene los tipos archivos permitidos
            permitedExtensionFilesUsers=  os.getenv("PERMITED_EXTENSION_FILES_USERS") 


            #tamaño de los archivos permitidos en Megabytes 
            #este valor esta expresado en Bytes = (n/1024/1024)Mb
            permitedSizeFilesUsers =  int(os.getenv("MAX_PERMITED_SIZE_FILES_USERS") )

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})
        

        # Guarda el archivo en el directorio "files_users"
        try:        
            slug = os.path.splitext(file.filename)[0]
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})
        
        # Reemplaza los caracteres no deseados por caracteres seguros
        safeFilename = re.sub(r"[^a-zA-Z0-9_-]", "_", slug)+str(uuid.uuid4())

        #path = os.path.join("files_users", file.filename)
        path = os.path.join(ruta, f"{safeFilename}.{file.filename.split('.')[-1]}")
        
        #devolvemos la extensión para verificr si se puede o no guardar el archivo
        fileExtension=file.filename.split('.')[-1]

        #creamos el nombre final del archivo
        nombreFinal=safeFilename+"."+fileExtension


        # determinmos el tamaño del archivo
        file_size = file.size

        #validamos que np exede el tamaño maximo permitido
        if (file_size > permitedSizeFilesUsers):
            # El archivo es demasiado grande
            return ({"result":"-2","estado":f"El archivo es demasiado grande, tamaño máximo permitido {(permitedSizeFilesUsers/1024/1024)}Mb"})

        if (fileExtension in permitedExtensionFilesUsers):
            try:
                #guardamos el archivo
                with open(path, "wb") as f:
                    f.write(file.file.read())

                # Guarda la ruta del archivo en la base de datos
                url = f"/{ruta}/{safeFilename}.{file.filename.split('.')[-1]}"

                # Crea un registro en la base de datos
                newFileUser = ArchivosUsuariosModel (
                    user_id = userId,
                    nombre = nombreFinal,
                    url = url,
                    created = ahora,
                    updated = ahora,
                    creator_user = creatorUserId,
                    updater_user= creatorUserId                      
                )
                self.db.add(newFileUser)
                self.db.commit()

                #devolvemos el resultado
                newFileUserId=newFileUser.id
                return ({"result":"1","estado":"archivo_creado","newFileUserId":newFileUserId})
            except ValueError as e:
                    # ocurrio un error y devolvemos el estado
                    return( {"result":"-3","error": str(e)})
        else:
            return ({"result":"-1","estado":"archivo_no permitido","Archivos Permitidos":list(permitedExtensionFilesUsers)})


    # metodo para consultar un archivo por Id
    # @params fileId: id del archivo del Usuario que se desea consultar
    def get_file_user(self, fileId):

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(ArchivosUsuariosModel).filter(ArchivosUsuariosModel.id==fileId).count()

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
            result= self.db.query(ArchivosUsuariosModel).filter(ArchivosUsuariosModel.id==fileId).first()

            resultado={
                "id":result.id,
                "user_id":result.user_id,
                "nombre":result.nombre,
                "url":result.url,
                "created":result.created,
                "updated": result.updated,
                "creator_user":result.creator_user,
                "updater_user":result.updater_user,
                "absolute_path":"file://"+app_dir+result.url
            }
            if (result):
                return ({"result":"1","estado":"Archivo encontrado","resultado":resultado })                            
            else:
                return ({"result":"-1","estado":"Archivo no encontrado","fileId":fileId })   
        else:
            return ({"result":"-1","estado":"Archivo no encontrado","fileId":fileId })    


        '''# verificamos que el usuario tenga archivos registrados bajo su ID
        nRecordFilesUser= self.db.query(ArchivosUsuariosModel).filter(ArchivosUsuariosModel.user_id == userId).count()

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
        
        if (nRecordFilesUser > 0):
            try:
                # Buscamos los archivos del usuario
                consulta = self.db.query(ArchivosUsuariosModel).filter(ArchivosUsuariosModel.user_id == userId)
                ''' resultado={
                    "id":result.id,
                    "user_id":result.user_id,
                    "nombre":result.nombre,
                    "url":result.url,
                    "created":result.created,
                    "updated": result.updated,
                    "creator_user":result.creator_user,
                    "updater_user":result.updater_user,
                    "absolute_path":"file://"+app_dir+result.url
                }'''
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                resultado=consulta.all()            
                if (resultado):
                    return ({"result":"1","estado":"Archivo encontrado","resultado":resultado })                            
                else:
                    return ({"result":"-1","estado":"Archivo no encontrado","userId":userId })   
            except ValueError as e:
                    # ocurrio un error y devolvemos el estado
                    return( {"result":"-3","error": str(e)})
        else:
            return ({"result":"-1","estado":"Archivo no encontrado","userId":userId })  ''' 