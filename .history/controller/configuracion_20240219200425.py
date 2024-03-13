'''
Este archivo contiene las funciones básicas del CRUD de Configuraciones
Created 2024-02
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Configuraciones"    
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
    categoria_id = Column (BIGINT, ForeignKey("CategoriasConfiguracion.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)       
    nombre = Column(VARCHAR(200), nullable=False)
    valor = Column(NUMERIC(18,4), nullable=False)
    detalle= Column(TEXT, nullable=True)
    cuenta = Column(VARCHAR(20), nullable=True)
    ocultar= Column(INTEGER, nullable=True)
    tipo_validacion = Column(VARCHAR(30), nullable=True)
    orden= Column(INTEGER, nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    categoria_id : int = Field(ge=1, le=1000)
    nombre : str = Field(min_length=3, max_length=200)    
    valor : float
    detalle : str = Field(min_length=0, max_length=500)   
    cuenta : str = Field(min_length=0, max_length=50) 
    ocultar : int
    tipo_validacion : str = Field(min_length=0, max_length=30)
    orden : int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id":1,
                    "categoria_id":1,
                    "nombre": "demo",    
                    "valor":0 ,
                    "detalle":"",  
                    "cuenta":"",
                    "ocultar":0,
                    "tipo_validacion":"",
                    "orden":1
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
from models.configuracion import Configuraciones as ConfiguracionesModel
from models.historico_configuracion import HistoricoConfiguraciones as HistoricoConfiguracionesModel

#importamos el esquema de datos de Sociedades
from schemas.configuracion import Configuraciones as ConfiguracionesSchema


# esto representa los metodos implementados en la tabla
class ConfiguracionController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las configuracions
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_configuracion(self, configuracion: ConfiguracionesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            '''
            id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
            configuracion_id = Column (BIGINT, nullable=False)              
            sociedad_id = Column (BIGINT, nullable=False)        
            categoria_id = Column (BIGINT, nullable=False)       
            nombre = Column(VARCHAR(200), nullable=False)
            valor = Column(NUMERIC(18,4), nullable=False)
            detalle= Column(TEXT, nullable=True)
            cuenta = Column(VARCHAR(20), nullable=True)
            ocultar= Column(INTEGER, nullable=True)
            tipo_validacion = Column(VARCHAR(30), nullable=True)
            orden= Column(INTEGER, nullable=True)
            created = Column (DateTime, nullable=False) #datetime NOT NULL,    
            updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
            creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
            updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
            fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
            observaciones = Column(TEXT, nullable= True)            
            '''

            newHistoricocategoriaConfiguracion= HistoricoConfiguracionesModel(
                configuracion_id=configuracion.id,
                sociedad_id=configuracion.sociedad_id,                
                categoria_id=configuracion.categoria_id,
                nombre=configuracion.nombre,
                valor=configuracion.valor,
                detalle=configuracion.detalle,
                cuenta=configuracion.cuenta,
                ocultar=configuracion.ocultar,
                tipo_validacion=configuracion.tipo_validacion,
                orden=configuracion.orden,
                created=configuracion.created,
                updated=configuracion.updated,
                creator_user=configuracion.creator_user,
                updater_user=configuracion.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricocategoriaConfiguracion)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la configuracion
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  configuracion  que se desea insertar       
    def create_configuracion(self, configuracion:ConfiguracionesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreConfiguracion=configuracion.nombre.upper().strip()

        # contamos si existe una configuracion con el mismo nombre
        nRecordNombre = self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.nombre == nombreConfiguracion).count()  


        if (nRecordNombre > 0):
            # buscamos la configuracion con el nombre y lo devolvemos
            configuracionExists=self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.nombre == nombreConfiguracion).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una configuracion con ese nombre","data":configuracionExists})          
        else:    
            #creamos el nuevo registro de configuracions
            '''
            id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
            sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
            categoria_id = Column (BIGINT, ForeignKey("CategoriasConfiguracion.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)       
            nombre = Column(VARCHAR(200), nullable=False)
            valor = Column(NUMERIC(18,4), nullable=False)
            detalle= Column(TEXT, nullable=True)
            cuenta = Column(VARCHAR(20), nullable=True)
            ocultar= Column(INTEGER, nullable=True)
            tipo_validacion = Column(VARCHAR(30), nullable=True)
            orden= Column(INTEGER, nullable=True)
            created = Column (DateTime, nullable=False) #datetime NOT NULL,    
            updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
            creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
            updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,            
            '''
            try:
                newConfiguracion=ConfiguracionesModel(
                    sociedad_id=configuracion.sociedad_id,
                    categoria_id=configuracion.categoria_id,
                    nombre=((configuracion.nombre).upper()).strip(),
                    valor=configuracion.valor,
                    detalle=configuracion.detalle,
                    cuenta=configuracion.cuenta,
                    ocultar=configuracion.ocultar,
                    tipo_validacion=configuracion.tipo_validacion,
                    orden=configuracion.orden,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newConfiguracion)
                self.db.commit()

                #creamos el registro historico de configuracions
                self.create_historico_configuracion(newConfiguracion,"Se creó una configuración en el sistema")

                data={
                    "id":newConfiguracion.id,
                    "sociedad_id":newConfiguracion.sociedad_id,
                    "categoria_id":newConfiguracion.categoria_id,
                    "nombre": newConfiguracion.nombre,
                    "valor":newConfiguracion.valor,
                    "detalle":newConfiguracion.detalle,
                    "cuenta":newConfiguracion.cuenta,
                    "ocultar":newConfiguracion.ocultar,
                    "tipo_validacion":newConfiguracion.tipo_validacion,
                    "orden":newConfiguracion.orden,
                    "created": newConfiguracion.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newConfiguracion.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newConfiguracion.creator_user,
                    "updater_user":newConfiguracion.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una configuracion
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_configuracion(self,id:int):

        # buscamos si este existe esta configuracion
        nRecord = self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta configuracion
            try:
                configuracionExits = self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.id == id).first()                  
                # devolvemos los datos de la configuracion
                return ({"result":"1","estado":"Se consiguieron los datos de la configuracion","data":configuracionExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})  
            
 
    #metodo para actualizar los datos de una configuracion por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la configuracion
    # @params id: Id de la configuracion que será actualizado
    def update_configuracion(self, configuracion:ConfiguracionesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                configuracionExists = self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.id == id).first()             

                #creamos el registro historico de configuracion
                self.create_historico_configuracion(configuracionExists ,"Actualización de la data de la configuracion")

                #registramnos los cambios en la tabla de configuracions
                configuracionExists.sociedad_id=configuracion.sociedad_id,
                configuracionExists.categoria_id=configuracion.categoria_id,
                configuracionExists.nombre=((configuracion.nombre).upper()).strip(),
                configuracionExists.valor=configuracion.valor,
                configuracionExists.detalle=configuracion.detalle,
                configuracionExists.cuenta=configuracion.cuenta,
                configuracionExists.ocultar=configuracion.ocultar,
                configuracionExists.tipo_validacion=configuracion.tipo_validacion,
                configuracionExists.orden=configuracion.orden,
                configuracionExists.updated=ahora,
                configuracionExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":configuracionExists.id,
                    "sociedad_id":configuracionExists.sociedad_id,
                    "categoria_id":configuracionExists.categoria_id,
                    "nombre":configuracionExists.nombre,
                    "valor":configuracionExists.valor,
                    "detalle":configuracionExists.detalle,
                    "cuenta":configuracionExists.cuenta,
                    "ocultar":configuracionExists.ocultar,
                    "tipo_validacion":configuracionExists.tipo_validacion,
                    "orden":configuracionExists.orden,
                    "created":configuracionExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":configuracionExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":configuracionExists.creator_user,
                    "updater_user":configuracionExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la configuracion","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las configuracions
    def list_configuracion(self):
        result = self.db.query(ConfiguracionesModel).order_by(ConfiguracionesModel.id).all()
        return (result)


    # metodo para consultar todas las configuracions
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_configuracion_sociedad(self,idSociedad):
        result = self.db.query(ConfiguracionesModel).filter(ConfiguracionesModel.sociedad_id==idSociedad).order_by(ConfiguracionesModel.id).all()
        return (result)


    # metodo para listar los datos historicos  de una configuracion
    # @params id: Id de la sociedad que se esta consultando
    def list_history_configuracion(self, id:int):

        # buscamos si exite la configuracion
        nRecord = self.db.query(HistoricoConfiguracionesModel).filter(HistoricoConfiguracionesModel.configuracion_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                listHistoryconfiguracion = self.db.query(HistoricoConfiguracionesModel).filter(HistoricoConfiguracionesModel.configuracion_id == id).all()

               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la categoria de configuracion ","data": listHistoryconfiguracion})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     