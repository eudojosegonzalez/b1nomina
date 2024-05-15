'''
Este archivo contiene las funciones básicas del CRUD de Bancarios del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
     __tablename__="ColacionUsuarios"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    movilizacion = Column(NUMERIC(18,4), nullable=False)
    colacion  = Column(NUMERIC(18,4), nullable=False)
    familiar  = Column(NUMERIC(18,4), nullable=False) 
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id: int = Field (ge=1,lt=1000)
    user_id: int = Field (ge=1,lt=20000)
    movilizacion : float
    colacion  : float
    familiar  : float    
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'sociedad_id': 1,
                    'user_id': 1,
                    'movilizacion' : 0,
                    'colacion'  : 0,
                    'familiar'  : 0  
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
from models.colacion_usuarios import ColacionUsuarios as ColacionUsuariosModel
from models.historico_colacion_usuarios import HistoricoColacionUsuarios as HistoricoColacionUsuariosModel



# importamos el schema de datos
from schemas.colacion_usuarios import ColacionUser as ColacionUserSchema


# esto representa los metodos implementados en la tabla
class ColacionUsuariosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de datos bancarios del usuario
    #@param historicoBancarioUser: Modelo del registro de Bancarios del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_colacion_user (self, colacionUsuarios:ColacionUsuariosModel, observacion:str):
     # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:

            #creamos la instancia la nuevo registro del historico
            newHistoricoBancarioUser= HistoricoColacionUsuariosModel(
                colacion_usuario_id=colacionUsuarios.id,
                sociedad_id=colacionUsuarios.sociedad_id,
                user_id=colacionUsuarios.user_id,     
                movilizacion=colacionUsuarios.movilizacion,
                colacion=colacionUsuarios.colacion,
                familiar=colacionUsuarios.familiar,                
                created=colacionUsuarios.created,
                updated=colacionUsuarios.updated,
                creator_user = colacionUsuarios.creator_user,
                updater_user=colacionUsuarios.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoBancarioUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de colacion del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_colacion_user(self, colacionUsuario:ColacionUserSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        # determinamos el user_id de los datos enviados
        userId=colacionUsuario.user_id

        # buscamos si existe el dato de colacion
        nRecord = self.db.query(ColacionUsuariosModel).filter(ColacionUsuariosModel.user_id == userId).count()
        
        if (nRecord > 0):
            # existen datos bancarios del usuario no puede volver a crearlos
            return ({"result":"-1","estado":"No record found"})        
        else:    
            #creamos el nuevo registro de bancarios de usuarios
            try:
                newColacionUser=ColacionUsuariosModel(
                    sociedad_id=colacionUsuario.sociedad_id,   
                    user_id=colacionUsuario.user_id,   
                    movilizacion=colacionUsuario.movilizacion,     
                    colacion=colacionUsuario.colacion,
                    familiar=colacionUsuario.familiar,                                                
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newColacionUser)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                ColacionUsuariosController.create_historico_colacion_user(self,newColacionUser,"Se creó los datos de colacion del usuario")

                newColacionId=newColacionUser.id
                return ({"result":"1","estado":"creado","newColacionId":newColacionId})
            except ValueError as e:
                return( {"result":"-1","error": str(e)})
    

    #metodo para consultar los datos de colacion del usuario 
    # @params userId: id del Usuario al cual se le estan consultadn los datos de colacion
    def get_colacion_user(self,userId:int):

        # buscamos si este usuario ya tiene datos de colacion
        nRecord = self.db.query(ColacionUsuariosModel).filter(ColacionUsuariosModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos bancarios del usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                colacionUserExits = self.db.query(ColacionUsuariosModel).filter(ColacionUsuariosModel.user_id == userId).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de colacion del usuario","data":colacionUserExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
    #metodo para actualizar los datos de colacion del usuario 
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params contactoUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def update_colacion_user(self,userUpdaterId:int ,colacionUsuario:ColacionUserSchema):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        userId=colacionUsuario.user_id

        # buscamos si existe el dato de colacion
        nRecord = self.db.query(ColacionUsuariosModel).filter(ColacionUsuariosModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de colacion
            return ({"result":"-2","estado":f"No record found {userId}"})
        else:
            # existen los datosdel banco se puede actualizar
            try:
                #extraemos los datos para guardar el histórico
                colacionUserExists = self.db.query(ColacionUsuariosModel).filter(ColacionUsuariosModel.user_id == userId).first()                  

                #creamos el registro historico de banco
                ColacionUsuariosController.create_historico_colacion_user(self,colacionUserExists,"Actualización de la data de colacion del usuario")   


                #registramnos los cambios en la tabla de colacion del usuario
                colacionUserExists.sociedad_id=colacionUserExists.sociedad_id,                
                colacionUserExists.user_id=colacionUserExists.user_id,   
                colacionUserExists.movilizacion=colacionUserExists.movilizacion,   
                colacionUserExists.colacion=colacionUserExists.colacion,                   
                colacionUserExists.familiar=colacionUserExists.familiar,                   
                colacionUserExists.updated=ahora,
                colacionUserExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de colacion del usuario","Colacion Usuario":colacionUserExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
        
            

    # metodo para listar los datos historicos de colacion del usuario 
    # @params userId:: Id del usuario que se esta consultando
    def list_history_colacion_user(self,userId):

        # buscamos si existen los datos de colacion del usuario
        nRecord = self.db.query(HistoricoColacionUsuariosModel).filter(HistoricoColacionUsuariosModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el banco no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe extraemos los datos y los enviamos
            try:
                listHistoryBancariosUser = self.db.query(HistoricoColacionUsuariosModel).filter(HistoricoColacionUsuariosModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos los registros
                return ({"result":"1","estado":"Se consiguieron los datos de colacion del usuario","data": listHistoryBancariosUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     