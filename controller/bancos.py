'''
Este archivo contiene las funciones básicas del CRUD de Bancos del Sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    codigo = Column(VARCHAR(50), nullable=False, unique=True)
    nombre = Column(VARCHAR(150), nullable=False)
    nomina = Column(BOOLEAN, nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL, 



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    codigo : str = Field(min_length=3, max_length=50),
    nombre : str = Field(min_length=3, max_length=150),
    nomina : int 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo": "001",
                    "nombre":"BANCO CHILE Y EDWARDS",
                    "nomina": 1
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
from models.bancos import Bancos as BancosModel
from models.historico_bancos import HistoricoBancos as HistoricoBancosModel


# importamos el schema de datos
from schemas.bancos import Bancos as BancosSchema


# esto representa los metodos implementados en la tabla
class bancosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de bancos
    #@param banco: Modelo del registro de Bancos
    #@param observavacion: Observación sobre el historico
    def create_historico_bancos (self, banco: BancosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoBanco= HistoricoBancosModel(
                
                banco_id = banco.id,
                codigo = banco.codigo,
                nombre = banco.nombre,
                nomina = banco.nomina,
                created = banco.created,
                updated = banco.updated,
                creator_user= banco.creator_user,
                updater_user = banco.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoBanco)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del banco 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params banco: esquema de los datos banco que se desea insertar       
    def create_banco(self, banco:BancosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreBanco=banco.nombre.upper().strip()
        codigoBanco=banco.codigo.upper().strip()


        # contamos si existe un banco con el mismo nombre
        nRecordNombre = self.db.query(BancosModel).filter(BancosModel.nombre == nombreBanco).count()  

        # contamos si existe un banco con el mismo código 
        nRecordCodigo = self.db.query(BancosModel).filter(BancosModel.codigo == codigoBanco).count()  

        if (nRecordNombre > 0):
            # buscamos el banco con el nombre y lo devolvemos
            bancoExists=self.db.query(BancosModel).filter(BancosModel.nombre == nombreBanco).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-1","estado":"Existe un banco con ese nombre","data":bancoExists})
        elif (nRecordCodigo>0):
            # buscamos el bnco ccon el mismo codigo
            bancoExists=self.db.query(BancosModel).filter(BancosModel.codigo == codigoBanco).first() 

            # devolvemos el banco que ya existe
            return ({"result":"-2","estado":"Existe un banco con ese codigo","data":bancoExists})            
        else:    
            #creamos el nuevo registro de banco
            try:
                newBanco=BancosModel(
                    codigo=((banco.codigo).upper()).strip(),
                    nombre=((banco.nombre).upper()).strip(),
                    nomina=banco.nomina,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newBanco)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_bancos(newBanco,"Se creó un banco en el sistema")
  
                data={
                    "id":newBanco.id,
                    "codigo": newBanco.codigo,
                    "nombre": newBanco.nombre,
                    "nomina": newBanco.nomina,
                    "created": newBanco.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newBanco.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newBanco.creator_user,
                    "updater_user":newBanco.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un banco por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_banco(self,id:int):

        # buscamos los datos bancarios
        nRecord = self.db.query(BancosModel).filter(BancosModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este banco
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                bancoExits = self.db.query(BancosModel).filter(BancosModel.id == id).first()                  
                '''
                __tablename__="Bancos"
                id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
                codigo = Column(VARCHAR(50), nullable=False, unique=True)
                nombre = Column(VARCHAR(150), nullable=False)
                nomina = Column(BOOLEAN, nullable=False)
                created = Column (DateTime, nullable=False) #datetime NOT NULL,    
                updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
                creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
                updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,                 
                '''
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos del banco","data":bancoExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los bancos
    # @params cadena: cadena que se buscara en la tabla banco comparando con el campo nombre y codigo      
    def search_banco(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(BancosModel).filter(BancosModel.nombre.like(findingT) | BancosModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(BancosModel).filter(BancosModel.nombre.like(findingT) | BancosModel.nombre.like(findingT))
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
    # @params banco: esquema de los datos de banco  
    # @params id: Id del banco que será actualizado
    def update_banco(self, banco:BancosSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(BancosModel).filter(BancosModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del banco
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                bancoExists = self.db.query(BancosModel).filter(BancosModel.id == id).first()             

                #creamos el registro historico de bancos
                self.create_historico_bancos(bancoExists ,"Actualización de la data del banco")

                #registramnos los cambios en la tabla de bancarios del usuario
                bancoExists.codigo=((banco.codigo).upper()).strip(),
                bancoExists.nombre=((banco.nombre).upper()).strip(),
                bancoExists.updated=ahora,
                bancoExists.updater_user=userUpdaterId               

                if (banco.nomina==1):
                    bancoExists.nomina=True
                else:
                    bancoExists.nomina=False

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
                return ({"result":"1","estado":"Se actualizó la data del Banco","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todos los bancos
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_bancos(self, page, records):
        consulta = self.db.query(BancosModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos de un banco
    # @params id: Id del banco que se esta consultando
    def list_history_bancos(self, page:int, records: int, id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricoBancosModel).filter(HistoricoBancosModel.banco_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del banco
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoBancosModel).filter(HistoricoBancosModel.banco_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistoryBancos=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos del banco ","data": listHistoryBancos})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     