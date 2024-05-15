'''
Este archivo contiene las funciones básicas del CRUD de AFP del Sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    codigo_previred = Column(VARCHAR(50), unique=True, nullable=False)
    nombre = Column(VARCHAR(100), nullable=False)
    cotizacion=Column(NUMERIC(18,4),nullable=True)
    cuenta_AFP=Column(VARCHAR(150), nullable=True)
    sis=Column(NUMERIC(18,4),nullable=True)
    cuenta_sis_cred=Column(VARCHAR(20), nullable=True)
    cuenta_ahorro_AFP_cuenta2=Column(VARCHAR(150), nullable=True)
    codigo_direccion_trabajo=Column(VARCHAR(150), nullable=True)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    id : int = Field (min=1, max=2000) ,
    codigo_previred : str = Field(min_length=3, max_length=50) ,
    nombre  : str = Field(min_length=3, max_length=100)  ,
    cotizacion : float = Field (min=0, max=20000),
    cuenta_AFP : str = Field(min_length=0, max_length=50) ,
    sis : float   = Field (min=0, max=20000),   
    cuenta_sis_cred : str = Field(min_length=0, max_length=20),   
    cuenta_ahorro_AFP_cuenta2 : str = Field(min_length=0, max_length=150),
    codigo_direccion_trabajo: str = Field(min_length=0, max_length=20)  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo_previred" : "001",
                    "nombre"  : "AFP Prueba",
                   "cotizacion" : 0,
                    "cuenta_AFP" : "0001" ,
                    "sis" : 0,
                    "cuenta_sis_cred" : "",   
                    "cuenta_ahorro_AFP_cuenta2" : "",
                   "codigo_direccion_trabajo": ""  
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
from models.afp import AFP as AFPModel
from models.historico_afp import HistoricoAFP as HistoricoAFPModel


# importamos el schema de datos
from schemas.afp import AFP as AFPSchema


# esto representa los metodos implementados en la tabla
class AFPController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico de AFPs
    #@param AFP: Modelo del registro de AFPs
    #@param observavacion: Observación sobre el historico
    def create_historico_AFPs (self, AFP: AFPModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            '''
            `id`  bigint auto_increment not null,
            `afp_id`  bigint not null,
            `codigo_previred` varchar(50) NULL,
            `nombre` varchar(100) NULL,
            `cotizacion` numeric(18,4) NULL,
            `cuenta_AFP` varchar(150)  NULL,
            `sis` numeric(18,4) NULL,
            `cuenta_sis_cred` varchar(20) NULL,
            `cuenta_ahorro_AFP_cuenta2` varchar(150) NULL,
            `codigo_direccion_trabajo` varchar(10),
            `created` DATETIME NOT NULL COMMENT 'fecha en que fue creado el parametro',
            `updated` DATETIME NOT NULL COMMENT 'fecha en que fue actualizado el parametro',
            `creator_user` BIGINT NOT NULL COMMENT 'usuario que creó el parametro',
            `updater_user` BIGINT NOT NULL COMMENT 'usuario que actualizó el parametro', 
            `fecha_registro` DATETIME NOT NULL COMMENT 'fecha en que fue creado el registro historico',
            `observaciones` DATETIME NOT NULL COMMENT 'observaciones del historico',
            '''            
            newHistoricoAFP= HistoricoAFPModel(
                afp_id = AFP.id,
                codigo_previred = AFP.codigo_previred,
                nombre = AFP.nombre,
                cotizacion=AFP.cotizacion,
                cuenta_AFP=AFP.cuenta_AFP,
                sis=AFP.sis,
                cuenta_sis_cred=AFP.cuenta_sis_cred,
                cuenta_ahorro_AFP_cuenta2=AFP.cuenta_ahorro_AFP_cuenta2,
                codigo_direccion_trabajo=AFP.codigo_direccion_trabajo,
                created = AFP.created,
                updated = AFP.updated,
                creator_user= AFP.creator_user,
                updater_user = AFP.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricoAFP)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del AFP 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params AFP: esquema de los datos AFP que se desea insertar       
    def create_AFP(self, AFP:AFPSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreAFP=AFP.nombre.upper().strip()
        codigo_previred=AFP.codigo_previred.upper().strip()


        # contamos si existe un AFP con el mismo nombre
        nRecordNombre = self.db.query(AFPModel).filter(AFPModel.nombre == nombreAFP).count()  

        # contamos si existe un AFP con el mismo código 
        nRecordCodigo = self.db.query(AFPModel).filter(AFPModel.codigo_previred == codigo_previred).count()  

        if (nRecordNombre > 0):
            # buscamos el AFP con el nombre y lo devolvemos
            AFPExists=self.db.query(AFPModel).filter(AFPModel.nombre == nombreAFP).first() 

            # devolvemos el AFP que ya existe
            return ({"result":"-1","estado":"Existe un AFP con ese nombre","data":AFPExists})
        elif (nRecordCodigo>0):
            # buscamos el bnco ccon el mismo codigo
            AFPExists=self.db.query(AFPModel).filter(AFPModel.codigo_previred == codigo_previred).first() 

            # devolvemos el AFP que ya existe
            return ({"result":"-2","estado":"Existe un AFP con ese codigo","data":AFPExists})            
        else:    
            #creamos el nuevo registro de AFP
            try:
                newAFP=AFPModel(
                    codigo_previred=((AFP.codigo_previred).upper()).strip(),
                    nombre=((AFP.nombre).upper()).strip(),
                    cotizacion=AFP.cotizacion,
                    cuenta_AFP=AFP.cuenta_AFP,
                    sis=AFP.sis,
                    cuenta_sis_cred=AFP.cuenta_sis_cred,
                    cuenta_ahorro_AFP_cuenta2=AFP.cuenta_ahorro_AFP_cuenta2,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newAFP)
                self.db.commit()

                #creamos el registro historico de bancarios del usuario
                self.create_historico_AFPs(newAFP,"Se creó un AFP en el sistema")
                data={
                    "id":newAFP.id,
                    "codigo_previred": newAFP.codigo_previred,
                    "nombre": newAFP.nombre,
                    "cotizacion":newAFP.cotizacion,
                    "cuenta_AFP":newAFP.cuenta_AFP,
                    "sis":newAFP.sis,
                    "cuenta_sis_cred":newAFP.cuenta_sis_cred,
                    "cuenta_ahorro_AFP_cuenta2":newAFP.cuenta_ahorro_AFP_cuenta2,
                    "codigo_direccion_trabajo":newAFP.codigo_direccion_trabajo,
                    "created": newAFP.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newAFP.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newAFP.creator_user,
                    "updater_user":newAFP.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de un AFP por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_AFP(self,id:int):

        # buscamos los datos bancarios
        nRecord = self.db.query(AFPModel).filter(AFPModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de este AFP
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de la institucion AFP
            try:
                AFPExits = self.db.query(AFPModel).filter(AFPModel.id == id).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos del AFP","data":AFPExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los AFPs
    # @params cadena: cadena que se buscara en la tabla AFP comparando con el campo nombre y codigo      
    def search_AFP(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(AFPModel).filter(AFPModel.nombre.like(findingT) | AFPModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(AFPModel).filter(AFPModel.nombre.like(findingT) | AFPModel.nombre.like(findingT))
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
            
 
    #metodo para actualizar los datos de un AFP por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params AFP: esquema de los datos de AFP  
    # @params id: Id del AFP que será actualizado
    def update_AFP(self, AFP:AFPSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este AFP existe
        nRecord = self.db.query(AFPModel).filter(AFPModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del AFP
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                AFPExists = self.db.query(AFPModel).filter(AFPModel.id == id).first()             

                #creamos el registro historico de de la actualizacio AFP
                self.create_historico_AFPs(AFPExists ,"Actualización de la data del AFP")

                #registramnos los cambios en la tabla de de instituciones AFP
                AFPExists.codigo_previred = AFP.codigo_previred,
                AFPExists.nombre = ((AFP.nombre).upper()).strip(),
                AFPExists.cotizacion=AFP.cotizacion,
                AFPExists.cuenta_AFP=AFP.cuenta_AFP,
                AFPExists.sis=AFP.sis,
                AFPExists.cuenta_sis_cred=AFP.cuenta_sis_cred,
                AFPExists.cuenta_ahorro_AFP_cuenta2=AFP.cuenta_ahorro_AFP_cuenta2,
                AFPExists.codigo_direccion_trabajo=AFP.codigo_direccion_trabajo,
                AFPExists.updated = ahora,
                AFPExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

               
                data={
                    "id":AFPExists.id,
                    "codigo_previred":AFPExists.codigo_previred,
                    "nombre":AFPExists.nombre,
                    "cotizacion":AFPExists.cotizacion,
                    "cuenta_AFP":AFPExists.cuenta_AFP,  
                    "sis":AFPExists.sis,   
                    "cuenta_sis_cred":AFPExists.cuenta_sis_cred,
                    "cuenta_ahorro_AFP_cuenta2":AFPExists.cuenta_ahorro_AFP_cuenta2,
                    "codigo_direccion_trabajo":AFPExists.codigo_direccion_trabajo,
                    "created":AFPExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":AFPExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":AFPExists.creator_user,
                    "updater_user":AFPExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó los datos de la Institucion AFP","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todos los AFPs
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_AFP(self, page, records):
        consulta = self.db.query(AFPModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos de un AFP
    # @params id: Id del AFP que se esta consultando
    def list_history_AFPs(self, page:int, records: int, id:int):

        # buscamos si exite el AFP
        nRecord = self.db.query(HistoricoAFPModel).filter(HistoricoAFPModel.afp_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del AFP
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del AFP
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoAFPModel).filter(HistoricoAFPModel.afp_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistoryAFPs=consulta.all()
               
                # se actualizó el registro devolvemoslos registros encontrados
                return ({"result":"1","estado":"Se consiguieron los datos historicos del AFP ","data": listHistoryAFPs})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     