'''
Este archivo contiene las funciones básicas del CRUD de departamentos en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="departamento"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("departamento.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    nombre = Column(VARCHAR(200), nullable=False)
    direccion = Column (TEXT, nullable=True)      
    region_id = Column (BIGINT, ForeignKey("Regiones.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    comuna_id = Column (BIGINT, ForeignKey("Comunas.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)
    ciudad = Column(VARCHAR(250), nullable=False)
    icono = Column(VARCHAR(250), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000),
    nombre : str = Field(min_length=3, max_length=250),
    direccion : str = Field(min_length=3, max_length=500),
    region_id : int = Field(ge=1, le=1000),
    comuna_id : int = Field(ge=1, le=1000),
    ciudad : str = Field(min_length=3, max_length=250),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "nombre":"departamento Demo",
                    "direccion": "Direccion departamento Demo",
                    "region_id": 1,
                    "comuna_id": 1101,
                    "ciudad":"Demo ciudad"
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
from models.departamento import departamento as departamentoModel
from models.historico_departamento import Historicodepartamento as HistoricodepartamentoModel

#importamos el esquema de datos de Sociedades
from schemas.departamento import departamento as departamentoSchema



# esto representa los metodos implementados en la tabla
class departamentosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sociedades
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_departamento(self, departamento: departamentoModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricodepartamentoModel(
                departamento_id=departamento.id,
                sociedad_id=departamento.sociedad_id,
                nombre=departamento.nombre,
                direccion=departamento.direccion,
                region_id=departamento.region_id,
                comuna_id=departamento.comuna_id,
                ciudad=departamento.ciudad,
                created=departamento.created,
                updated=departamento.updated,
                creator_user=departamento.creator_user,
                updater_user=departamento.updater_user,
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
    def create_departamento(self, departamento:departamentoSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombredepartamento=departamento.nombre.upper().strip()

        # contamos si existe una sociedad con el mismo nombre
        nRecordNombre = self.db.query(departamentoModel).filter(departamentoModel.nombre == nombredepartamento).count()  


        if (nRecordNombre > 0):
            # buscamos la sociedad con el nombre y lo devolvemos
            departamentoExists=self.db.query(departamentoModel).filter(departamentoModel.nombre == nombredepartamento).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sociedad con ese nombre","data":departamentoExists})          
        else:    
            #creamos el nuevo registro de banco
            try:
                newdepartamento=departamentoModel(
                    sociedad_id=departamento.sociedad_id,
                    nombre=((departamento.nombre).upper()).strip(),
                    region_id=departamento.region_id,
                    comuna_id=departamento.comuna_id,
                    direccion=((departamento.direccion).upper()).strip(),
                    ciudad=((departamento.ciudad).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newdepartamento)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_departamento(newdepartamento,"Se creó una sociedad en el sistema")
  
                data={
                    "sociedad_id":newdepartamento.sociedad_id,
                    "nombre": newdepartamento.nombre,
                    "region_id":newdepartamento.region_id,
                    "comuna_id":newdepartamento.comuna_id,
                    "ciudad":newdepartamento.ciudad,
                    "direccion":newdepartamento.direccion,
                    "created": newdepartamento.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newdepartamento.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newdepartamento.creator_user,
                    "updater_user":newdepartamento.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una departamento
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_departamento(self,id:int):

        # buscamos si este existe esta departamento
        nRecord = self.db.query(departamentoModel).filter(departamentoModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta departamento
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta departamento
            try:
                departamentoExits = self.db.query(departamentoModel).filter(departamentoModel.id == id).first()                  
                # devolvemos los datos de la departamento
                return ({"result":"1","estado":"Se consiguieron los datos de la departamento","data":departamentoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las departamentos
    # @params cadena: cadena que se buscara en la tabla departamentos comparando con el campo nombre 
    def search_departamentos(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(departamentoModel).filter(departamentoModel.nombre.like(findingT) | departamentoModel.direccion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(departamentoModel).filter(departamentoModel.nombre.like(findingT) | departamentoModel.direccion.like(findingT))
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
            
 
    #metodo para actualizar los datos de una departamento por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la departamento
    # @params id: Id de la sociedad que será actualizado
    def update_departamento(self, departamento:departamentoSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(departamentoModel).filter(departamentoModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la departamento
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                departamentoExists = self.db.query(departamentoModel).filter(departamentoModel.id == id).first()             

                #creamos el registro historico de departamento
                self.create_historico_departamento(departamentoExists ,"Actualización de la data de la sociedad")

                #registramnos los cambios en la tabla de bancarios del usuario
                departamentoExists.sociedad_id=departamento.sociedad_id,
                departamentoExists.nombre=((departamento.nombre).upper()).strip(),
                departamentoExists.region_id=departamento.region_id,
                departamentoExists.comuna_id=departamento.comuna_id,
                departamentoExists.direccion=((departamento.direccion).upper()).strip(),
                departamentoExists.ciudad=((departamento.ciudad).upper()).strip(),
                departamentoExists.updated=ahora,
                departamentoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":departamentoExists.id,
                    "departamento_id":departamentoExists.sociedad_id,
                    "nombre":departamentoExists.nombre,
                    "region_id":departamentoExists.region_id,
                    "comuna_id":departamentoExists.comuna_id,
                    "direccion":departamentoExists.direccion,
                    "ciudad":departamentoExists.ciudad,
                    "created":departamentoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":departamentoExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":departamentoExists.creator_user,
                    "updater_user":departamentoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la departamento","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las departamentos
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_departamentos(self, page, records):
        consulta = self.db.query(departamentoModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para consultar todas las departamentos
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_departamentos_sociedad(self,idSociedad, page, records):
        consulta = self.db.query(departamentoModel).filter(departamentoModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una departamento
    # @params id: Id de la sociedad que se esta consultando
    def list_history_departamentos(self, page:int, records: int, id:int):

        # buscamos si exite la departamento
        nRecord = self.db.query(HistoricodepartamentoModel).filter(HistoricodepartamentoModel.sociedad_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la departamento
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricodepartamentoModel).filter(HistoricodepartamentoModel.sociedad_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorydepartamento=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la departamento ","data": listHistorydepartamento})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     