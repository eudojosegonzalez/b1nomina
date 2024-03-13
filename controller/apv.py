'''
Este archivo contiene las funciones básicas del CRUD de Instuciones APV del Sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    id = Column(BIGINT, primary_key=True,  nullable=False)
    nombre = Column(VARCHAR(30), nullable=False)
    nombre_largo = Column(VARCHAR(250), nullable=False)
    cuenta_contable=Column(VARCHAR(100), nullable=True)
    codigo_externo=Column(VARCHAR(50), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    id : int = Field (min=1, max=2000) ,
    nombre  : str = Field(min_length=3, max_length=300)  ,
    nombre_largo  : str = Field(min_length=3, max_length=250)  ,    
    cuenta_contable : str = Field(min_length=0, max_length=100)  ,    
    codigo_externo : str = Field(min_length=0, max_length=50)  ,    
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id" : "5",
                    "nombre"  : "Habitat",
                    "nombre_largo"  : "Habitat",
                    "cuenta_contable": '21050001',
                    "codigo_externo": '005'
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
from models.apv import APVInstituciones as APVModel
from models.historico_apv import HistoricoAPVInstituciones as HistoricoAPVModel

# importamos el schema de datos
from schemas.apv import APVInstituciones as APVSchema


# esto representa los metodos implementados en la tabla
class APVController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de APVs
    #@param APV: Modelo del registro de APVs
    #@param observavacion: Observación sobre el historico
    def create_historico_apv (self, APV: APVModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            '''
            `id` bigint auto_increment not null,
            `apv_id` bigint  not null,
            `nombre` varchar(30) not NULL,
            `nombre_largo` varchar(250) not NULL,
            `cuenta_contable` varchar(100)  NULL,
            `codigo_externo` varchar(50) NULL,
            `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
            `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
            `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
            `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro', 
            `fecha_registro` datetime NOT NULL COMMENT 'fecha en que fue creado el registro historico',
            `observaciones` text DEFAULT NULL COMMENT 'observaciones del historico',    
            '''            
            newHistoricoAPV= HistoricoAPVModel(
                apv_id=APV.id,
                nombre = APV.nombre,
                nombre_largo = APV.nombre_largo,
                cuenta_contable=APV.cuenta_contable,
                codigo_externo=APV.codigo_externo,
                created = APV.created,
                updated = APV.updated,
                creator_user= APV.creator_user,
                updater_user = APV.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoAPV)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del APV 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params APV: esquema de los datos APV que se desea insertar       
    def create_apv(self, APV:APVSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreAPV=APV.nombre.upper().strip()
        codigoExternoAPV=APV.codigo_externo.upper().strip()


        # contamos si existe un APV con el mismo nombre
        nRecordNombre = self.db.query(APVModel).filter(APVModel.nombre == nombreAPV).count()  

        # contamos si existe un APV con el mismo código 
        nRecordCodigo = self.db.query(APVModel).filter(APVModel.codigo_externo == codigoExternoAPV).count()  

        if (nRecordNombre > 0):
            # buscamos el APV con el nombre y lo devolvemos
            APVExists=self.db.query(APVModel).filter(APVModel.nombre == nombreAPV).first() 

            # devolvemos el APV que ya existe
            return ({"result":"-1","estado":"Existe un APV con ese nombre","data":APVExists})
        elif (nRecordCodigo>0):
            # buscamos el bnco ccon el mismo codigo
            APVExists=self.db.query(APVModel).filter(APVModel.codigo_externo == codigoExternoAPV).first() 

            # devolvemos el APV que ya existe
            return ({"result":"-2","estado":"Existe un APV con ese codigo","data":APVExists})            
        else:    
            #creamos el nuevo registro de APV
            try:
                newAPV=APVModel(
                    id=APV.id,
                    nombre=((APV.nombre).upper()).strip(),
                    nombre_largo=((APV.nombre_largo).upper()).strip(),
                    codigo_externo=((APV.codigo_externo).upper()).strip(),
                    cuenta_contable=(APV.cuenta_contable).strip(),                    
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newAPV)
                self.db.commit()

                #creamos el registro historico de las intituciones APV
                self.create_historico_apv(newAPV,"Se creó un APV en el sistema")

                data={
                    "id":newAPV.id,
                    "nombre": newAPV.nombre,
                    "nombre_largo": newAPV.nombre_largo,
                    "codigo_externo": newAPV.codigo_externo,
                    "cuenta_contable":newAPV.cuenta_contable,
                    "created": newAPV.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newAPV.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newAPV.creator_user,
                    "updater_user":newAPV.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un APV por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_apv(self,id:int):

        # buscamos los datos bancarios
        nRecord = self.db.query(APVModel).filter(APVModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este APV
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de contacto del usuario
            try:
                APVExits = self.db.query(APVModel).filter(APVModel.id == id).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos del APV","data":APVExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los APVs
    # @params cadena: cadena que se buscara en la tabla APV comparando con el campo nombre y codigo      
    def search_apv(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes por nombre
            nRecordNombre=self.db.query(APVModel).filter(APVModel.nombre.like(findingT) | APVModel.nombre_largo.like(findingT) | APVModel.codigo_externo.like(findingT)).count()  

            # hay registros
            if (nRecordNombre >0):                 
                # ejecutamos la consulta
                consulta = self.db.query(APVModel).filter(APVModel.nombre.like(findingT) | APVModel.nombre_largo.like(findingT) | APVModel.codigo_externo.like(findingT)) 
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
            
 
    #metodo para actualizar los datos de un APV por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params APV: esquema de los datos de APV  
    # @params id: Id del APV que será actualizado
    def update_apv(self, APV:APVSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este APV existe
        nRecord = self.db.query(APVModel).filter(APVModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del APV
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                APVExists = self.db.query(APVModel).filter(APVModel.id == id).first()             

                #creamos el registro historico de bancarios del usuario
                self.create_historico_apv(APVExists ,"Actualización de la data del APV")

                #registramnos los cambios en la tabla de bancarios del usuario
                APVExists.nombre = ((APV.nombre).upper()).strip(),
                APVExists.nombre_largo = ((APV.nombre_largo).upper()).strip(),
                APVExists.codigo_externo = ((APV.codigo_externo).upper()).strip(),
                APVExists.cuenta_contable = ((APV.cuenta_contable).upper()).strip(),
                APVExists.updated = ahora,
                APVExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

               
                data={
                    "id":APVExists.id,
                    "nombre":APVExists.nombre,
                    "nombre_largo":APVExists.nombre_largo,
                    "cuenta_contable":APVExists.cuenta_contable,
                    "codigo_externo":APVExists.codigo_externo,                                        
                    "created":APVExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":APVExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":APVExists.creator_user,
                    "updater_user":APVExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó los datos de la Institucion APV","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todos los APVs
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_apv(self, page, records):
        consulta = self.db.query(APVModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos de un APV
    # @params id: Id del APV que se esta consultando
    def list_history_apv(self, page:int, records: int, id:int):

        # buscamos si exite el APV
        nRecord = self.db.query(HistoricoAPVModel).filter(HistoricoAPVModel.apv_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del APV
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del APV
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoAPVModel).filter(HistoricoAPVModel.apv_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistoryAPVs=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos del APV ","data": listHistoryAPVs})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     