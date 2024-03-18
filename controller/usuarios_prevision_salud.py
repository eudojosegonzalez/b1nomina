'''
Este archivo contiene las funciones básicas del CRUD de Prevision Salud del Usuario
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
	__tablename__="UsuariosPrevisionSalud"
	id = Column(BIGINT, primary_key=True, autoincrement=True)
	prevision_salud_id = Column(BIGINT,  ForeignKey("PrevisionSalus.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
	user_id = Column(BIGINT,  ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
	pactado= Column(NUMERIC (18,4),nullable=False)   
	tipo_contrato= Column(INTEGER,nullable=False)   
	created = Column (DateTime, nullable=False) #datetime NOT NULL,    
	updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
	creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
	updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    prevision_salud_id : int = Field(ge=1, le=100)
    user_id : int = Field(ge=1, le=2000)
    pactado : float    
    tipo_contrato : int = Field (ge=1, le=2)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prevision_salud_id" : 1,
                    "user_id" : 1,
                    "pactado" : 0.00 ,                  
                    "tipo_contrato" : 1,

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
from models.usuario_prevision_salud import UsuariosPrevisionSalud as UsuariosPrevisionSaludModel
from models.historico_usuario_prevision_salud import HistoricoUsuariosPrevisionSalud as HistoricoUsuariosPrevisionSaludModel


# importamos el schema de datos
from schemas.usuarios_prevision_salud import UsuariosPrevicionSalud as UsuariosPrevicionSaludSchema


# esto representa los metodos implementados en la tabla
class UsuariosPrevisionSaludController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de la ubicacion del usuario
    #@param contactUser: Modelo del registro de contaco del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_usuario_prevision_salud (self, usuariosPrevisionSalud:UsuariosPrevisionSaludModel, observacion:str):
        # determinamos la fecha/hora actual
        paso=1
        ahora = datetime.datetime.now()

        try:
            paso=2
            #creamos la instancia la nuevo registro del historico
            newHistoricoUsuariosPrevisionSalud= HistoricoUsuariosPrevisionSaludModel(
                usuario_prevision_salud_id=usuariosPrevisionSalud.id,
                prevision_salud_id=usuariosPrevisionSalud.prevision_salud_id,
                user_id=usuariosPrevisionSalud.user_id,
                pactado=usuariosPrevisionSalud.pactado,
                tipo_contrato=usuariosPrevisionSalud.tipo_contrato,
                created=usuariosPrevisionSalud.created,
                updated=usuariosPrevisionSalud.updated,
                creator_user=usuariosPrevisionSalud.creator_user,
                updater_user=usuariosPrevisionSalud.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            paso=3
            self.db.add(newHistoricoUsuariosPrevisionSalud)
            paso=4
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:   
            return( {"result":False,"cadenaError": f"Error {str(e)} paso {paso}"})   
        

    #metodo para insertar  los datos de Previsalud del Usuario del usuario 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params usuarioPrevisionSalud: esquema de los datos de Prevision Saludos del usuario que se desea insertar       
    def create_usuario_prevision_salud(self, userCreatorId:int , usuarioPrevisionSalud:UsuariosPrevicionSaludSchema):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()
        
        # determinamos el user_id de los datos enviados
        paso=2
        usuarioPrevisionSaludId=usuarioPrevisionSalud.user_id

        # buscamos si este usuario ya tiene un dato de contacto
        paso=3        
        nRecord = self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id == usuarioPrevisionSaludId).count()
        
        if (nRecord > 0):
            paso=4
            # el contacto del usuario ya existe no puede volver a crearlo
            usuarioPrevisionSaludId=self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id == usuarioPrevisionSaludId).first()            
            return ({"result":"-2","estado":"El usuario ya tiene un registro de Prevision Salud","data": usuarioPrevisionSaludId })

        # no existe el contacto del usuario, procedemos a insertar el registro
        try:
            paso=5
            newUsuarioPrevisionSalud=UsuariosPrevisionSaludModel (
                prevision_salud_id=usuarioPrevisionSalud.prevision_salud_id,
                user_id=usuarioPrevisionSalud.user_id,
                pactado=usuarioPrevisionSalud.pactado,
                tipo_contrato=usuarioPrevisionSalud.tipo_contrato,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )
            paso=6 
            self.db.add(newUsuarioPrevisionSalud)
            paso=7
            self.db.commit()

            #creamos el registro historico de AFP del usuario
            paso=8
            UsuariosPrevisionSaludController.create_historico_usuario_prevision_salud(self,newUsuarioPrevisionSalud,"Se creó la data de AFP del usuario")
            data ={
                "id":newUsuarioPrevisionSalud.id,
                "user_id":newUsuarioPrevisionSalud.user_id,
                "pactado":str(newUsuarioPrevisionSalud.pactado),
                "tipo_contrato":newUsuarioPrevisionSalud.tipo_contrato,
                "created":newUsuarioPrevisionSalud.created.strftime("%Y-%m-%d %H:%M:%S"),
                "updated":newUsuarioPrevisionSalud.updated.strftime("%Y-%m-%d %H:%M:%S"),
                "creator_user":newUsuarioPrevisionSalud.creator_user,
                "updater_user":newUsuarioPrevisionSalud.updater_user
                    
            }
            return ({"result":"1","estado":"creado","data":data})
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
    
    
    #metodo para actualizar los datos AFP del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_usuario_prevision_salud(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        paso=1
        nRecord = self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                paso=2
                usuarioAPrevisionSaludExists = self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id == userId).first()      
                data ={
                    "id":usuarioAPrevisionSaludExists.id,
                    "user_id":usuarioAPrevisionSaludExists.user_id,
                    "pactado":str(usuarioAPrevisionSaludExists.pactado),
                    "tipo_contrato":usuarioAPrevisionSaludExists.tipo_contrato,
                    "created":usuarioAPrevisionSaludExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":usuarioAPrevisionSaludExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":usuarioAPrevisionSaludExists.creator_user,
                    "updater_user":usuarioAPrevisionSaludExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos de AFP del usuario","data":data})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
        

    #metodo para actualizar los datos AFP del usuario
    # @userId : id el usuario al cual se le esta actualizando la data del AFP
    # @userUpdaterId: Id del usuario que está actualizando el registro
    # @params usuarioAFP: esquema de los datos del AFP del usuario que se desea actualizar   
   
    def update_usuario_prevision_salud(self, userUpdaterId:int, usuarioPrevisionSalud:UsuariosPrevicionSaludSchema, userId : int):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()

        # buscamos si este usuario ya tiene un dato de AFP
        paso=2
        nRecord = self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el AFP del usuario, procedemos a actualizar el registro
            try:
                paso=3
                #extraemos los datos de la ubicacion para guardarlos en el historico
                usuarioPrevisionSaludExists = self.db.query(UsuariosPrevisionSaludModel).filter(UsuariosPrevisionSaludModel.user_id == userId).first()     

                #creamos el registro historico de ubicacion del usuario
                paso=4
                self.create_historico_usuario_prevision_salud(usuarioPrevisionSaludExists,"Se actualizó la data de AFP del usuario")

                #guardamos las modificaciones en la tabla de ubicacion del usuario

                paso=5
                usuarioPrevisionSaludExists.prevision_salud_id=usuarioPrevisionSalud.prevision_salud_id,
                usuarioPrevisionSaludExists.pactado=usuarioPrevisionSalud.pactado,
                usuarioPrevisionSaludExists.tipo_contrato=usuarioPrevisionSalud.tipo_contrato,
                usuarioPrevisionSaludExists.updated=ahora
                usuarioPrevisionSaludExists.updater_user=userUpdaterId
                
                # confirmamos los cambios.
                paso=6
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                data ={
                    "id":usuarioPrevisionSaludExists.id,
                    "user_id":usuarioPrevisionSaludExists.user_id,
                    "pactado":str(usuarioPrevisionSaludExists.pactado),
                    "tipo_contrato":usuarioPrevisionSaludExists.tipo_contrato,
                    "created":usuarioPrevisionSaludExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":usuarioPrevisionSaludExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":usuarioPrevisionSaludExists.creator_user,
                    "updater_user":usuarioPrevisionSaludExists.updater_user
                }
                return ({"result":"1","estado":"Se actualizaron los datos de AFP  del usuario","data":data})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
    


    #metodo para listar los datos historicos de AFP del Usuario
    # @params userId: Id del usuario que se esta consultando
    def list_history_usuario_prevision_salud(self,userId:int):

        # buscamos si este usuario ya tiene un dato de contacto
        nRecord = self.db.query(HistoricoUsuariosPrevisionSaludModel).filter(HistoricoUsuariosPrevisionSaludModel.user_id == userId).count()
        
        if (nRecord == 0):
            # el contacto del usuario no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe el contacto del usuario, procedemos a actualizar el registro
            try:
                listHistoryUsarioPrevisionSalud = self.db.query(HistoricoUsuariosPrevisionSaludModel).filter(HistoricoUsuariosPrevisionSaludModel.user_id == userId).all()                  
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se consiguieron los datos históricos de AFP del usuario","data": listHistoryUsarioPrevisionSalud})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     