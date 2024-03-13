'''
Este archivo contiene las funciones básicas del CRUD de Cuentas Conatables en el sistema
Created 2024-02
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
   __tablename__="CuentasContables"
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
from schemas.sede import Sede as SedeSchema



# esto representa los metodos implementados en la tabla
class sedesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sedes
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_cuenta_contable(self, cuentasContable:CuentasContablesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoCuentacontable= HistoricoCuentasContablesModel(
                cuentas_contable_id=cuentasContable.id,
                sociedad_id=cuentasContable.sociedad_id,

                created=cuentasContable.created,
                updated=cuentasContable.updated,
                creator_user=cuentasContable.creator_user,
                updater_user=cuentasContable.updater_user,
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
    def create_cuenta_contable(self, sede:SedeSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreCuentaContable=cuentasContable.nombre.upper().strip()

        # contamos si existe una sede con el mismo nombre
        nRecordNombre = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.nombre == nombreSede).count()  


        if (nRecordNombre > 0):
            # buscamos la cuenta contable con el nombre y lo devolvemos
            sedeExists=self.db.query(CuentasContablesModel).filter(CuentasContablesModel.nombre == nombreSede).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sede con ese nombre","data":sedeExists})          
        else:    
            #creamos el nuevo registro de sedes
            try:
                newCuentacontable=CuentasContablesModel(
                    sociedad_id=cuentasContable.sociedad_id,
                    nombre=((cuentasContable.nombre).upper()).strip(),
                    region_id=cuentasContable.region_id,
                    comuna_id=cuentasContable.comuna_id,
                    direccion=((cuentasContable.direccion).upper()).strip(),
                    ciudad=((cuentasContable.ciudad).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newCuentacontable)
                self.db.commit()

                #creamos el registro historico de sedes
                self.create_historico_cuenta_contable(newCuentacontable,"Se creó una sede en el sistema")
  
                data={
                    "sociedad_id":newcuentasContable.sociedad_id,
                    "nombre": newcuentasContable.nombre,
                    "region_id":newcuentasContable.region_id,
                    "comuna_id":newcuentasContable.comuna_id,
                    "ciudad":newcuentasContable.ciudad,
                    "direccion":newcuentasContable.direccion,
                    "created": newcuentasContable.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newcuentasContable.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newcuentasContable.creator_user,
                    "updater_user":newcuentasContable.updater_user
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
            

    #metodo para efectuar búsquedas en las sedes
    # @params cadena: cadena que se buscara en la tabla cuenta contables comparando con el campo nombre 
    def search_cuenta_contables(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(CuentasContablesModel).filter(CuentasContablesModel.nombre.like(findingT) | CuentasContablesModel.direccion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.nombre.like(findingT) | CuentasContablesModel.direccion.like(findingT))
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
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
    def update_cuenta_contable(self, sede:SedeSchema, userUpdaterId:int, id:int):
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
                sedeExists = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_cuenta_contable(sedeExists ,"Actualización de la data de la cuenta contable")

                #registramnos los cambios en la tabla de sedes
                sedeExists.sociedad_id=cuentasContable.sociedad_id,
                sedeExists.nombre=((cuentasContable.nombre).upper()).strip(),
                sedeExists.region_id=cuentasContable.region_id,
                sedeExists.comuna_id=cuentasContable.comuna_id,
                sedeExists.direccion=((cuentasContable.direccion).upper()).strip(),
                sedeExists.ciudad=((cuentasContable.ciudad).upper()).strip(),
                sedeExists.updated=ahora,
                sedeExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":sedeExists.id,
                    "sede_id":sedeExists.sociedad_id,
                    "nombre":sedeExists.nombre,
                    "region_id":sedeExists.region_id,
                    "comuna_id":sedeExists.comuna_id,
                    "direccion":sedeExists.direccion,
                    "ciudad":sedeExists.ciudad,
                    "created":sedeExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":sedeExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":sedeExists.creator_user,
                    "updater_user":sedeExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la cuenta contable","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cuenta_contables(self, page, records):
        consulta = self.db.query(CuentasContablesModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cuenta_contables_sociedad(self,idSociedad, page, records):
        consulta = self.db.query(CuentasContablesModel).filter(CuentasContablesModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sociedad que se esta consultando
    def list_history_cuenta_contables(self, page:int, records: int, id:int):

        # buscamos si exite la cuenta contable
        nRecord = self.db.query(HistoricoCuentasContablesModel).filter(HistoricoCuentasContablesModel.sociedad_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la cuenta contable
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCuentasContablesModel).filter(HistoricoCuentasContablesModel.sociedad_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la cuenta contable ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     