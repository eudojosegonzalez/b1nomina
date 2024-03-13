'''
Este archivo contiene las funciones básicas del CRUD de Prevision Salud
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="PrevisionSalud"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    codigo_externo = Column(VARCHAR(50), unique=True, nullable=False)
    nombre = Column(VARCHAR(100), nullable=False)
    prevision_salud_cuenta = Column(VARCHAR(150), nullable=False)
    codigo_direccion_trabajo = Column(VARCHAR(10), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field (ge=1, le=1000)
    nombre : str = Field(min_length=3, max_length=250)
    prevision_salud_cuenta : str = Field(min_length=3, max_length=150)
    codigo_direccion_trabajo: str = Field(min_length=0, max_length=10)  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "nombre":"Banmédica",
                    "prevision_salud_cuenta": "21050002",
                    "codigo_direccion_trabajo": "3",
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
from models.prevision_salud import PrevisionSalud as PrevisionSaludModel
from models.historico_prevision_salud import HistoricoPrevisionSalud as HistoricoPrevisionSaludModel


#importamos el esquema de datos de Sociedades
from schemas.prevision_salud import PrevisionSalud as PrevisionSaludSchema



# esto representa los metodos implementados en la tabla
class PrevisionSaludController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sedes
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_prevision_salud(self, prevision:PrevisionSaludSchema, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newPrevisionSalud= HistoricoPrevisionSaludModel(
                prevision_id=prevision.id,
                codigo_externo=prevision.codigo_externo,
                nombre=prevision.nombre,
                prevision_salud_cuenta=prevision.prevision_salud_cuenta,
                codigo_direccion_trabajo=prevision.codigo_direccion_trabajo,
                created=prevision.created,
                updated=prevision.updated,
                creator_user=prevision.creator_user,
                updater_user=prevision.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newPrevisionSalud)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la sede
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  sede  que se desea insertar       
    def create_prevision_salud(self, prevision:PrevisionSaludSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombrePrevision=prevision.nombre.upper().strip()

        # contamos si existe una sede con el mismo nombre
        nRecordNombre = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.nombre == nombrePrevision).count()  


        if (nRecordNombre > 0):
            # buscamos la sede con el nombre y lo devolvemos
            previsionExists=self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.nombre == nombrePrevision).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una Prevision Salud con ese nombre","data":previsionExists})          
        else:    
            #creamos el nuevo registro de sedes
            try:
                newPrevision=PrevisionSaludModel(
                    codigo_externo=prevision.codigo_externo,
                    nombre=prevision.nombre,
                    prevision_salud_cuenta=prevision.prevision_salud_cuenta,
                    codigo_direccion_trabajo=prevision.codigo_direccion_trabajo,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newSede)
                self.db.commit()

                #creamos el registro historico de sedes
                self.create_historico_prevision_salud(newSede,"Se creó una sede en el sistema")
  
                data={
                    "sociedad_id":newprevision.sociedad_id,
                    "nombre": newprevision.nombre,
                    "region_id":newprevision.region_id,
                    "comuna_id":newprevision.comuna_id,
                    "ciudad":newprevision.ciudad,
                    "direccion":newprevision.direccion,
                    "created": newprevision.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newprevision.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newprevision.creator_user,
                    "updater_user":newprevision.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una sede
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_prevision_salud(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta sede
            try:
                sedeExits = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.id == id).first()                  
                # devolvemos los datos de la sede
                return ({"result":"1","estado":"Se consiguieron los datos de la sede","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las sedes
    # @params cadena: cadena que se buscara en la tabla sedes comparando con el campo nombre 
    def search_prevision_saluds(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.nombre.like(findingT) | PrevisionSaludModel.direccion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.nombre.like(findingT) | PrevisionSaludModel.direccion.like(findingT))
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
    # @params id: Id de la sede que será actualizado
    def update_prevision_salud(self, sede:SedeSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                sedeExists = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_prevision_salud(sedeExists ,"Actualización de la data de la sede")

                #registramnos los cambios en la tabla de sedes
                sedeExists.sociedad_id=prevision.sociedad_id,
                sedeExists.nombre=((prevision.nombre).upper()).strip(),
                sedeExists.region_id=prevision.region_id,
                sedeExists.comuna_id=prevision.comuna_id,
                sedeExists.direccion=((prevision.direccion).upper()).strip(),
                sedeExists.ciudad=((prevision.ciudad).upper()).strip(),
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
    def list_prevision_saluds(self, page, records):
        consulta = self.db.query(PrevisionSaludModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para consultar todas las sedes
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_prevision_saluds_sociedad(self,idSociedad, page, records):
        consulta = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sociedad que se esta consultando
    def list_history_prevision_saluds(self, page:int, records: int, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoPrevisionSaludModel).filter(HistoricoPrevisionSaludModel.sociedad_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoPrevisionSaludModel).filter(HistoricoPrevisionSaludModel.sociedad_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorySede=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la sede ","data": listHistorySede})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     