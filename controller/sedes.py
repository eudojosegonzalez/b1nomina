'''
Este archivo contiene las funciones básicas del CRUD de Sedes en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="Sede"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("sede.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
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
                    "nombre":"Sede Demo",
                    "direccion": "Direccion Sede Demo",
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
from models.sede import Sede as SedeModel
from models.historico_sede import HistoricoSede as HistoricoSedeModel

#importamos el esquema de datos de Sede
from schemas.sede import Sede as SedeSchema



# esto representa los metodos implementados en la tabla
class sedesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sedes
    #@param sede: Modelo del registro de Sede
    #@param observavacion: Observación sobre el historico
    def create_historico_sede(self, sede: SedeModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoSedeModel(
                sede_id=sede.id,
                sociedad_id=sede.sociedad_id,
                nombre=sede.nombre,
                direccion=sede.direccion,
                region_id=sede.region_id,
                comuna_id=sede.comuna_id,
                ciudad=sede.ciudad,
                created=sede.created,
                updated=sede.updated,
                creator_user=sede.creator_user,
                updater_user=sede.updater_user,
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
    
    
    #metodo para insertar  los datos de la sede
    # @userCreatorId: Id del usuario que está creando el registro
    # @params sede: esquema de los datos de  sede  que se desea insertar       
    def create_sede(self, sede:SedeSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreSede=sede.nombre.upper().strip()

        # contamos si existe una sede con el mismo nombre
        nRecordNombre = self.db.query(SedeModel).filter(SedeModel.nombre == nombreSede).count()  


        if (nRecordNombre > 0):
            # buscamos la sede con el nombre y lo devolvemos
            sedeExists=self.db.query(SedeModel).filter(SedeModel.nombre == nombreSede).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sede con ese nombre","data":sedeExists})          
        else:    
            #creamos el nuevo registro de sedes
            try:
                newSede=SedeModel(
                    sociedad_id=sede.sociedad_id,
                    nombre=((sede.nombre).upper()).strip(),
                    region_id=sede.region_id,
                    comuna_id=sede.comuna_id,
                    direccion=((sede.direccion).upper()).strip(),
                    ciudad=((sede.ciudad).upper()).strip(),
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newSede)
                self.db.commit()

                #creamos el registro historico de sedes
                self.create_historico_sede(newSede,"Se creó una sede en el sistema")
  
                data={
                    "sociedad_id":newSede.sociedad_id,
                    "nombre": newSede.nombre,
                    "region_id":newSede.region_id,
                    "comuna_id":newSede.comuna_id,
                    "ciudad":newSede.ciudad,
                    "direccion":newSede.direccion,
                    "created": newSede.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newSede.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newSede.creator_user,
                    "updater_user":newSede.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos de una sede
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_sede(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(SedeModel).filter(SedeModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta sede
            try:
                sedeExits = self.db.query(SedeModel).filter(SedeModel.id == id).first()                  
                # devolvemos los datos de la sede
                return ({"result":"1","estado":"Se consiguieron los datos de la sede","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    # metodo para efectuar búsquedas en las sedes
    # @params cadena: cadena que se buscara en la tabla sedes comparando con el campo nombre 
    def search_sedes(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(SedeModel).filter(SedeModel.nombre.like(findingT) | SedeModel.direccion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(SedeModel).filter(SedeModel.nombre.like(findingT) | SedeModel.direccion.like(findingT))
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
            
 
    # metodo para actualizar los datos de una sede por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sede: esquema de los datos de la sede
    # @params id: Id de la sede que será actualizado
    def update_sede(self, sede:SedeSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este sede existe
        nRecord = self.db.query(SedeModel).filter(SedeModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                sedeExists = self.db.query(SedeModel).filter(SedeModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_sede(sedeExists ,"Actualización de la data de la sede")

                #registramnos los cambios en la tabla de sedes
                sedeExists.sociedad_id=sede.sociedad_id,
                sedeExists.nombre=((sede.nombre).upper()).strip(),
                sedeExists.region_id=sede.region_id,
                sedeExists.comuna_id=sede.comuna_id,
                sedeExists.direccion=((sede.direccion).upper()).strip(),
                sedeExists.ciudad=((sede.ciudad).upper()).strip(),
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
                return ({"result":"1","estado":"Se actualizó el dato de la sede","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sedes(self, page, records):
        consulta = self.db.query(SedeModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sedes_sociedad(self,idSociedad, page, records):
        consulta = self.db.query(SedeModel).filter(SedeModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sede que se esta consultando
    def list_history_sedes(self, page:int, records: int, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoSedeModel).filter(HistoricoSedeModel.sede_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de la sede
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoSedeModel).filter(HistoricoSedeModel.sede_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la sede ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     