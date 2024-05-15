'''
Este archivo contiene las funciones básicas del CRUD de los Departamentos
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Departamentos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column (BIGINT, ForeignKey("Sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False) 
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000),
    sede_id : int = Field(ge=1, le=1000),    
    nombre : str = Field(min_length=3, max_length=250)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "sede_id": 1,
                    "nombre":"Departamento Demo"
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
from models.departamentos import Departamentos as DepartamentosModel
from models.historico_departamentos import HistoricoDepartamentos as HistoricosDepartamentosModel

#importamos el esquema de datos de Sociedades
from schemas.departamentos import Departamentos as DepartamentosSchema



# esto representa los metodos implementados en la tabla
class DepartamentosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sociedades
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_departamento(self, departamento: DepartamentosSchema, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoDepartamento= HistoricosDepartamentosModel(
                departamento_id=departamento.id,
                sede_id=departamento.sede_id,
                sociedad_id=departamento.sociedad_id,
                nombre=departamento.nombre,
                created=departamento.created,
                updated=departamento.updated,
                creator_user=departamento.creator_user,
                updater_user=departamento.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoDepartamento)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de un departamento
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  sociedad que se desea insertar       
    def create_departamento(self, departamento:DepartamentosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreSede=departamento.nombre.upper().strip()

        # contamos si existe una sociedad con el mismo nombre
        nRecordNombre = self.db.query(DepartamentosModel).filter(DepartamentosModel.nombre == nombreSede).count()  


        if (nRecordNombre > 0):
            # buscamos la sociedad con el nombre y lo devolvemos
            departamentoExists=self.db.query(DepartamentosModel).filter(DepartamentosModel.nombre == nombreSede).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sociedad con ese nombre","data":departamentoExists})          
        else:    
            #creamos el nuevo registro de banco
            try:
                newDepartamento=DepartamentosModel(
                    sociedad_id=departamento.sociedad_id,
                    sede_id=departamento.sede_id,
                    nombre=((departamento.nombre).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newDepartamento)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_departamento(newDepartamento,"Se creó un departamento en el sistema")
  
                data={
                    "sociedad_id":newDepartamento.sociedad_id,
                    "sede_id":newDepartamento.sede_id,
                    "nombre": newDepartamento.nombre,
                    "created": newDepartamento.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newDepartamento.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newDepartamento.creator_user,
                    "updater_user":newDepartamento.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una sede
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_departamento(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DepartamentosModel).filter(DepartamentosModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta sede
            try:
                sedeExits = self.db.query(DepartamentosModel).filter(DepartamentosModel.id == id).first()                  
                # devolvemos los datos de la sede
                return ({"result":"1","estado":"Se consiguieron los datos de la sede","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los departamentos
    # @params cadena: cadena que se buscara en la tabla sedes comparando con el campo nombre 
    def search_departamentos(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(DepartamentosModel).filter(DepartamentosModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(DepartamentosModel).filter(DepartamentosModel.nombre.like(findingT))
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
    def update_departamento(self, departamento:DepartamentosSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(DepartamentosModel).filter(DepartamentosModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                departamentoExists = self.db.query(DepartamentosModel).filter(DepartamentosModel.id == id).first()             

                #creamos el registro historico del departamento
                self.create_historico_departamento(departamentoExists ,"Actualización de la data del departamento")

                #registramnos los cambios en la tabla de bancarios del usuario
                departamentoExists.sociedad_id=departamento.sociedad_id,
                departamentoExists.sede_id=departamento.sede_id,
                departamentoExists.nombre=((departamento.nombre).upper()).strip(),

                departamentoExists.updated=ahora,
                departamentoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":departamentoExists.id,
                    "sociedad_id":departamentoExists.sociedad_id,
                    "sede_id":departamentoExists.sede_id,
                    "nombre":departamentoExists.nombre,
                    "created":departamentoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":departamentoExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":departamentoExists.creator_user,
                    "updater_user":departamentoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de un departamento","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    

    # metodo para consultar todas los departamentos de una sociedad se toman en cuenta todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_departamentos_sociedad(self, page, records,socidadId):
        consulta = self.db.query(DepartamentosModel).filter(DepartamentosModel.sociedad_id==socidadId)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)
    
    # metodo para consultar todas los departamentos de una sociedad segun una sede
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_departamentos_sociedad_sede(self, page, records,socidadId,sedeId):
        consulta = self.db.query(DepartamentosModel).filter(and_(DepartamentosModel.sociedad_id==socidadId,  DepartamentosModel.sede_id==sedeId))
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)    
    
    
    # metodo para consultar todas los departamentos de una sede
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_departamentos_sede(self, page, records, sedeId):
        consulta = self.db.query(DepartamentosModel).filter(DepartamentosModel.sede_id==sedeId)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)    


    # metodo para listar los datos historicos  de un departamento
    # @params id: Id de la sociedad que se esta consultando
    def list_history_departamentos(self, page:int, records: int, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricosDepartamentosModel).filter(HistoricosDepartamentosModel.departamento_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricosDepartamentosModel).filter(HistoricosDepartamentosModel.departamento_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la sede ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     