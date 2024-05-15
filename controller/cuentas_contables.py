'''
Este archivo contiene las funciones básicas del CRUD de Cuentas Conatables en el sistema
Created 2024-02
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
   __tablename__="cuentaContables"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT,nullable=False)
    acct_code = Column(VARCHAR(20),nullable=False)
    acct_name = Column(VARCHAR(100),nullable=False)
    finance = Column(VARCHAR(1),nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    acct_code : str = Field(min_length=3, max_length=20)
    acct_name : str = Field(min_length=3, max_length=100)
    finance : str = Field(min_length=1, max_length=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "acct_code":"11010001",
                    "acct_name":"Caja",                    
                    "finance":"Y"                    
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
from models.cuentas_contable import CuentasContables as CuentasContablesModel
from models.historico_cuentas_contable import HistoricoCuentasContables as HistoricoCuentasContablesModel
#importamos el esquema de datos de Sociedades
from schemas.cuentas_contables import CuentasContable as cuentaContablesSchema

# esto representa los metodos implementados en la tabla
class CuentasContablesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las CuentasContables
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_cuenta_contable(self, cuentaContable:CuentasContablesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoCuentacontable= HistoricoCuentasContablesModel(
                cuenta_contable_id=cuentaContable.id,
                sociedad_id=cuentaContable.sociedad_id,
                acct_code=cuentaContable.acct_code,
                acct_name=cuentaContable.acct_name,
                finance=cuentaContable.finance,
                created=cuentaContable.created,
                updated=cuentaContable.updated,
                creator_user=cuentaContable.creator_user,
                updater_user=cuentaContable.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoCuentacontable)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la cuenta contable
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  sede  que se desea insertar       
    def create_cuenta_contable(self, cuentaContable:cuentaContablesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreCuentaContable=cuentaContable.acct_name.upper().strip()

        # contamos si existe una sede con el mismo nombre
        nRecordNombre = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.acct_name == nombreCuentaContable).count()  


        if (nRecordNombre > 0):
            # buscamos la cuenta contable con el nombre y lo devolvemos
            cuentaContableExists=self.db.query(CuentasContablesModel).filter(CuentasContablesModel.acct_name == nombreCuentaContable).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sede con ese nombre","data":cuentaContableExists})          
        else:    
            #creamos el nuevo registro de CuentasContables
            try:
                newCuentaContable=CuentasContablesModel(
                    sociedad_id=cuentaContable.sociedad_id,
                    acct_code=cuentaContable.acct_code,
                    acct_name=cuentaContable.acct_name,
                    finance=cuentaContable.finance,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newCuentaContable)
                self.db.commit()

                #creamos el registro historico de CuentasContables
                self.create_historico_cuenta_contable(newCuentaContable,"Se creó una sede en el sistema")
  
                data={
                    "id":newCuentaContable.id,
                    "sociedad_id":newCuentaContable.sociedad_id,
                    "acct_code": newCuentaContable.acct_code,
                    "acct_name":newCuentaContable.acct_name,
                    "finance":newCuentaContable.finance,
                    "created": newCuentaContable.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newCuentaContable.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newCuentaContable.creator_user,
                    "updater_user":newCuentaContable.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una sede
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_cuenta_contable(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta sede
            try:
                sedeExits = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.id == id).first()                  
                # devolvemos los datos de la cuenta contable
                return ({"result":"1","estado":"Se consiguieron los datos de la cuenta contable","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las CuentasContables
    # @params cadena: cadena que se buscara en la tabla cuenta contables comparando con el campo nombre 
    def search_cuenta_contable(self,finding ):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(CuentasContablesModel).filter(CuentasContablesModel.acct_name.like(findingT) | CuentasContablesModel.acct_code.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.acct_name.like(findingT) | CuentasContablesModel.acct_code.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de una sede por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la cuenta contable
    # @params id: Id de la cuenta contable que será actualizado
    def update_cuenta_contable(self, cuentaContable:cuentaContablesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la cuenta contable
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                cuentaContableExists = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_cuenta_contable(cuentaContableExists ,"Actualización de la data de la cuenta contable")

                #registramnos los cambios en la tabla de CuentasContables
                cuentaContableExists.sociedad_id=cuentaContable.sociedad_id,
                cuentaContableExists.acct_code=cuentaContable.acct_code,
                cuentaContableExists.acct_name=cuentaContable.acct_name,
                cuentaContableExists.finance=cuentaContable.finance,
                cuentaContableExists.updated=ahora,
                cuentaContableExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":cuentaContableExists.id,
                    "sede_id":cuentaContableExists.sociedad_id,
                    "acct_code":cuentaContableExists.acct_code,
                    "acct_name":cuentaContableExists.acct_name,
                    "finance":cuentaContableExists.finance,
                    "created":cuentaContableExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":cuentaContableExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":cuentaContableExists.creator_user,
                    "updater_user":cuentaContableExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la cuenta contable","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las CuentasContables
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cuenta_contable(self, ):
        consulta = self.db.query(CuentasContablesModel)

        result=consulta.all()
        return (result)


    # metodo para consultar todas las CuentasContables
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cuenta_contable_sociedad(self,idSociedad):
        consulta = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.sociedad_id==idSociedad)
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sociedad que se esta consultando
    def list_history_cuenta_contable(self,  id:int):

        # buscamos si exite la cuenta contable
        nRecord = self.db.query(HistoricoCuentasContablesModel).filter(HistoricoCuentasContablesModel.cuenta_contable_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la cuenta contable
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCuentasContablesModel).filter(HistoricoCuentasContablesModel.cuenta_contable_id == id)

                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la cuenta contable ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     