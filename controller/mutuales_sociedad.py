'''
Este archivo contiene las funciones básicas del CRUD de Mutuales de la Sociedad
Created 2024-03
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="MutualesSociedad"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    banco_id = Column (BIGINT, ForeignKey("Bancos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    numero_cuenta = Column(VARCHAR(100), nullable=False)
    codigo_convenio = Column(VARCHAR(150), nullable=True)
    giro_empresa = Column(VARCHAR(150), nullable=True)
    razon_social = Column(VARCHAR(150), nullable=True)  
    ocultar_email = Column(INTEGER, nullable=True)      
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id: int = Field (ge=1,lt=20000)
    mutual_id : int = Field(gr=1, lt=1000)
    procentaje : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": '1',
                    "mutual_id" : '1',
                    "procentaje" : 0
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
from models.mutuales_sociedades import MutualesSociedad as MutualesSociedadModel
from models.historico_mutuales_sociedades import HistoricoMutualesSociedad as HistoricoMutualesSociedadModel



# importamos el schema de datos
from schemas.mutuales_sociedad import MutalesSociedad as MutualesSociedadSchema


# esto representa los metodos implementados en la tabla
class MutualesSociedadController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de datos bancarios de la sociedad
    #@param historicoBancarioUser: Modelo del registro de Bancarios del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_mutual_sociedad (self, mutualesSociedad:MutualesSociedadModel, observacion:str):
     # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:

            #creamos la instancia la nuevo registro del historico
            newHistoricoMutualSociedad= HistoricoMutualesSociedadModel(
                mutual_sociedad_id=mutualesSociedad.id,
                sociedad_id=mutualesSociedad.sociedad_id,     
                mutual_id=mutualesSociedad.mutual_id,
                porcentaje=mutualesSociedad.porcentaje,
                created=mutualesSociedad.created,
                updated=mutualesSociedad.updated,
                creator_user = mutualesSociedad.creator_user,
                updater_user=mutualesSociedad.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoMutualSociedad)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos mutuales de la sociedad
    # @userCreatorId: Id de la sociedad que está creando el registro
    # @params contactoUsuario: esquema de los datos de contacto de la sociedadque se desea insertar       
    def create_mutual_sociedad(self, mutualesSociedad:MutualesSociedadSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        #creamos el nuevo registro de mutuales de la sociedad
        try:
            
            newMutualesSociedad=MutualesSociedadModel(
                sociedad_id=mutualesSociedad.sociedad_id,
                mutual_id=mutualesSociedad.mutual_id,
                porcentaje=mutualesSociedad.porcentaje,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )

            #confirmamos el cambio en la Base de Datos
            self.db.add(newMutualesSociedad)
            self.db.commit()

            #creamos el registro historico de mutuales de la sociedad
            MutualesSociedadController.create_historico_mutual_sociedad(self,newMutualesSociedad,"Se creó los datos mutuales  de la sociedad")

            newMutualesSociedadId=newMutualesSociedad.id
            return ({"result":"1","estado":"creado","newMutualSociedadId":newMutualesSociedadId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    

    #metodo para consultar los datos mutuales de la sociedad
    # @params userId: id del Usuario al cual se le estan consultando los datos mutuales
    def get_mutual_sociedad(self,sociedadId:int):

        # buscamos si este usuario ya tiene datos mutuales
        nRecord = self.db.query(MutualesSociedadModel).filter(MutualesSociedadModel.sociedad_id == sociedadId).count()
        
        if (nRecord == 0):
            # no existen datos mutuales de la sociedad
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos mutuales
            try:
                mutualesSociedadExits = self.db.query(MutualesSociedadModel).filter(MutualesSociedadModel.sociedad_id == sociedadId).first()                  
                # devolvemos los datos mutuales de la sociedad
                return ({"result":"1","estado":"Se consiguieron los datos mutuales de la sociedad","data":mutualesSociedadExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
    #metodo para actualizar los datos mutuales de la sociedad
    # @userUpdaterId: Id de la sociedadque está actualizando el registro
    # @params bancarioSociedad: esquema de los datos mutuales de la sociedad que se desea insertar       
    def update_mutual_sociedad(self,userUpdaterId:int ,mutualesSociedad:MutualesSociedadSchema, idSociedad):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()


        # buscamos si existe el banco
        nRecord = self.db.query(MutualesSociedadModel).filter(MutualesSociedadModel.sociedad_id == idSociedad).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos mutuales de la sociedad
            return ({"result":"-2","estado":f"No record found {idSociedad}"})
        else:
            # existen los datos mutuales se puede actualizar
            try:
                #extraemos los datos para guardar el histórico
                mutualSociedadExists = self.db.query(MutualesSociedadModel).filter(MutualesSociedadModel.sociedad_id == idSociedad).first()                  

                #creamos el registro historico de mutuales
                MutualesSociedadController.create_historico_mutual_sociedad(self,mutualSociedadExists,"Actualización de la data de mutuales de la sociedad")   


                #registramnos los cambios en la tabla de mutuales de la sociedad
                mutualSociedadExists.mutual_id=mutualesSociedad.mutual_id,
                mutualSociedadExists.porcentaje=mutualesSociedad.porcentaje,
                mutualSociedadExists.updated=ahora,
                mutualSociedadExists.updater_sociedad=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó la data de mutuales de la sociedad","MutualesSociedad":mutualSociedadExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
        


            

    # metodo para listar los datos historicos mutuales de la sociedad
    # @params userId:: Id de la sociedadque se esta consultando
    def list_history_mutual_sociedad(self,sociedadId):

        # buscamos si existen los datos mutuales de la sociedad
        nRecord = self.db.query(HistoricoMutualesSociedadModel).filter(HistoricoMutualesSociedadModel.sociedad_id == sociedadId).count()
        
        if (nRecord == 0):
            # el banco no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe extraemos los datos y los enviamos
            try:
                listHistoryMutualesSociedad = self.db.query(HistoricoMutualesSociedadModel).filter(HistoricoMutualesSociedadModel.sociedad_id == sociedadId).all()                  
                # se actualizó el registro devolvemos los registros
                return ({"result":"1","estado":"Se consiguieron los datos mutuales de la sociedad","data": listHistoryMutualesSociedad})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     