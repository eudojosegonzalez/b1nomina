'''
Este archivo contiene las funciones básicas del CRUD de AFC del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="UsuariosAFC"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    estado = Column(BIGINT, nullable=False)
    jubiladoafp = Column(BIGINT, nullable=False)
    antiguedad= Column(BIGINT, nullable=False)
    vejez= Column(BIGINT, nullable=False)
    invalidez= Column(BIGINT, nullable=False)
    exinp= Column(BIGINT, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    user_id : int = Field(ge=1, le=2000)
    estado : int = Field(ge=0, le=1)
    jubiladoafp: int = Field(ge=0, le=1)
    antiguedad : int = Field(ge=0, le=1)
    vejez : int = Field(ge=0, le=1)
    invalidez : int = Field(ge=0, le=1)
    exinp : int = Field(ge=0, le=1)
 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "estado" : 1,
                    "jubiladoafp": 1,
                    "antiguedad" : 1,
                    "vejez" : 0,
                    "invalidez" : 0,
                    "exinp" : 0
                }
            ]
        }
    }
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime


# importamos el modelo de la base de datos
from models.usuario_afc import UsuariosAFC as UsuariosAFCModel
from models.historico_usuario_afc import HistoricoUsuariosAFC as HistoricoUsuariosAFCModel


# importamos el schema de datos
from schemas.usuarios_afc import UsuariosAFC as UsuariosAFCSchema


# esto representa los metodos implementados en la tabla
class UsuariosAFCController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de la ubicacion del usuario
    #@param contactUser: Modelo del registro de contaco del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_usuario_afc (self, usuarioAFC:UsuariosAFCModel, observacion:str):
        # determinamos la fecha/hora actual
        paso=1
        ahora = datetime.datetime.now()

        try:
            paso=2
            #creamos la instancia la nuevo registro del historico
            newHistoricoUsuariosAFC= HistoricoUsuariosAFCModel(
                usuarios_afc_id=usuarioAFC.id,
                user_id=usuarioAFC.user_id,     
                estado=usuarioAFC.estado,
                antiguedad=usuarioAFC.antiguedad,
                vejez=usuarioAFC.vejez,
                invalidez=usuarioAFC.invalidez,
                exinp=usuarioAFC.exinp,
                created=usuarioAFC.created,
                updated=usuarioAFC.updated,
                creator_user = usuarioAFC.creator_user,
                updater_user=usuarioAFC.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            paso=3
            self.db.add(newHistoricoUsuariosAFC)
            paso=4
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:   
            return( {"result":False,"cadenaError": f"Error {str(e)} paso {paso}"})   
        

    #metodo para insertar  los datos de contacto del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params ubicacionUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_usuario_afc(self, userCreatorId:int , usuarioAFC:UsuariosAFCSchema):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        paso=2
        usuarioAFCId=usuarioAFC.user_id

        # buscamos si este usuario ya tiene un dato de contacto
        paso=3        
        nRecord = self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id == usuarioAFCId).count()
        
        if (nRecord > 0):
            paso=4
            # el contacto del usuario ya existe no puede volver a crearlo
            usuarioAFCExists=self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id == usuarioAFCId).first()            
            return ({"result":"-2","estado":"El usuario ya tiene un registro AFC","usuarioAFC": usuarioAFCExists })

        # no existe el contacto del usuario, procedemos a insertar el registro
        try:
            paso=5
            newUsuarioAFC=UsuariosAFCModel (
                user_id=usuarioAFC.user_id,
                estado=usuarioAFC.estado,
                antiguedad=usuarioAFC.antiguedad,
                vejez=usuarioAFC.vejez,
                invalidez=usuarioAFC.invalidez,
                exinp=usuarioAFC.exinp,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )
            paso=6 
            self.db.add(newUsuarioAFC)
            paso=7
            self.db.commit()

            #creamos el registro historico de afc del usuario
            paso=8
            UsuariosAFCController.create_historico_usuario_afc(self,newUsuarioAFC,"Se creó la data de AFC del usuario")
            data ={
                "id":newUsuarioAFC.id,
                "user_id":newUsuarioAFC.user_id,
                "estado":newUsuarioAFC.estado,
                "antiguedad":newUsuarioAFC.antiguedad,
                "vejez":newUsuarioAFC.vejez,
                "invalidez":newUsuarioAFC.invalidez,
                "exinp":newUsuarioAFC.exinp,
                "created":newUsuarioAFC.created,
                "updated":newUsuarioAFC.updated,
                "creator_user":newUsuarioAFC.creator_user,
                "updater_user":newUsuarioAFC.updater_user
                    
            }
            return ({"result":"1","estado":"creado","UsuarioAFC":data})
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
    
    
    #metodo para actualizar los datos de ubicacion del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_usuario_afc(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        paso=1
        nRecord = self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                paso=2
                usuarioAFCExists = self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id == userId).first()      
                data ={
                    "id":usuarioAFCExists.id,
                    "user_id":usuarioAFCExists.user_id,
                    "estado":usuarioAFCExists.estado,
                    "antiguedad":usuarioAFCExists.antiguedad,
                    "vejez":usuarioAFCExists.vejez,
                    "invalidez":usuarioAFCExists.invalidez,
                    "exinp":usuarioAFCExists.exinp,
                    "created":usuarioAFCExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":usuarioAFCExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":usuarioAFCExists.creator_user,
                    "updater_user":usuarioAFCExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos de AFC del usuario","UsuarioAFC":data})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
        

    #metodo para actualizar los datos de ubicacion del usuario
    # @userId : id el usuario al cual se le esta actualizando la data del AFC
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params usuarioAFC: esquema de los datos del AFC del usuario que se desea actualizar   
   
    def update_usuario_afc(self, userUpdaterId:int, usuarioAFC:UsuariosAFCSchema, userId : int):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()

        # buscamos si este usuario ya tiene un dato de AFC
        paso=2
        nRecord = self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el AFC del usuario, procedemos a actualizar el registro
            try:
                paso=3
                #extraemos los datos de la ubicacion para guardarlos en el historico
                usuarioAFCExists = self.db.query(UsuariosAFCModel).filter(UsuariosAFCModel.user_id == userId).first()     

                #creamos el registro historico de ubicacion del usuario
                paso=4
                self.create_historico_usuario_afc(usuarioAFCExists,"Se actualizó la data de AFC del usuario")

                #guardamos las modificaciones en la tabla de ubicacion del usuario
                paso=5
                usuarioAFCExists.estado=usuarioAFC.estado
                usuarioAFCExists.antiguedad=usuarioAFC.antiguedad
                usuarioAFCExists.vejez=usuarioAFC.vejez
                usuarioAFCExists.invalidez=usuarioAFC.invalidez
                usuarioAFCExists.exinp=usuarioAFC.exinp
                usuarioAFCExists.updated=ahora
                usuarioAFCExists.updater_user=userUpdaterId
                
                # confirmamos los cambios.
                paso=6
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                data ={
                    "id":usuarioAFCExists.id,
                    "user_id":usuarioAFCExists.user_id,
                    "estado":usuarioAFCExists.estado,
                    "antiguedad":usuarioAFCExists.antiguedad,
                    "vejez":usuarioAFCExists.vejez,
                    "invalidez":usuarioAFCExists.invalidez,
                    "exinp":usuarioAFCExists.exinp,
                    "created":usuarioAFCExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":usuarioAFCExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":usuarioAFCExists.creator_user,
                    "updater_user":usuarioAFCExists.updater_user
                }
                return ({"result":"1","estado":"Se actualizaron los datos de AFC  del usuario","UsuarioAFC":usuarioAFCExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
    


    #metodo para listar los datos historicos de AFC del Usuario
    # @params userId: Id del usuario que se esta consultando
    def list_history_usuario_afc(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(HistoricoUsuariosAFCModel).filter(HistoricoUsuariosAFCModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                listHistoryUsuarioAFC = self.db.query(HistoricoUsuariosAFCModel).filter(HistoricoUsuariosAFCModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos históricos de AFC del usuario","listHistoryUsarioAFC": listHistoryUsuarioAFC})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     