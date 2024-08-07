'''
Este archivo contiene las funciones básicas del CRUD de Mutuales del Sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(VARCHAR(150), nullable=False)
    codigo_externo = Column(VARCHAR(50), nullable=False)
    cuenta_contable = Column(VARCHAR(50), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    nombre : str = Field(min_length=3, max_length=50),
    codigo_externo : str = Field(min_length=3, max_length=50),
    cuenta_contable : str = Field(min_length=3, max_length=50),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Asociación Chilena de seguridad (ACHS)",
                    "codigo_externo":"01",
                    "cuenta_contable": "21050004"
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
from models.mutuales import Mututales as mutualesModel
from models.historico_mutuales import HistoricoMututales as HistoricomutualesModel


# importamos el schema de datos
from schemas.mutuales import Mutuales as mutualesSchema


# esto representa los metodos implementados en la tabla
class mutualesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de mutuales
    #@param mutual: Modelo del registro de mutuales
    #@param observavacion: Observación sobre el historico
    def create_historico_mutuales (self, mutual: mutualesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoMutual= HistoricomutualesModel(
                mutuales_id = mutual.id,
                codigo_externo = mutual.codigo_externo,
                nombre = ((mutual.nombre).upper()).strip(),
                cuenta_contable=mutual.cuenta_contable,
                created = mutual.created,
                updated = mutual.updated,
                creator_user= mutual.creator_user,
                updater_user = mutual.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoMutual)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del banco 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params mutual: esquema de los datos banco que se desea insertar       
    def create_mutuales(self, mutual:mutualesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreMutual=mutual.nombre.upper().strip()
        codigoMutual=mutual.codigo_externo.upper().strip()


        # contamos si existe un banco con el mismo nombre
        nRecordNombre = self.db.query(mutualesModel).filter(mutualesModel.nombre == nombreMutual).count()  

        # contamos si existe un banco con el mismo código 
        nRecordCodigo = self.db.query(mutualesModel).filter(mutualesModel.codigo_externo == codigoMutual).count()  

        if (nRecordNombre > 0):
            # buscamos el banco con el nombre y lo devolvemos
            mutualExists=self.db.query(mutualesModel).filter(mutualesModel.nombre == nombreMutual).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-1","estado":"Existe una Mutual con ese nombre","data":mutualExists})
        elif (nRecordCodigo>0):
            # buscamos el bnco ccon el mismo codigo
            bancoExists=self.db.query(mutualesModel).filter(mutualesModel.codigo_externo == codigoMutual).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-2","estado":"Existe un banco con ese codigo","data":mutualExists})            
        else:    
            #creamos el nuevo registro de banco
            try:
                newMutual=mutualesModel(
                    codigo_externo=mutual.codigo_externo,
                    nombre=((mutual.nombre).upper()).strip(),
                    cuenta_contable=mutual.cuenta_contable,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newMutual)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_mutuales(newMutual,"Se creó una Mutual en el sistema")
  
                data={
                    "id":newMutual.id,
                    "codigo_externo":newMutual.codigo_externo,
                    "nombre":newMutual.nombre,
                    "cuenta_contable":newMutual.cuenta_contable,
                    "created":newMutual.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newMutual.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newMutual.creator_user,
                    "updater_user":newMutual.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un banco por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_mutuales(self,id:int):

        # buscamos los datos bancarios
        nRecord = self.db.query(mutualesModel).filter(mutualesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este banco
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de de la mutual
            try:
                bancoExits = self.db.query(mutualesModel).filter(mutualesModel.id == id).first()                  

                # devolvemos los datos de la mutual
                return ({"result":"1","estado":"Se consiguieron los datos del banco","data":bancoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los mutuales
    # @params cadena: cadena que se buscara en la tabla banco comparando con el campo nombre y codigo      
    def search_mutuales(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(mutualesModel).filter(mutualesModel.nombre.like(findingT) | mutualesModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(mutualesModel).filter(mutualesModel.nombre.like(findingT) | mutualesModel.nombre.like(findingT))
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
            
 
    #metodo para actualizar los datos de un banco por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params mutual: esquema de los datos de banco  
    # @params id: Id del banco que será actualizado
    def update_mutuales(self, mutual:mutualesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(mutualesModel).filter(mutualesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del banco
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                bancoExists = self.db.query(mutualesModel).filter(mutualesModel.id == id).first()             

                #creamos el registro historico de bancarios del usuario
                self.create_historico_mutuales(bancoExists ,"Actualización de la data del banco")

                #registramnos los cambios en la tabla de bancarios del usuario
                bancoExists.codigo=((mutual.codigo).upper()).strip(),
                bancoExists.nombre=((mutual.nombre).upper()).strip(),
                bancoExists.updated=ahora,
                bancoExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":bancoExists.id,
                    "codigo":bancoExists.codigo,
                    "nombre":bancoExists.nombre,
                    "nomina":bancoExists.nomina,
                    "created":bancoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":bancoExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":bancoExists.creator_user,
                    "updater_user":bancoExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de contacto del usuario","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todos los mutuales
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_mutuales(self, page, records):
        consulta = self.db.query(mutualesModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos de un banco
    # @params id: Id del banco que se esta consultando
    def list_history_mutuales(self, page:int, records: int, id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricomutualesModel).filter(HistoricomutualesModel.mutuales_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del banco
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricomutualesModel).filter(HistoricomutualesModel.mutuales_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorymutuales=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos del mutual ","data": listHistorymutuales})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     