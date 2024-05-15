'''
Este archivo contiene las funciones básicas del CRUD de Configuraciones de Remuneraciones
Created 2024-05
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="ConfRemuneraciones"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
    sueldo_minimo= Column(NUMERIC(18,4), nullable=False)
    gratificacion_minimo= Column(NUMERIC(5,2), nullable=False)
    tope_gratificacion= Column(NUMERIC(5,2), nullable=False)
    dias_vacaciones= Column(INTEGER, nullable=False)
    horas_legales= Column(INTEGER, nullable=False)
    retencion_honorarios= Column(NUMERIC(5,2), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    sueldo_minimo : float 
    gratificacion_minimo: float
    tope_gratificacion : float
    dias_vacaciones: int
    horas_legales : int
    retencion_honorarios : float
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'sociedad_id': 1,  
                    'sueldo_minimo' : 450000.00,
                    'gratificacion_minimo': 1.0,
                    'tope_gratificacion' : 5.0
                    'dias_vacaciones': 15,
                    'horas_legales' : 8,
                    'retencion_honorarios' : 0
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
from models.conf_remuneraciones import ConfRemuneraciones as ConfRemuneracionesModel
from models.historico_conf_remuneraciones import HistoricoConfRemuneraciones as HistoricoConfRemuneracionesModel

#importamos el esquema de datos de Sociedades
from schemas.conf_remuneraciones import ConfRemuneraciones as ConfRemuneracionesSchema


# esto representa los metodos implementados en la tabla
class ConfRemuneracionesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las configuracions
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_configuracion(self, configuracion: ConfRemuneracionesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            '''
            id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
            conf_remuneracion_id=Column(INTEGER,nullable=False) 
            sociedad_id = Column (BIGINT, nullable=False)        
            sueldo_minimo= Column(NUMERIC(18,4), nullable=False)
            gratificacion_minimo= Column(NUMERIC(5,2), nullable=False)
            tope_gratificacion= Column(NUMERIC(5,2), nullable=False)
            dias_vacaciones= Column(INTEGER, nullable=False)
            horas_legales= Column(INTEGER, nullable=False)
            retencion_honorarios= Column(NUMERIC(5,2), nullable=False)
            created = Column (DateTime, nullable=False) #datetime NOT NULL,    
            updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
            creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
            updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,
            fecha_registro = Column (DateTime, nullable=False) #datetime NOT NULL,      
            observaciones = Column(TEXT, nullable= True)    
            '''

            newHistoricocategoriaConfiguracion= HistoricoConfRemuneracionesModel(
                conf_remuneracion_id=configuracion.id,
                sociedad_id=configuracion.sociedad_id,                
                sueldo_minimo=configuracion.sueldo_minimo,
                gratificacion_minimo=configuracion.gratificacion_minimo,
                tope_gratificacion=configuracion.tope_gratificacion,
                dias_vacaciones=configuracion.dias_vacaciones,
                horas_legales=configuracion.oras_legales,
                retencion_honorarios=configuracion.retencion_honorarios,              
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
    def create_configuracion(self, configuracion:ConfRemuneracionesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreConfiguracion=configuracion.nombre.upper().strip()

        # contamos si existe una configuracion con el mismo nombre
        nRecordNombre = self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.nombre == nombreConfiguracion).count()  


        if (nRecordNombre > 0):
            # buscamos la configuracion con el nombre y lo devolvemos
            configuracionExists=self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.nombre == nombreConfiguracion).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una configuracion con ese nombre","data":configuracionExists})          
        else:    
            #creamos el nuevo registro de configuracions
            '''
            id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
            sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
            sueldo_minimo= Column(NUMERIC(18,4), nullable=False)
            gratificacion_minimo= Column(NUMERIC(5,2), nullable=False)
            tope_gratificacion= Column(NUMERIC(5,2), nullable=False)
            dias_vacaciones= Column(INTEGER, nullable=False)
            horas_legales= Column(INTEGER, nullable=False)
            retencion_honorarios= Column(NUMERIC(5,2), nullable=False)
            created = Column (DateTime, nullable=False) #datetime NOT NULL,    
            updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
            creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
            updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,           
            '''
            try:
                newConfiguracion=ConfRemuneracionesModel(
                    sociedad_id=configuracion.sociedad_id,
                    sueldo_minimo= configuracion.sueldo_minimo,
                    gratificacion_minimo= configuracion.gratificacion_minimo,
                    tope_gratificacion= configuracion.tope_gratificacion,
                    dias_vacaciones= configuracion.dias_vacaciones,
                    horas_legales= configuracion.horas_legales,
                    retencion_honorarios= configuracion.retencion_honorarios,                 
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

                data=newConfiguracion.to_dict()

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una configuracion
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_configuracion(self,id:int):

        # buscamos si este existe esta configuracion
        nRecord = self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta configuracion
            try:
                configuracionExits = self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.id == id).first()                  
                # devolvemos los datos de la configuracion
                return ({"result":"1","estado":"Se consiguieron los datos de la configuracion","data":configuracionExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})  
            
 
    #metodo para actualizar los datos de una configuracion por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la configuracion
    # @params id: Id de la configuracion que será actualizado
    def update_configuracion(self, configuracion:ConfRemuneracionesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                configuracionExists = self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.id == id).first()             

                #creamos el registro historico de configuracion
                self.create_historico_configuracion(configuracionExists ,"Actualización de la data de la configuracion")

                #registramnos los cambios en la tabla de configuracions
                configuracionExists.sociedad_id=configuracion.sociedad_id
                configuracionExists.sueldo_minimo= configuracion.sueldo_minimo
                configuracionExists.gratificacion_minimo= configuracion.gratificacion_minimo
                configuracionExists.tope_gratificacion= configuracion.tope_gratificacion
                configuracionExists.dias_vacaciones= configuracion.dias_vacaciones
                configuracionExists.horas_legales= configuracion.horas_legales
                configuracionExists.retencion_honorarios= configuracion.retencion_honorarios 
                configuracionExists.updated=ahora
                configuracionExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data=configuracionExists.to_dict()
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la configuracion","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las configuracions
    def list_configuracion(self):
        result = self.db.query(ConfRemuneracionesModel).order_by(ConfRemuneracionesModel.id).all()
        return (result)


    # metodo para consultar todas las configuracions
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_configuracion_sociedad(self,idSociedad):
        result = self.db.query(ConfRemuneracionesModel).filter(ConfRemuneracionesModel.sociedad_id==idSociedad).order_by(ConfRemuneracionesModel.id).all()
        return (result)


    # metodo para listar los datos historicos  de una configuracion
    # @params id: Id de la sociedad que se esta consultando
    def list_history_configuracion(self, id:int):

        # buscamos si exite la configuracion
        nRecord = self.db.query(HistoricoConfRemuneracionesModel).filter(HistoricoConfRemuneracionesModel.configuracion_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                listHistoryconfiguracion = self.db.query(HistoricoConfRemuneracionesModel).filter(HistoricoConfRemuneracionesModel.configuracion_id == id).all()

               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la  configuracion ","data": listHistoryconfiguracion})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     