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

    # funcion para crear el registro de historico las Previsiones Salud
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_prevision_salud(self, prevision:PrevisionSaludSchema, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newPrevisionSalud= HistoricoPrevisionSaludModel(
                codigo_externo=prevision.codigo_externo,
                prevision_salud_id=prevision.id,
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
            #creamos el nuevo registro de Prevision Salud
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
                self.db.add(newPrevision)
                self.db.commit()

                #creamos el registro historico de Prevision Salud
                self.create_historico_prevision_salud(newPrevision,"Se creó una Prevision Salud en el sistema")
  
                data={
                    "id":newPrevision.id,
                    "codigo_externo":newPrevision.codigo_externo,
                    "nombre": newPrevision.nombre,
                    "prevision_salud_cuenta": newPrevision.prevision_salud_cuenta,
                    "codigo_direccion_trabajo":newPrevision.codigo_direccion_trabajo,
                    "created": newPrevision.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newPrevision.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newPrevision.creator_user,
                    "updater_user":newPrevision.updater_user
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
                return ({"result":"1","estado":"Se consiguieron los datos de la Prevision Salud","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las Previsiones Salud
    # @params cadena: cadena que se buscara en la tabla sedes comparando con el campo nombre 
    def search_prevision_salud(self,finding):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.nombre.like(findingT) )
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
    def update_prevision_salud(self, prevision:PrevisionSaludSchema, userUpdaterId:int, id:int):
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
                previsionExists = self.db.query(PrevisionSaludModel).filter(PrevisionSaludModel.id == id).first()             

                #creamos el registro historico de sede
                self.create_historico_prevision_salud(previsionExists ,"Actualización de la data de la Prevision Salud")

                #registramnos los cambios en la tabla de Prevision Salud
                '''
                id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
                codigo_externo = Column(VARCHAR(50), unique=True, nullable=False)
                nombre = Column(VARCHAR(100), nullable=False)
                prevision_salud_cuenta = Column(VARCHAR(150), nullable=False)
                codigo_direccion_trabajo = Column(VARCHAR(10), nullable=True)
                created = Column (DateTime, nullable=False) #datetime NOT NULL,    
                updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
                creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
                updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,                
                '''
                previsionExists.codigo_externo=previsionExists.codigo_externo,
                previsionExists.nombre=((prevision.nombre).upper()).strip(),
                previsionExists.prevision_salud_cuenta=prevision.prevision_salud_cuenta,
                previsionExists.codigo_direccion_trabajo=prevision.codigo_direccion_trabajo,
                previsionExists.updated=ahora,
                previsionExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":previsionExists.id,
                    "codigo_externo":previsionExists.codigo_externo,
                    "nombre":previsionExists.nombre,
                    "prevision_salud_cuenta":previsionExists.prevision_salud_cuenta,
                    "codigo_direccion_trabajo":previsionExists.codigo_direccion_trabajo,
                    "created":previsionExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":previsionExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":previsionExists.creator_user,
                    "updater_user":previsionExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la sede","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las Previsiones Salud
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_prevision_salud(self):
        consulta = self.db.query(PrevisionSaludModel)
        result=consulta.all()
        return (result)



    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sociedad que se esta consultando
    def list_history_prevision_salud(self, id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoPrevisionSaludModel).filter(HistoricoPrevisionSaludModel.prevision_salud_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoPrevisionSaludModel).filter(HistoricoPrevisionSaludModel.prevision_salud_id == id)
                listHistoryPrevisionSalud=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la Prevision Salud ","data": listHistoryPrevisionSalud})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     