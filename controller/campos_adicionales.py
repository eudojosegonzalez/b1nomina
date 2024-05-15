'''
Este archivo contiene las funciones básicas del CRUD Campis Adicionales en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
   __tablename__="CamposAdicionales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False) 
    camuser1 = Column (VARCHAR(200), nullable=True)
    activo1=Column(INTEGER,nullable=False)
    camuser2 = Column (VARCHAR(200), nullable=True)    
    activo2=Column(INTEGER,nullable=False)    
    camuser3 = Column (VARCHAR(200), nullable=True)
    activo3=Column(INTEGER,nullable=False)    
    camuser4 = Column (VARCHAR(200), nullable=True) 
    activo4=Column(INTEGER,nullable=False)       
    camuser5 = Column (VARCHAR(200), nullable=True)
    activo5=Column(INTEGER,nullable=False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
class CamposAdicionalesUser(BaseModel):
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
from models.campos_adicionales import CamposAdicionales as CamposAdicionalesModel
from models.historico_campos_adicioanles import HistoricoCamposAdicionales as HistoricoCamposAdicionalesModel

#importamos el esquema de datos de Sede
from schemas.campos_adicionales import CamposAdicionales as CamposAdicionalesSchema



# esto representa los metodos implementados en la tabla
class CamposAdicionalesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de los campos adicionales del usuario
    #@param camposUser: Modelo del registro de Campos Adicionales del Usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_campos_adicionales(self, camposAdicionales: CamposAdicionalesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoCamposAdicionales= HistoricoCamposAdicionalesModel(
                sociedad_id=camposAdicionales.sociedad_id,
                campos_adicionales_id=camposAdicionales.id,
                camuser1=camposAdicionales.camuser1,
                activo1=camposAdicionales.activo1,
                camuser2=camposAdicionales.camuser2,
                activo2=camposAdicionales.activo2,
                camuser3=camposAdicionales.camuser3,
                activo3=camposAdicionales.activo3,                
                camuser4=camposAdicionales.camuser4,
                activo4=camposAdicionales.activo4,                
                camuser5=camposAdicionales.camuser5,
                activo5=camposAdicionales.activo5,                
                created=camposAdicionales.created,
                updated=camposAdicionales.updated,
                creator_user=camposAdicionales.creator_user,
                updater_user=camposAdicionales.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoCamposAdicionales)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de los campos asicionales del usuario
    # @userCreatorId: Id del usuario que está creando el registro
    # @params camposUser: esquema de los datos de  los campos adicionales del usuario     
    def create_campos_adicionales(self, camposAdicionales: CamposAdicionalesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
 
        sociedadId=camposAdicionales.sociedad_id
        # contamos si existe el registro en la Bd
        nRecordNombre = self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.sociedad_id == sociedadId).count()  


        if (nRecordNombre > 0):
            # buscamos si existe el registro de campos adiciaonels del usuario
            camposAdicionalesExists=self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.sociedad_id == sociedadId).first() 

            # devolvemos el registro de campos adicionales 
            return ({"result":"-1","estado":"Este usuario ya tiene los campos adicionales configurados","data":camposAdicionalesExists})          
        else:    
            #creamos el nuevo registro de campos adiciaonles del usuario
            try:
                newCamposAdicionales=CamposAdicionalesModel(
                    sociedad_id=camposAdicionales.sociedad_id,
                    camuser1=camposAdicionales.camuser1,
                    activo1=camposAdicionales.activo1,
                    camuser2=camposAdicionales.camuser2,
                    activo2=camposAdicionales.activo2,                    
                    camuser3=camposAdicionales.camuser3,
                    activo3=camposAdicionales.activo3,                    
                    camuser4=camposAdicionales.camuser4,
                    activo4=camposAdicionales.activo4,                    
                    camuser5=camposAdicionales.camuser5,
                    activo5=camposAdicionales.activo5,                    
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newCamposAdicionales)
                self.db.commit()

                #creamos el registro historico de campos adicionales del usuario
                CamposAdicionalesController.create_historico_campos_adicionales(self,newCamposAdicionales,"Se creó una configuracion de campos adicionales en el sistema")
  
                # convertimos el registro en un diccionario para devolverlo
                data=newCamposAdicionales.to_dict()

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos de campos adicionales del usuario
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_campos_adicionales(self,id:int):

        # buscamos si este existe el registro
        nRecord = self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos del registro de campos adicionales del usuario
            try:
                camposUserExits = self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.id == id).first()                  
                # devolvemos los datos de campos adicionales del usuario
                return ({"result":"1","estado":"Se consiguieron los campos adicionales ","data":camposUserExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    # metodo para actualizar los datos de los campos adicionales del usuario
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params camposUser: esquema de los datos de los campos adicionales del usuario
    # @params id: Id del registrop de campos adicionales lde usuario
    def update_campos_adicionales(self, camposAdicionales: CamposAdicionalesSchema, userUpdaterId:int, id:int):
        paso=1
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si el registro de campos adicionales existe
        paso=2
        nRecord = self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de los campos adicionales del usuario
            paso=3
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                paso=4
                camposAdicionalesExists = self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.id == id).first()             

                #creamos el registro de campos adicionales del usuario en el historico
                paso=5
                CamposAdicionalesController.create_historico_campos_adicionales(self,camposAdicionalesExists ,"Actualización de la data de Campos Adicionales del Usuario")

                #registramnos los cambios en la tabla de sedes
                paso=6
                camposAdicionalesExists.sociedad_id=camposAdicionales.sociedad_id,
                camposAdicionalesExists.camuser1=camposAdicionales.camuser1,
                camposAdicionalesExists.activo1=camposAdicionales.activo1,
                camposAdicionalesExists.camuser2=camposAdicionales.camuser2,
                camposAdicionalesExists.activo2=camposAdicionales.activo2,
                camposAdicionalesExists.camuser3=camposAdicionales.camuser3,
                camposAdicionalesExists.activo3=camposAdicionales.activo3,
                camposAdicionalesExists.camuser4=camposAdicionales.camuser4,
                camposAdicionalesExists.activo4=camposAdicionales.activo4,
                camposAdicionalesExists.camuser5=camposAdicionales.camuser5,
                camposAdicionalesExists.activo5=camposAdicionales.activo5,
                camposAdicionalesExists.updated=ahora,
                camposAdicionalesExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                paso=7
                self.db.commit()

                paso=8
                data=camposAdicionalesExists.to_dict()
                
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el registro de campos adicionales del usuario","data":data})
            except ValueError as e:
                return( {"result":"-3","cadenaError": f"Ocurrió un error inesperadpo {str(e)} Pasp:{paso}"})                    


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_campos_adicionales(self):
        consulta = self.db.query(CamposAdicionalesModel)
        result=consulta.all()
        return (result)


    # metodo para consultar todas los registros de campos adicionales por sociedad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_campos_adicionales_sociedad(self,idSociedad):
        consulta = self.db.query(CamposAdicionalesModel).filter(CamposAdicionalesModel.sociedad_id==idSociedad)
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de los campos adicionales de un usuario
    # @params id: Id del usuario  que se esta consultando
    def list_history_campos_adicionales(self,  id:int):

        # buscamos si exite el registro de  historico de campos adicionales del usuario
        nRecord = self.db.query(HistoricoCamposAdicionalesModel).filter(HistoricoCamposAdicionalesModel.user_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de los campos adicionales del usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de la sede
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCamposAdicionalesModel).filter(HistoricoCamposAdicionalesModel.user_id == id)

                listHistoryCamposUser=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de los campos adicionales del usuario ","data": listHistoryCamposUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     