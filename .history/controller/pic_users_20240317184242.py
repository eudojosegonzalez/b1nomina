'''
Este archivo contiene las funciones básicas para controlas las fotos del usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="FotosUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True)
    url = Column(TEXT, nullable=False)
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
from models.pic_users import PicUsuarios as FotosUsuariosModel
from models.historico_pic_users import HistoricoPicUsuarios  as HistoricoFotosUsuariosModel


# esto representa los metodos implementados en la tabla
class PicUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de las fotos del usuario
    #@param contactUser: Modelo del registro de contaco del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_pic_user (self, fotosUsuarios: FotosUsuariosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoPicUser= HistoricoFotosUsuariosModel(
                pic_id=fotosUsuarios.id,                  
                user_id=fotosUsuarios.user_id,     
                url=fotosUsuarios.url,
                created=fotosUsuarios.created,
                updated=fotosUsuarios.updated,
                creator_user = fotosUsuarios.creator_user,
                updater_user=fotosUsuarios.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoPicUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})    
              

    # metodo para subir la foto de usuario al servidor
    # @params creatorUserId: usuario que subio el archivo
    # @params userId: usuario al que pertenece el archivo
    # @params file: archivo que se está subiendo al archivo
    def upload_pic_user(self,creatorUserId,userId,file):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        
        try:
            # declaramos la ruta de almacenaje de las fotos del usuario            
            ruta = os.getenv("PIC_USERS")

            #diccionario que contiene los tipos archivos permitidos
            permitedExtensionPicUsers=  os.getenv("PERMITED_EXTENSION_PIC_USERS") 
            
            #tamaño de los archivos permitidos en Megabytes 
            #este valor esta expresado en Bytes = (n/1024/1024)Mb
            permitedSizePicUsers =  int(os.getenv("MAX_PERMITED_SIZE_PIC_USERS") ) 

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
        try:
            path = os.path.join(ruta, f"{safeFilename}.{file.filename.split('.')[-1]}")
        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})            

        
        #devolvemos la extensión para verificr si se puede o no guardar el archivo
        fileExtension=file.filename.split('.')[-1]

        #determinamos el tamaño del archivo
        file_size = file.size

        #verificamos que no exceda el tamaño máximo permitido
        if (file_size > permitedSizePicUsers):
            # El archivo es demasiado grande
            return ({"result":"-2","estado":f"El archivo es demasiado grande, tamaño máximo permitido {(permitedSizePicUsers/1024/1024)}Mb"})

        if (fileExtension in permitedExtensionPicUsers):
            try:
                #guardamos el archivo
                with open(path, "wb") as f:
                    f.write(file.file.read())

                # Guarda la ruta del archivo en la base de datos
                url = f"/{ruta}/{safeFilename}.{file.filename.split('.')[-1]}"

                # determinamos si la foto del usuario existe 
                nRecordPicUser=  self.db.query(FotosUsuariosModel).filter(FotosUsuariosModel.user_id==userId).count()

                if (nRecordPicUser>0):
                     # existe no podemos volver a crearlo
                     result =  self.db.query(FotosUsuariosModel).filter(FotosUsuariosModel.user_id==userId).first()
                     picUser={
                        "id":result.id,
                        "user_id":result.user_id,
                        "url":result.url,
                        "created":result.created.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated":result.updated.strftime("%Y-%m-%d %H:%M:%S"),
                        "creator_user":result.creator_user,
                        "updater_user":result.updater_user 
                     }
                     return ({"result":"-4","estado":"Record Found", "picUser":picUser})
                else:
                    # no existe foto del usuario podemos crearla
                    # Crea un registro en la base de datos
                    newPicUser = FotosUsuariosModel (
                        user_id = userId,
                        url = url,
                        created = ahora,
                        updated = ahora,
                        creator_user = creatorUserId,
                        updater_user= creatorUserId                      
                    )
                    self.db.add(newPicUser)
                    self.db.commit()

                    # creamos un registro en el historico de fotos
                    self.create_historico_pic_user (newPicUser, "Creación de foto del usuario")                    

                    #devolvemos el resultado
                    newPicUserId=newPicUser.id
                    return ({"result":"1","estado":"foto creada","newPicUserId":newPicUserId})
            except ValueError as e:
                    # ocurrio un error y devolvemos el estado
                    return( {"result":"-3","error": str(e)})
        else:
            return ({"result":"-1","estado":"archivo_no permitido","Archivos Permitidos":list(permitedExtensionPicUsers)})
        

    # metodo para consultar un archivo por Id
    # @params fileId: id del archivo del Usuario que se desea consultar
    def get_pic_user(self, fileId):

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(FotosUsuariosModel).filter(FotosUsuariosModel.id==fileId).count()

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
            result= self.db.query(FotosUsuariosModel).filter(FotosUsuariosModel.id==fileId).first()

            resultado={
                "id":result.id,
                "user_id":result.user_id,
                "url":result.url,
                "created":result.created,
                "updated": result.updated,
                "creator_user":result.creator_user,
                "updater_user":result.updater_user,
                "absolute_path":"file://"+app_dir+result.url
            }
            if (result):
                return ({"result":"1","estado":"Foto encontrada","resultado":resultado })                            
            else:
                return ({"result":"-1","estado":"foto no encontrada","fileId":fileId })   
        else:
            return ({"result":"-1","estado":"foto no encontrada","fileId":fileId })    


    # esta función permite la eliminación de una foto de usuario
    # @param picId: Id que representa la clave primaria de la foto que se eliminará
    def delete_pic_user(self,userId:int):
        # buscamos el registro
        nRecordFileUser = self.db.query(FotosUsuariosModel).filter(FotosUsuariosModel.id==userId).count()

        main_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(main_file)+"/.."        

        if (nRecordFileUser > 0):
            try:
                filePicExists= self.db.query(FotosUsuariosModel).filter(FotosUsuariosModel.user_id==userId).first()

                ruta_archivo=app_dir+"/"+filePicExists.url

                os.remove(ruta_archivo)
                return ({"result":"1","estado":"Archivo eliminado"})                
            except OSError as error:
                return({"result":"-3","estado":f"Error al eliminar el archivo: {error} ruta {ruta_archivo}"})
        else:
            return ({"result":"-1","estado":"Archivo no encontrado" })  