'''
Este archivo contiene las funciones básicas del CRUD de Cargos en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Cargos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    nombre : str = Field(min_length=3, max_length=250),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre":"Cargo Demo",
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
from models.cargo import Cargos as CargosModel
from models.historico_cargos import HistoricoCargos as HistoricoCargosModel

#importamos el esquema de datos de Sociedades
from schemas.cargo import Cargos as CargosSchema



# esto representa los metodos implementados en la tabla
class cargosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sociedades
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_cargo(self, cargo: CargosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoCargosModel(
                sede_id=cargo.id,
                sociedad_id=cargo.sociedad_id,
                nombre=cargo.nombre,
                direccion=cargo.direccion,
                region_id=cargo.region_id,
                comuna_id=cargo.comuna_id,
                ciudad=cargo.ciudad,
                created=cargo.created,
                updated=cargo.updated,
                creator_user=cargo.creator_user,
                updater_user=cargo.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoSociedad)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del banco 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  sociedad que se desea insertar       
    def create_cargo(self, cargo:CargosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreSede=cargo.nombre.upper().strip()

        # contamos si existe una sociedad con el mismo nombre
        nRecordNombre = self.db.query(CargosModel).filter(CargosModel.nombre == nombreSede).count()  


        if (nRecordNombre > 0):
            # buscamos la sociedad con el nombre y lo devolvemos
            cargoExists=self.db.query(CargosModel).filter(CargosModel.nombre == nombreSede).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sociedad con ese nombre","data":cargoExists})          
        else:    
            #creamos el nuevo registro de banco
            try:
                newSede=CargosModel(
                    sociedad_id=cargo.sociedad_id,
                    nombre=((cargo.nombre).upper()).strip(),
                    region_id=cargo.region_id,
                    comuna_id=cargo.comuna_id,
                    direccion=((cargo.direccion).upper()).strip(),
                    ciudad=((cargo.ciudad).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newSede)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_cargo(newSede,"Se creó una sociedad en el sistema")
  
                data={
                    "sociedad_id":newcargo.sociedad_id,
                    "nombre": newcargo.nombre,
                    "region_id":newcargo.region_id,
                    "comuna_id":newcargo.comuna_id,
                    "ciudad":newcargo.ciudad,
                    "direccion":newcargo.direccion,
                    "created": newcargo.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newcargo.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newcargo.creator_user,
                    "updater_user":newcargo.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una sede
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_cargo(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(CargosModel).filter(CargosModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta sede
            try:
                sedeExits = self.db.query(CargosModel).filter(CargosModel.id == id).first()                  
                # devolvemos los datos de la sede
                return ({"result":"1","estado":"Se consiguieron los datos de la sede","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las cargos
    # @params cadena: cadena que se buscara en la tabla cargos comparando con el campo nombre 
    def search_cargos(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(CargosModel).filter(CargosModel.nombre.like(findingT) | CargosModel.direccion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(CargosModel).filter(CargosModel.nombre.like(findingT) | CargosModel.direccion.like(findingT))
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
    # @params sociedad: esquema de los datos de la sede
    # @params id: Id de la sociedad que será actualizado
    def update_cargo(self, cargo:CargosSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(CargosModel).filter(CargosModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                cargoExists = self.db.query(CargosModel).filter(CargosModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_cargo(cargoExists ,"Actualización de la data de la sociedad")

                #registramnos los cambios en la tabla de bancarios del usuario
                cargoExists.nombre=((cargo.nombre).upper()).strip(),
                cargoExists.updated=ahora,
                cargoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":cargoExists.id,
                    "nombre":cargoExists.nombre,
                    "created":cargoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":cargoExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":cargoExists.creator_user,
                    "updater_user":cargoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato del cargo","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las cargos
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cargos(self, page, records):
        consulta = self.db.query(CargosModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para consultar todas las cargos
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cargos_sociedad(self,idSociedad, page, records):
        consulta = self.db.query(CargosModel).filter(CargosModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sociedad que se esta consultando
    def list_history_cargos(self, page:int, records: int, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoCargosModel).filter(HistoricoCargosModel.sociedad_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCargosModel).filter(HistoricoCargosModel.sociedad_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la sede ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     