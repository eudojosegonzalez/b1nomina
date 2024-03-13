'''
Este archivo contiene las funciones básicas del CRUD Campis Adicionales en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="CamposUser"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)   
    camuser1 = Column (VARCHAR(200), nullable=True)
    camuser2 = Column (VARCHAR(200), nullable=True)    
    camuser3 = Column (VARCHAR(200), nullable=True)
    camuser4 = Column (VARCHAR(200), nullable=True)    
    camuser5 = Column (VARCHAR(200), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    user_id : int = Field(ge=1, le=1000)
    camuser1 : str = Field (min_length=0, max_length=200)
    camuser2 : str = Field (min_length=0, max_length=200)
    camuser3 : str = Field (min_length=0, max_length=200)
    camuser4 : str = Field (min_length=0, max_length=200)
    camuser5 : str = Field (min_length=0, max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "user_id" : 1,
                    "camuser1" : ""  ,
                    "camuser2" : ""  ,
                    "camuser3" : ""  ,
                    "camuser4" : ""  ,
                    "camuser5" : ""  
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
from models.campos_adicioanles_usuarios import CamposUser as CamposUserModel
from models.historico_campos_adicioanles_usuarios import HistoricoCamposUser as HistoricoCamposUserModel

#importamos el esquema de datos de Sede
from schemas.campos_adicionales_user import CamposAdicionalesUser as CamposAdicionalesUserSchema



# esto representa los metodos implementados en la tabla
class CamposUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de los campos adicionales del usuario
    #@param camposUser: Modelo del registro de Campos Adicionales del Usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_campos_adicionales_user(self, camposUser: CamposUserModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoCamposUser= HistoricoCamposUserModel(
                sociedad_id=camposUser.sociedad_id,
                campos_user_id=camposUser.id,
                user_id=camposUser.user_id,
                camuser1=camposUser.camuser1,
                camuser2=camposUser.camuser2,
                camuser3=camposUser.camuser3,
                camuser4=camposUser.camuser4,
                camuser5=camposUser.camuser5,
                created=camposUser.created,
                updated=camposUser.updated,
                creator_user=camposUser.creator_user,
                updater_user=camposUser.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoCamposUser)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de los campos asicionales del usuario
    # @userCreatorId: Id del usuario que está creando el registro
    # @params camposUser: esquema de los datos de  los campos adicionales del usuario     
    def create_campos_adicionales_user(self, camposUser: CamposAdicionalesUserSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        userId=camposUser.user_id

        # contamos si existe el registro en la Bd
        nRecordNombre = self.db.query(CamposUserModel).filter(CamposUserModel.user_id == userId).count()  


        if (nRecordNombre > 0):
            # buscamos si existe el registro de campos adiciaonels del usuario
            camposUserExists=self.db.query(CamposUserModel).filter(CamposUserModel.user_id == userId).first() 

            # devolvemos el registro de campos adicionales 
            return ({"result":"-1","estado":"Este usuario ya tiene los campos adicionales configurados","data":camposUserExists})          
        else:    
            #creamos el nuevo registro de campos adiciaonles del usuario
            try:
                newSCamposAdicionalesUser=CamposUserModel(
                    sociedad_id=camposUser.sociedad_id,
                    user_id=camposUser.user_id,
                    camuser1=camposUser.camuser1,
                    camuser2=camposUser.camuser2,
                    camuser3=camposUser.camuser3,
                    camuser4=camposUser.camuser4,
                    camuser5=camposUser.camuser5,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newSCamposAdicionalesUser)
                self.db.commit()

                #creamos el registro historico de campos adicionales del usuario
                CamposUserController.create_historico_campos_adicionales_user(self,newSCamposAdicionalesUser,"Se creó una configuracion de campos adicionales en el sistema")
  
                data={
                    "id": newSCamposAdicionalesUser.id,
                    "sociedad_id":newSCamposAdicionalesUser.sociedad_id,
                    "user_id":newSCamposAdicionalesUser.user_id,
                    "camuser1":newSCamposAdicionalesUser.camuser1,
                    "camuser2":newSCamposAdicionalesUser.camuser2,
                    "camuser3":newSCamposAdicionalesUser.camuser3,
                    "camuser4":newSCamposAdicionalesUser.camuser4,
                    "camuser5":newSCamposAdicionalesUser.camuser5,
                    "created": newSCamposAdicionalesUser.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newSCamposAdicionalesUser.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newSCamposAdicionalesUser.creator_user,
                    "updater_user":newSCamposAdicionalesUser.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos de campos adicionales del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_campos_adicionales_user(self,id:int):

        # buscamos si este existe el registro
        nRecord = self.db.query(CamposUserModel).filter(CamposUserModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos del registro de campos adicionales del usuario
            try:
                camposUserExits = self.db.query(CamposUserModel).filter(CamposUserModel.id == id).first()                  
                # devolvemos los datos de campos adicionales del usuario
                return ({"result":"1","estado":"Se consiguieron los campos adicionales ","data":camposUserExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
            
 
    # metodo para actualizar los datos de los campos adicionales del usuario
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params camposUser: esquema de los datos de los campos adicionales del usuario
    # @params id: Id del registrop de campos adicionales lde usuario
    def update_campos_adicionales_user(self, camposUser: CamposAdicionalesUserSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el registro de campos adicionales existe
        nRecord = self.db.query(CamposUserModel).filter(CamposUserModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de los campos adicionales del usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                camposUserExists = self.db.query(CamposUserModel).filter(CamposUserModel.id == id).first()             

                #creamos el registro de campos adicionales del usuario en el historico
                CamposUserController.create_historico_campos_adicionales_user(self,camposUserExists ,"Actualización de la data de Campos Adicionales del Usuario")

                #registramnos los cambios en la tabla de sedes
                camposUserExists.sociedad_id=camposUser.sociedad_id,
                camposUserExists.user_id=camposUser.user_id,
                camposUserExists.camuser1=camposUser.camuser1,
                camposUserExists.camuser2=camposUser.camuser3,
                camposUserExists.camuser3=camposUser.camuser3,
                camposUserExists.camuser4=camposUser.camuser4,
                camposUserExists.camuser5=camposUser.camuser5,
                camposUserExists.updated=ahora,
                camposUserExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":camposUserExists.id,
                    "sociedad_id":camposUserExists.sociedad_id,
                    "user_id":camposUserExists.user_id,
                    "camuser1":camposUserExists.camuser1,
                    "camuser2":camposUserExists.camuser2,
                    "camuser3":camposUserExists.camuser3,
                    "camuser4":camposUserExists.camuser4,
                    "camuser5":camposUserExists.camuser5,
                    "created":camposUserExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":camposUserExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":camposUserExists.creator_user,
                    "updater_user":camposUserExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el registro de campos adicionales del usuario","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_campos_adicionales_users(self):
        consulta = self.db.query(CamposUserModel)
        result=consulta.all()
        return (result)


    # metodo para consultar todas los registros de campos adicionales por sociedad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_campos_adicionales_users_sociedad(self,idSociedad):
        consulta = self.db.query(CamposUserModel).filter(CamposUserModel.sociedad_id==idSociedad)
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de los campos adicionales de un usuario
    # @params id: Id del usuario  que se esta consultando
    def list_history_campos_adicionales_users(self,  id:int):

        # buscamos si exite el registro de  historico de campos adicionales del usuario
        nRecord = self.db.query(HistoricoCamposUserModel).filter(HistoricoCamposUserModel.user_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de los campos adicionales del usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de la sede
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCamposUserModel).filter(HistoricoCamposUserModel.user_id == id)

                listHistoryCamposUser=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de los campos adicionales del usuario ","data": listHistoryCamposUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     