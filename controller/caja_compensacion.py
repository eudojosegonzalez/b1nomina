'''
Este archivo contiene las funciones básicas del CRUD de Cajas de Compensacion en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="CajasCompensacion"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(VARCHAR(200), nullable= False)
    codigo_externo= Column(VARCHAR(50), nullable= False)
    cuenta_contable = Column(VARCHAR(10), nullable= False)
    codigo_direccion_trabajo = Column(VARCHAR(50), nullable= False)    
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    nombre : str = Field(min_length=3, max_length=200)
    codigo_externo : str = Field(min_length=3, max_length=50)
    cuenta_contable : str = Field(min_length=3, max_length=50)
    codigo_direccion_trabajo : str = Field(min_length=0, max_length=10)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre":"Los Andes",
                    "codigo_externo":"01",
                    "cuenta_contable":"21050003",
                    "codigo:direccion":"1",
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
from models.cajas_compensacion import CajasCompensacion as CajasCompensacionModel
from models.historico_cajas_compensacion import HistricoCajasCompensacion as HistoricoCajasCompensacionModel

#importamos el esquema de datos de Sociedades
from schemas.cajas_compensacion import CajasCompensacion as CajasCompensacionSchema


# esto representa los metodos implementados en la tabla
class CajasCompensacionController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las cajaCompensacions
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_cajas_compensacion(self, cajaCompensacion:CajasCompensacionModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newCajaCompensacion= HistoricoCajasCompensacionModel(
                caja_compensacion_id=cajaCompensacion.id,
                nombre=cajaCompensacion.nombre,
                codigo_externo=cajaCompensacion.codigo_externo,
                cuenta_contable=cajaCompensacion.cuenta_contable,
                codigo_direccion_trabajo=cajaCompensacion.codigo_direccion_trabajo,
                created=cajaCompensacion.created,
                updated=cajaCompensacion.updated,
                creator_user=cajaCompensacion.creator_user,
                updater_user=cajaCompensacion.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newCajaCompensacion)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la cajaCompensacion
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  cajaCompensacion  que se desea insertar       
    def create_cajas_compensacion(self, cajaCompensacion:CajasCompensacionSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreCajaCompensacion=cajaCompensacion.nombre.upper().strip()

        # contamos si existe una cajaCompensacion con el mismo nombre
        nRecordNombre = self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.nombre == nombreCajaCompensacion).count()  


        if (nRecordNombre > 0):
            # buscamos la cajaCompensacion con el nombre y lo devolvemos
            cajaCompensacionExists=self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.nombre == nombreCajaCompensacion).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una Caja de Compensacion con ese nombre","data":cajaCompensacionExists})          
        else:    
          
            #creamos el nuevo registro de cajaCompensacions
            try:
                newCajaCompensacion=CajasCompensacionModel(
                    nombre=cajaCompensacion.nombre.upper().strip(),
                    codigo_externo=cajaCompensacion.codigo_externo,
                    cuenta_contable=cajaCompensacion.cuenta_contable,
                    codigo_direccion_trabajo=cajaCompensacion.codigo_direccion_trabajo,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newCajaCompensacion)
                self.db.commit()

                #creamos el registro historico de cajaCompensacions
                self.create_historico_cajas_compensacion(newCajaCompensacion,"Se creó una Caja de Compensacion en el sistema")
  
                data={
                    "id": newCajaCompensacion.id,
                    "nombre":newCajaCompensacion.nombre,
                    "codigo_externo":newCajaCompensacion.codigo_externo,
                    "codigo_direccion_trabajo":newCajaCompensacion.codigo_direccion_trabajo,
                    "created": newCajaCompensacion.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newCajaCompensacion.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newCajaCompensacion.creator_user,
                    "updater_user":newCajaCompensacion.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una cajaCompensacion
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_cajas_compensacion(self,id:int):

        # buscamos si este existe esta cajaCompensacion
        nRecord = self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta cajaCompensacion
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta cajaCompensacion
            try:
                cajaCompensacionExits = self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.id == id).first()                  
                # devolvemos los datos de la cajaCompensacion
                return ({"result":"1","estado":"Se consiguieron los datos del tipo de prestamo","data":cajaCompensacionExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las cajaCompensacions
    # @params cadena: cadena que se buscara en la tabla cajaCompensacions comparando con el campo nombre 
    def search_cajas_compensacion(self,finding ):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.nombre.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de una cajaCompensacion por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la cajaCompensacion
    # @params id: Id de la cajaCompensacion que será actualizado
    def update_cajas_compensacion(self, cajaCompensacion:CajasCompensacionSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la cajaCompensacion
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                cajaCompensacionExists = self.db.query(CajasCompensacionModel).filter(CajasCompensacionModel.id == id).first()             

                #creamos el registro historico de Caja Compensacion
                self.create_historico_cajas_compensacion(cajaCompensacionExists ,"Actualización de la data de los Tipos de Prestamos")

                #registramnos los cambios en la tabla de Caja Compensacion
                cajaCompensacionExists.nombre=cajaCompensacion.nombre.upper().strip(),
                cajaCompensacionExists.codigo_externo=cajaCompensacion.codigo_externo,
                cajaCompensacionExists.codigo_direccion_trabajo=cajaCompensacion.codigo_direccion_trabajo
                cajaCompensacionExists.updated=ahora,
                cajaCompensacionExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":cajaCompensacionExists.id,
                    "nombre":cajaCompensacionExists.nombre,
                    "codigo_externo":cajaCompensacionExists.codigo_externo,
                    "codigo_direccion_trabajo":cajaCompensacionExists.codigo_direccion_trabajo,
                    "created":cajaCompensacionExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":cajaCompensacionExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":cajaCompensacionExists.creator_user,
                    "updater_user":cajaCompensacionExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizaron los datos de la Caja Compensacion","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las cajaCompensacions
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_cajas_compensacion(self):
        consulta = self.db.query(CajasCompensacionModel)
        result=consulta.all()
        return (result)



    # metodo para listar los datos historicos  de una cajaCompensacion
    # @params id: Id de la sociedad que se esta consultando
    def list_history_cajas_compensacion(self, id:int):

        # buscamos si exite la cajaCompensacion
        nRecord = self.db.query(HistoricoCajasCompensacionModel).filter(HistoricoCajasCompensacionModel.caja_compensacion_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la cajaCompensacion
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoCajasCompensacionModel).filter(HistoricoCajasCompensacionModel.caja_compensacion_id == id)
                listHistorycajaCompensacion=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la Caja Compensacion ","data": listHistorycajaCompensacion})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     