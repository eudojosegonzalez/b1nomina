'''
Este archivo contiene las funciones básicas del CRUD de Periodos
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Periodos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    anio = Column(INTEGER, nullable=False)
    mes = Column(INTEGER, nullable=False)    
    nombre = Column(VARCHAR(200), nullable=False)
    observaciones = Column(TEXT, nullable=True)
    actio=Column(INTEGER, nullable=False)    
    utm=Column(NUMERIC(18,4), nullable=False)    
    uf=Column(NUMERIC(18,4), nullable=False)     
    factor_actualizacion=Column(NUMERIC(18,4), nullable=False) 
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    anio : int = Field(ge=1990, le=1000)
    mes : int = Field(ge=1, le=12)
    nombre : str = Field(min_length=3, max_length=250)
    observaciones: str = Field(min_length=3, max_length=500)
    activo : bool
    utm : float
    uf :float
    factor_actualizacion : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "anio": 2023,
                    "mes": 1,
                    "nombre":"Enero 2023",
                    "observaciones":"",
                    "activo":True,
                    "utm":47729.00,
                    "uf":28679.45,
                    "factor_actualizacion":1013
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
from models.periodos import Periodos as PeriodosModel
from models.historico_periodos import HistoricoPeriodos as HistoricoPeriodosModel

#importamos el esquema de datos de Periodos
from schemas.periodos import Periodos as PeriodosSchema



# esto representa los metodos implementados en la tabla
class PeriodosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de perido
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_periodos(self, periodos: PeriodosModel, observacionv:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoPeriodos= HistoricoPeriodosModel(
                periodos_id=periodos.id,
                anio=periodos.anio,
                mes=periodos.mes,
                nombre=periodos.nombre,
                observaciones=periodos.observaciones,
                activo=periodos.activo,
                utm=periodos.utm,
                uf=periodos.uf,
                factor_actualizacion=periodos.factor_actualizacion,                
                created=periodos.created,
                updated=periodos.updated,
                creator_user=periodos.creator_user,
                updater_user=periodos.updater_user,
                fecha_registro = ahora,
                observaciones_update = observacionv
            )
            

            # confirmamos el registro en el historico
            self.db.add(newHistoricoPeriodos)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    # metodo para insertar  los datos del del periodo
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  periodo que se desea insertar       
    def create_periodo(self, periodos:PeriodosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombrePeriodos=periodos.nombre.upper().strip()
        mesPeriodo=periodos.mes
        anioPeriodo=periodos.anio

        # contamos si existe un periodo con el mismo nombre
        nRecordNombre = self.db.query(PeriodosModel).filter(PeriodosModel.nombre == nombrePeriodos).count()  

        # contamos si existe un periodo con el mismo nombre
        nRecordAnioMes = self.db.query(PeriodosModel).filter(and_(PeriodosModel.anio == anioPeriodo,PeriodosModel.mes==mesPeriodo)).count()          

        if (nRecordNombre > 0):
            # buscamos la sociedad con el nombre y lo devolvemos
            PeriodosExists=self.db.query(PeriodosModel).filter(PeriodosModel.nombre == nombrePeriodos).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe un periodo con ese nombre","data":PeriodosExists})   
        elif (nRecordAnioMes >0) :
            # buscamos la sociedad con el nombre y lo devolvemos
            PeriodosExists=self.db.query(PeriodosModel).filter(and_(PeriodosModel.anio == anioPeriodo,PeriodosModel.mes==mesPeriodo)).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-2","estado":"Existe un periodo con ese  mes y ese año","data":PeriodosExists})                   
        else:    
            #creamos el nuevo registro de periodo
            try:
                newPeriodos=PeriodosModel(
                    anio=periodos.anio,
                    mes=periodos.mes,
                    nombre=((periodos.nombre).upper()).strip(),
                    observaciones=periodos.observaciones,
                    activo=periodos.activo,
                    utm=periodos.utm,
                    uf=periodos.uf,
                    factor_actualizacion=periodos.factor_actualizacion,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newPeriodos)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_periodos(newPeriodos,"Se creó un periodo en el sistema")
  
                data={
                    "id":newPeriodos.id,
                    "anio":newPeriodos.anio,
                    "mes":newPeriodos.mes,
                    "nombre": newPeriodos.nombre,
                    "observaciones":newPeriodos.observaciones,
                    "activo":newPeriodos.activo,
                    "utm":newPeriodos.utm,
                    "uf":newPeriodos.uf,
                    "factor_actualizacion":newPeriodos.factor_actualizacion,
                    "created": newPeriodos.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newPeriodos.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newPeriodos.creator_user,
                    "updater_user":newPeriodos.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un periodo
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_periodo(self,id:int):

        # buscamos si este existe esta Periodos
        nRecord = self.db.query(PeriodosModel).filter(PeriodosModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta Periodos
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta Periodos
            try:
                PeriodosExits = self.db.query(PeriodosModel).filter(PeriodosModel.id == id).first()                  
                # devolvemos los datos de la Periodos
                return ({"result":"1","estado":"Se consiguieron los datos del Periodo","data":PeriodosExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    # metodo para consultar los detalles de los periodos por año
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_periodos_by_anio(self,anioId:int):

        # buscamos si este existe estr Periodos
        nRecord = self.db.query(PeriodosModel).filter(PeriodosModel.anio == anioId).count()
        
        if (nRecord == 0):
            # no existen datos de esta Periodos
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de este Periodos
            try:
                PeriodosExits = self.db.query(PeriodosModel).filter(PeriodosModel.anio == anioId).order_by(PeriodosModel.mes).all()
                # devolvemos los detalles del periodo
                return ({"result":"1","estado":"Se consiguieron los datos del Periodo","data":PeriodosExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    # metodo para consultar todas los Periodoss  se usaa par poder consultar en la tabla los años almacenados
    # se agrupa por la columna anio y se orderna por la misma
    def list_all_periodos(self):
        consulta = self.db.query(PeriodosModel).group_by(PeriodosModel.anio).order_by(PeriodosModel.anio)
        result=consulta.all()
        return (result)

           
 
    #metodo para actualizar los datos de una Periodos por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la Periodos
    # @params id: Id de la sociedad que será actualizado
    def update_periodo(self, periodos:PeriodosSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(PeriodosModel).filter(PeriodosModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la Periodos
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                PeriodosExists = self.db.query(PeriodosModel).filter(PeriodosModel.id == id).first()             

                #creamos el registro historico de Periodos
                self.create_historico_periodos(PeriodosExists ,"Actualización de la data de un periodo")

                #registramnos los cambios en la tabla de bancarios del usuario
                PeriodosExists.anio=periodos.anio,
                PeriodosExists.mes=periodos.mes,
                PeriodosExists.nombre=((periodos.nombre).upper()).strip(),
                PeriodosExists.observaciones=periodos.observaciones,
                PeriodosExists.utm=periodos.utm,
                PeriodosExists.uf=periodos.uf,
                PeriodosExists.activo=periodos.activo,                
                PeriodosExists.factor_actualizacion=periodos.factor_actualizacion
                PeriodosExists.updated=ahora,
                PeriodosExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":PeriodosExists.id,
                    "anio":PeriodosExists.anio,
                    "mes":PeriodosExists.mes,
                    "nombre": PeriodosExists.nombre,
                    "observaciones":PeriodosExists.observaciones,
                    "activo":PeriodosExists.activo,
                    "utm":PeriodosExists.utm,
                    "uf":PeriodosExists.uf,
                    "factor_actualizacion":PeriodosExists.factor_actualizacion,
                    "created": PeriodosExists.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":PeriodosExists.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":PeriodosExists.creator_user,
                    "updater_user":PeriodosExists.updater_user                   
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó Periodo","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para listar los datos historicos  de una Periodos
    # @params id: Id de la sociedad que se esta consultando
    def list_history_periodos(self,id):

        # buscamos si exite la Periodos
        nRecord = self.db.query(HistoricoPeriodosModel).filter(HistoricoPeriodosModel.periodos_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la Periodos
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoPeriodosModel).filter(HistoricoPeriodosModel.periodos_id == id)
                listHistoryPeriodos=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la Periodos ","data": listHistoryPeriodos})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     