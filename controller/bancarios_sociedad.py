'''
Este archivo contiene las funciones básicas del CRUD de Bancarios de la Sociedad
Created 2023-12
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="BancariosSociedad"
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
    creator_sociedad= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_sociedad = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,

    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id: int = Field (ge=1,lt=20000)
    banco_id : int = Field(gr=1, lt=1000)
    numero_cuenta : str = Field (min_length=3, max_length=100)
    codigo_convenio: str = Field (min_length=0, max_length=100)
    giro_empresa : str = Field (min_length=0, max_length=150)
    razon_social  : str = Field (min_length=0, max_length=150)
    ocultar_mail : bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": '1',
                    "banco_id" : '1',
                    "numero_cuenta" : '0102002',
                    "codigo_convenio": '',
                    "giro_empresa" : '',
                    "razon_social"  : '',
                    "ocultar_mail" : True
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
from models.bancarios_sociedades import BancariosSociedad as BancarioSociedadModel
from models.historico_bancarios_sociedades import HistoricoBancariosSociedad as HistoricoBancarioSociedadModel



# importamos el schema de datos
from schemas.bancarios_sociedad import BancarioSociedad as BancarioSociedadSchema


# esto representa los metodos implementados en la tabla
class BancariosSociedadController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de datos bancarios de la sociedad
    #@param historicoBancarioUser: Modelo del registro de Bancarios del usuario
    #@param observavacion: Observación sobre el historico
    def create_historico_bancario_sociedad (self, bancarioSociedad: BancarioSociedadModel, observacion:str):
     # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:


            #creamos la instancia la nuevo registro del historico
            newHistoricoBancarioSociedad= HistoricoBancarioSociedadModel(
                bancarios_sociedad_id=bancarioSociedad.id,
                sociedad_id=bancarioSociedad.sociedad_id,     
                banco_id=bancarioSociedad.banco_id,
                numero_cuenta=bancarioSociedad.numero_cuenta,
                codigo_convenio=bancarioSociedad.codigo_convenio,
                giro_empresa=bancarioSociedad.giro_empresa,
                razon_social=bancarioSociedad.razon_social,
                ocultar_email=bancarioSociedad.ocultar_email,
                created=bancarioSociedad.created,
                updated=bancarioSociedad.updated,
                creator_user = bancarioSociedad.creator_user,
                updater_user=bancarioSociedad.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoBancarioSociedad)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos bancarios de la sociedad
    # @userCreatorId: Id de la sociedadque está creando el registro
    # @params contactoUsuario: esquema de los datos de contacto de la sociedadque se desea insertar       
    def create_bancario_sociedad(self, bancarioSociedad:BancarioSociedadSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        #creamos el nuevo registro de bancarios de usuarios
        try:

            
            newBancarioSociedad=BancarioSociedadModel(
                sociedad_id=bancarioSociedad.sociedad_id,
                banco_id=bancarioSociedad.banco_id,
                numero_cuenta=bancarioSociedad.numero_cuenta,
                codigo_convenio=bancarioSociedad.codigo_convenio,
                giro_empresa=bancarioSociedad.giro_empresa,
                razon_social=bancarioSociedad.razon_social,
                ocultar_email=bancarioSociedad.ocultar_mail,
                created=ahora,
                updated=ahora,
                creator_user = userCreatorId,
                updater_user=userCreatorId
            )

            #confirmamos el cambio en la Base de Datos
            self.db.add(newBancarioSociedad)
            self.db.commit()

            #creamos el registro historico de bancarios de la sociedad
            BancariosSociedadController.create_historico_bancario_sociedad(self,newBancarioSociedad,"Se creó los datos bancarios  de la sociedad")

            newBancarioSociedadId=newBancarioSociedad.id
            return ({"result":"1","estado":"creado","newBancarioSociedadId":newBancarioSociedadId})
        except ValueError as e:
            return( {"result":"-1","error": str(e)})
    

    #metodo para consultar los datos bancarios de la sociedad
    # @params userId: id del Usuario al cual se le estan consultadn los datos bancarios
    def get_bancario_sociedad(self,sociedadId:int):

        # buscamos si este usuario ya tiene datos bancarios
        nRecord = self.db.query(BancarioSociedadModel).filter(BancarioSociedadModel.sociedad_id == sociedadId).count()
        
        if (nRecord == 0):
            # no existen datos bancarios de la sociedad
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los bancarios de la sicuedad
            try:
                bancariosSociedadExits = self.db.query(BancarioSociedadModel).filter(BancarioSociedadModel.sociedad_id == sociedadId).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos bancarios de la sociedad","data":bancariosSociedadExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

 
    #metodo para actualizar los datos bancarios de la sociedad
    # @userUpdaterId: Id de la sociedadque está actualizando el registro
    # @params bancarioSociedad: esquema de los datos bancarios de la sociedadque se desea insertar       
    def update_bancario_sociedad(self,userUpdaterId:int ,bancarioSociedad:BancarioSociedadSchema, sociedadId:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si existe el banco
        nRecord = self.db.query(BancarioSociedadModel).filter(BancarioSociedadModel.sociedad_id == sociedadId).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del banco
            return ({"result":"-2","estado":f"No record found {sociedadId}"})
        else:
            # existen los datosdel banco se puede actualizar
            try:
                #extraemos los datos para guardar el histórico
                bancarioSociedadExists = self.db.query(BancarioSociedadModel).filter(BancarioSociedadModel.sociedad_id == sociedadId).first()                  

                #creamos el registro historico de banco
                BancariosSociedadController.create_historico_bancario_sociedad(self,bancarioSociedadExists,"Actualización de la data de bancarios de la sociedad")   

                '''
                `sociedad_id` bigint(20) NOT NULL,
                `banco_id` bigint(20) NOT NULL,
                `numero_cuenta` varchar(100) not NULL,
                `codigo_convenio` varchar(150)  NULL,
                `giro_empresa` varchar(150)  NULL,
                `razon_social` varchar(150)  NULL,   
                `ocultar_email` boolean null,    
                `created` datetime NOT NULL,
                `updated` datetime NOT NULL,
                `creator_user` bigint(20) NOT NULL,
                `updater_user` bigint(20) NOT NULL,                
                
                '''
                #registramnos los cambios en la tabla de bancarios de la sociedad
                bancarioSociedadExists.banco_id=bancarioSociedad.banco_id,
                bancarioSociedadExists.numero_cuenta=bancarioSociedad.numero_cuenta,
                bancarioSociedadExists.codigo_convenio=bancarioSociedad.codigo_convenio,
                bancarioSociedadExists.razon_social=bancarioSociedad.razon_social,
                bancarioSociedadExists.ocultar_email=bancarioSociedad.ocultar_mail,
                bancarioSociedadExists.updated=ahora,
                bancarioSociedadExists.updater_sociedad=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó la data de bancarios de la sociedad","BancariosSociedad":bancarioSociedadExists})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
        
            

    # metodo para listar los datos historicos bancarios de la sociedad
    # @params userId:: Id de la sociedadque se esta consultando
    def list_history_bancario_sociedad(self,sociedadId):

        # buscamos si existen los datos bancarios de la sociedad
        nRecord = self.db.query(HistoricoBancarioSociedadModel).filter(HistoricoBancarioSociedadModel.sociedad_id == sociedadId).count()
        
        if (nRecord == 0):
            # el banco no existe
            return ({"result":"-2","estado":"No record found"})
        else:
            # existe extraemos los datos y los enviamos
            try:
                listHistoryBancariosUser = self.db.query(HistoricoBancarioSociedadModel).filter(HistoricoBancarioSociedadModel.sociedad_id == sociedadId).all()                  
                # se actualizó el registro devolvemos los registros
                return ({"result":"1","estado":"Se consiguieron los datos bancarios de la sociedad","data": listHistoryBancariosUser})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     