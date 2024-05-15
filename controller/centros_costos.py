'''
Este archivo contiene las funciones básicas del CRUD de Centros de Costos del Sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="CentrosDeCostos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column(BIGINT,  ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    codigo_sap = Column(VARCHAR(50), nullable=True)
    centro_costo = Column(VARCHAR(200), nullable=True)
    dimension_id = Column(BIGINT,  ForeignKey("Dimensiones.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    codigo_sap : str = Field (min_length=0, max_length=50)
    centro_costo : str = Field (min_length=0, max_length=200)
    dimension_id : int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id" : 1,
                    "codigo_sap" : "",
                    "centro_costo" : "",
                    "dimension_id" : 1
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
from models.centros_costos import CentrosDeCostos as CentrosDeCostosModel
from models.historico_centros_costos import HistoricoCentrosDeCostos as HistoricoCentrosDeCostosModel
from models.dimensiones import Dimensiones as DimensionesModel


# importamos el schema de datos
from schemas.centros_costos import CentrosDeCostos as CentrosDeCostosSchema


# esto representa los metodos implementados en la tabla
class CentrosDeCostosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de Centros de Costos
    #@param centrosCostos: Modelo del registro de Centros de Costos
    #@param observavacion: Observación sobre el historico
    def create_historico_centros_costos (self, centrosCostos:CentrosDeCostosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico

            newCentrosCostos= HistoricoCentrosDeCostosModel(
                centros_costos_id = centrosCostos.id,
                sociedad_id=centrosCostos.sociedad_id,
                codigo_sap=centrosCostos.codigo_sap,
                centro_costo=centrosCostos.centro_costo,
                dimension_id=centrosCostos.dimension_id,
                created = centrosCostos.created,
                updated = centrosCostos.updated,
                creator_user= centrosCostos.creator_user,
                updater_user = centrosCostos.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newCentrosCostos)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del centro de costo
    # @userCreatorId: Id del usuario que está creando el registro
    # @params centrosCostos: esquema de los datos del centro de cosatos que se desea insertar       
    def create_centro_costo(self, centrosCostos:CentrosDeCostosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        paso=1
        ahora=datetime.datetime.now()

        paso=2
        codigoSap=centrosCostos.codigo_sap
        paso=3
        centroCosto=centrosCostos.centro_costo
        sociedadId=centrosCostos.sociedad_id

        # contamos si existe un centro de costo con el mismo codigop_sap y el mismo centro de costo
        paso=4
        nRecord = self.db.query(CentrosDeCostosModel).filter(
            and_(CentrosDeCostosModel.codigo_sap == codigoSap, 
                 CentrosDeCostosModel.centro_costo==centroCosto,
                 CentrosDeCostosModel.sociedad_id==sociedadId)
            ).count()  

        if (nRecord > 0):
            # buscamos el banco con el nombre y lo devolvemos
            paso=5
            centroCostosExists=self.db.query(CentrosDeCostosModel).filter( 
                and_(CentrosDeCostosModel.codigo_sap == codigoSap, 
                 CentrosDeCostosModel.centro_costo==centroCosto,
                 CentrosDeCostosModel.sociedad_id==sociedadId)
            ).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-1","estado":"Existe un centro de costo con este codigo_sap y centro_costo, no puede volver a crearlos","data":centroCostosExists})
        else:    
            #creamos el nuevo registro de banco
            try:
                paso=6
                newCentroCosto=CentrosDeCostosModel(
                    sociedad_id=centrosCostos.sociedad_id,
                    codigo_sap=centrosCostos.codigo_sap,
                    centro_costo=centrosCostos.centro_costo,
                    dimension_id=centrosCostos.dimension_id,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                paso=7
                self.db.add(newCentroCosto)
                paso=8
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                paso=9
                CentrosDeCostosController.create_historico_centros_costos(self,newCentroCosto,"Se creó un centro de costo el sistema")
  
                paso=10
                data={
                    "id":newCentroCosto.id,
                    "sociedad_id":newCentroCosto.sociedad_id,
                    "codigo_sap":newCentroCosto.codigo_sap,
                    "centro_costo":newCentroCosto.centro_costo,
                    "dimension_id":newCentroCosto.dimension_id,
                    "created": newCentroCosto.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newCentroCosto.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newCentroCosto.creator_user,
                    "updater_user":newCentroCosto.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": f"Ocurrio un error {str(e)} Paso:{paso}"})
    

    #metodo para consultar los datos de un centro de costo por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_centro_costo(self,id:int):

        # buscamos los datos bancarios
        nRecord = self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este banco
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                bancoExits = self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.id == id).first()                  

                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos del banco","data":bancoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los centros de costo 
    # @params cadena: cadena que se buscara en la tabla centro de costos comparando 
    # con el campo codigo_sap, centro de costo      
    def search_centro_costo(self,finding):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.codigo_sap.like(findingT) | CentrosDeCostosModel.centro_costo.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.codigo_sap.like(findingT) | CentrosDeCostosModel.centro_costo.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de un centro de costo por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params centrosCostos: esquema de los datos de centro de costos 
    # @params id: Id del centro de costos que será actualizado
    def update_centro_costo(self, centrosCostos:CentrosDeCostosSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        paso=1
        
        codigoSap=centrosCostos.codigo_sap.strip()
        centroCosto=centrosCostos.centro_costo.strip()
        sociedadId=centrosCostos.sociedad_id
        
        
        # buscamos si este centro de costo existe
        paso=2
        nRecord = self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del banco
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                                    
                paso=3
                # verificar si existe un centro de costo igual al que se desea actualizar
                nRecordExists=self.db.query(CentrosDeCostosModel).filter(
                    and_(CentrosDeCostosModel.codigo_sap == codigoSap,
                         CentrosDeCostosModel.centro_costo == centroCosto,
                         CentrosDeCostosModel.sociedad_id == sociedadId, 
                         CentrosDeCostosModel.id != id)
                    ).count()
                
                # no se puede actualizar con esa data porque ya existe
                if (nRecordExists > 0):
                    paso=4
                    centroCostosExists=self.db.query(CentrosDeCostosModel).filter(
                        and_(CentrosDeCostosModel.codigo_sap == codigoSap,
                             CentrosDeCostosModel.centro_costo == centroCosto,
                             CentrosDeCostosModel.sociedad_id == sociedadId,
                             CentrosDeCostosModel.id != id)
                        ).first()
                    
                    data={
                        "id":centroCostosExists.id,
                        "sociedad_id":centroCostosExists.sociedad_id,
                        "codigo_sap":centroCostosExists.codigo_sap,
                        "centro_costo":centroCostosExists.centro_costo,
                        "dimension_id":centroCostosExists.dimension_id,
                        "created": centroCostosExists.created.strftime("%Y-%m-%d %H:%M:%S"),  
                        "updated":centroCostosExists.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                        "creator_user":centroCostosExists.creator_user,
                        "updater_user":centroCostosExists.updater_user
                    }                    
                    return ({"result":"-1","estado":"No se puede actualizar la data por que ya existe un centro de costo igual","data":data})
                else:    
                    #extraemos los datos para guardar el histórico
                    paso=5
                    centroCostosExists = self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.id == id).first()             

                    #creamos el registro historico de bancos
                    paso=6
                    CentrosDeCostosController.create_historico_centros_costos(self,centroCostosExists ,"Actualización de la data del centro de costo")

                    #registramnos los cambios en la tabla de centro de costos
                    paso=7
                    centroCostosExists.codigo_sap=centrosCostos.codigo_sap.strip(),
                    centroCostosExists.centro_costo=centrosCostos.centro_costo.strip(),
                    centroCostosExists.dimension_id=centrosCostos.dimension_id,
                    centroCostosExists.updated=ahora,
                    centroCostosExists.updater_user=userUpdaterId               


                    #confirmamos los cambios
                    paso=8
                    self.db.commit()
                    
                    data={
                        "id":centroCostosExists.id,
                        "sociedad_id":centroCostosExists.sociedad_id,
                        "codigo_sap":centroCostosExists.codigo_sap,
                        "centro_costo":centroCostosExists.centro_costo,
                        "dimension_id":centroCostosExists.dimension_id,
                        "created": centroCostosExists.created.strftime("%Y-%m-%d %H:%M:%S"),  
                        "updated":centroCostosExists.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                        "creator_user":centroCostosExists.creator_user,
                        "updater_user":centroCostosExists.updater_user
                    }
                    # se actualizó el registro devolvemos el registro actualizado
                    return ({"result":"1","estado":"Se actualizó la data del centro de costo","data":data})
            except ValueError as e:
                return( {"result":"-3","estado":f"Ocurrio un error {str(e)} Paso:{paso}" })                    


    # metodo para consultar todos los centros de costo de una sociedad
    def list_centros_costos(self, id : int):
        consulta = self.db.query(CentrosDeCostosModel).filter(CentrosDeCostosModel.sociedad_id==id)
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos de un centro de costo
    # @params id: Id del centro de costo que se esta consultando
    def list_history_centros_costos(self, id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricoCentrosDeCostosModel).filter(HistoricoCentrosDeCostosModel.id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del banco
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCentrosDeCostosModel).filter(HistoricoCentrosDeCostosModel.id == id)
                listHistoryCentroCosto=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos del centro de costo ","data": listHistoryCentroCosto})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     