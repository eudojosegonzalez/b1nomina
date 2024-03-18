'''
Este archivo contiene las funciones básicas del CRUD de AFP del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="UsuariosAFP"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    jubilado_afp= Column (BIGINT,nullable=False)
    afp_id = Column(BIGINT,  ForeignKey("afp.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)  
    ahorro_afp2 = Column(NUMERIC (13,4),nullable=True)  
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    user_id : int = Field(ge=1, le=2000)
    afp_id : int = Field (ge=1, le=100)
    jubilado_afp : int = Field(ge=0,le=1)
    ahorro_afp2 : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "afp_id" : 1,
                    "jubilado_afp" : 0,
                    "ahorro_afp2" : 0.00
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


import datetime


# importamos el modelo de la base de datos
from models.usuario_afp import UsuariosAFP as UsuariosAFPModel
from models.historico_usuario_afp import HistoricoUsuariosAFP as HistoricoUsuariosAFPModel


# importamos el schema de datos
from schemas.usuarios_afp import UsuariosAFP as UsuariosAFPSchema


# esto representa los metodos implementados en la tabla
class UsuariosAFPController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de la ubicacion del usuario
    #@param contactUser: Modelo del registro de contaco del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_usuario_afp (self, usuarioAFP:UsuariosAFPModel, observacion:str):
        # determinamos la fecha/hora actual
        paso=1
        ahora = datetime.datetime.now()

        try:
            paso=2
            #creamos la instancia la nuevo registro del historico
            newHistoricoUsuariosAFP= HistoricoUsuariosAFPModel(
                usuarios_afp_id=usuarioAFP.id,
                user_id=usuarioAFP.user_id,     
                jubilado_afp=usuarioAFP.jubilado_afp,
                afp_id=usuarioAFP.ahorro_afp2,
                ahorro_afp2=usuarioAFP.ahorro_afp2,
                created=usuarioAFP.created,
                updated=usuarioAFP.updated,
                creator_user = usuarioAFP.creator_user,
                updater_user=usuarioAFP.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            paso=3
            self.db.add(newHistoricoUsuariosAFP)
            paso=4
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:   
            return( {"result":False,"cadenaError": f"Error {str(e)} paso {paso}"})   
        

    #metodo para insertar  los datos de contacto del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params ubicacionUsuario: esquema de los datos de contacto del usuario que se desea insertar       
    def create_usuario_afp(self, userCreatorId:int , usuarioAFP:UsuariosAFPSchema):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        paso=2
        usuarioAFPId=usuarioAFP.user_id

        # buscamos si este usuario ya tiene un dato de contacto
        paso=3        
        nRecord = self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id == usuarioAFPId).count()
        
        if (nRecord > 0):
            paso=4
            # el contacto del usuario ya existe no puede volver a crearlo
            usuarioAFPExists=self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id == usuarioAFPId).first()            
            return ({"result":"-2","estado":"El usuario ya tiene un registro AFP","usuarioAFP": usuarioAFPExists })

        # no existe el contacto del usuario, procedemos a insertar el registro
        try:
            paso=5
            newusuarioAFP=UsuariosAFPModel (
                user_id=usuarioAFP.user_id,
                jubilado_afp=usuarioAFP.jubilado_afp,
                afp_id=usuarioAFP.afp_id,
                ahorro_afp2=usuarioAFP.ahorro_afp2,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )
            paso=6 
            self.db.add(newusuarioAFP)
            paso=7
            self.db.commit()

            #creamos el registro historico de AFP del usuario
            paso=8
            UsuariosAFPController.create_historico_usuario_afp(self,newusuarioAFP,"Se creó la data de AFP del usuario")
            data ={
                "id":newusuarioAFP.id,
                "user_id":newusuarioAFP.user_id,
                "jubilado_afp":newusuarioAFP.jubilado_afp,
                "afp_id":newusuarioAFP.afp_id,
                "ahorro_afp2":newusuarioAFP.ahorro_afp2,
                "created":newusuarioAFP.created.strftime("%Y-%m-%d %H:%M:%S"),
                "updated":newusuarioAFP.updated.strftime("%Y-%m-%d %H:%M:%S"),
                "creator_user":newusuarioAFP.creator_user,
                "updater_user":newusuarioAFP.updater_user
                    
            }
            return ({"result":"1","estado":"creado","UsuarioAFP":data})
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
    
    
    #metodo para actualizar los datos AFP del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_usuario_afp(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        paso=1
        nRecord = self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                paso=2
                usuarioAFPExists = self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id == userId).first()      
                data ={
                    "id":usuarioAFPExists.id,
                    "user_id":usuarioAFPExists.user_id,
                    "jubilado_afp":usuarioAFPExists.jubilado_afp,
                    "afp_id":usuarioAFPExists.afp_id,
                    "ahorro_afp2":str(usuarioAFPExists.ahorro_afp2),
                    "created":usuarioAFPExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":usuarioAFPExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":usuarioAFPExists.creator_user,
                    "updater_user":usuarioAFPExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos de AFP del usuario","UsuarioAFP":data})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
        

    #metodo para actualizar los datos AFP del usuario
    # @userId : id el usuario al cual se le esta actualizando la data del AFP
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params usuarioAFP: esquema de los datos del AFP del usuario que se desea actualizar   
   
    def update_usuario_afp(self, userUpdaterId:int, usuarioAFP:UsuariosAFPSchema, userId : int):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()

        # buscamos si este usuario ya tiene un dato de AFP
        paso=2
        nRecord = self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el AFP del usuario, procedemos a actualizar el registro
            try:
                paso=3
                #extraemos los datos de la ubicacion para guardarlos en el historico
                usuarioAFPExists = self.db.query(UsuariosAFPModel).filter(UsuariosAFPModel.user_id == userId).first()     

                #creamos el registro historico de ubicacion del usuario
                paso=4
                self.create_historico_usuario_afp(usuarioAFPExists,"Se actualizó la data de AFP del usuario")

                #guardamos las modificaciones en la tabla de ubicacion del usuario

                paso=5
                usuarioAFPExists.jubilado_afp=usuarioAFP.jubilado_afp,
                usuarioAFPExists.afp_id=usuarioAFP.afp_id,
                usuarioAFPExists.ahorro_afp2=usuarioAFP.ahorro_afp2
                usuarioAFPExists.updated=ahora
                usuarioAFPExists.updater_user=userUpdaterId
                
                # confirmamos los cambios.
                paso=6
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                data ={
                    "id":usuarioAFPExists.id,
                    "user_id":usuarioAFPExists.user_id,
                    "jubilado_afp":usuarioAFPExists.jubilado_afp,
                    "afp_id":usuarioAFPExists.afp_id,
                    "ahorro_afp2":str(usuarioAFPExists.ahorro_afp2),
                    "created":usuarioAFPExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":usuarioAFPExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":usuarioAFPExists.creator_user,
                    "updater_user":usuarioAFPExists.updater_user
                }
                return ({"result":"1","estado":"Se actualizaron los datos de AFP  del usuario","UsuarioAFP":data})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
    


    #metodo para listar los datos historicos de AFP del Usuario
    # @params userId: Id del usuario que se esta consultando
    def list_history_usuario_afp(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(HistoricoUsuariosAFPModel).filter(HistoricoUsuariosAFPModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                listHistoryusuarioAFP = self.db.query(HistoricoUsuariosAFPModel).filter(HistoricoUsuariosAFPModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos históricos de AFP del usuario","listHistoryUsarioAFP": listHistoryusuarioAFP})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     