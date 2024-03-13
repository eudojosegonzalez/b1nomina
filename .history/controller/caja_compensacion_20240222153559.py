'''
Este archivo contiene las funciones básicas del CRUD de TiposPrestamoss en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="TiposPrestamos"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("tiposPrestamos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
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
                    "nombre":"TiposPrestamos Demo",
                    "direccion": "Direccion TiposPrestamos Demo",
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
from models.tipos_prestamos import TiposPrestamos as TiposPrestamosModel
from models.historico_tipos_prestamos import HistoricoTiposPrestamos as HistoricoTiposPrestamosModel

#importamos el esquema de datos de Sociedades
from schemas.tipos_prestamos import TiposPrestamos as TiposPrestamosSchema



# esto representa los metodos implementados en la tabla
class TiposPrestamosController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las TiposPrestamoss
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_tipos_prestamos(self, tiposPrestamos: TiposPrestamosModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newTiposPrestamos= HistoricoTiposPrestamosModel(
                tipo_prestamo_id=tiposPrestamos.id,
                sociedad_id=tiposPrestamos.sociedad_id,
                descripcion=tiposPrestamos.descripcion,
                cuenta=tiposPrestamos.cuenta,
                CCAF=tiposPrestamos.CCAF,
                caja_compensacion_id=tiposPrestamos.caja_compensacion_id,
                created=tiposPrestamos.created,
                updated=tiposPrestamos.updated,
                creator_user=tiposPrestamos.creator_user,
                updater_user=tiposPrestamos.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newTiposPrestamos)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la TiposPrestamos
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  TiposPrestamos  que se desea insertar       
    def create_tipos_prestamos(self, tiposPrestamos:TiposPrestamosSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        descripcionTiposPrestamos=tiposPrestamos.descripcion.upper().strip()

        # contamos si existe una TiposPrestamos con el mismo nombre
        nRecordNombre = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.descripcion == descripcionTiposPrestamos).count()  


        if (nRecordNombre > 0):
            # buscamos la TiposPrestamos con el nombre y lo devolvemos
            TiposPrestamosExists=self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.descripcion == descripcionTiposPrestamos).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe un Tipo de Prestamos con ese nombre","data":TiposPrestamosExists})          
        else:    
          
            #creamos el nuevo registro de TiposPrestamoss
            try:
                newTiposPrestamos=TiposPrestamosModel(
                    sociedad_id=tiposPrestamos.sociedad_id,
                    descripcion=tiposPrestamos.descripcion,
                    cuenta=tiposPrestamos.cuenta,
                    CCAF=tiposPrestamos.CCAF,
                    caja_compensacion_id=tiposPrestamos.caja_compensacion_id,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newTiposPrestamos)
                self.db.commit()

                #creamos el registro historico de TiposPrestamoss
                self.create_historico_tipos_prestamos(newTiposPrestamos,"Se creó un tipo de prestamo en el sistema")
  
                data={
                    "id": newTiposPrestamos.id,
                    "sociedad_id":newTiposPrestamos.sociedad_id,
                    "descripcion":newTiposPrestamos.descripcion,
                    "cuenta":newTiposPrestamos.cuenta,
                    "CCAF":newTiposPrestamos.CCAF,
                    "caja_compensacion_id":newTiposPrestamos.caja_compensacion_id,
                    "created": newTiposPrestamos.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newTiposPrestamos.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newTiposPrestamos.creator_user,
                    "updater_user":newTiposPrestamos.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una TiposPrestamos
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_tipos_prestamos(self,id:int):

        # buscamos si este existe esta TiposPrestamos
        nRecord = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta TiposPrestamos
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta TiposPrestamos
            try:
                TiposPrestamosExits = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.id == id).first()                  
                # devolvemos los datos de la TiposPrestamos
                return ({"result":"1","estado":"Se consiguieron los datos del tipo de prestamo","data":TiposPrestamosExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las TiposPrestamoss
    # @params cadena: cadena que se buscara en la tabla TiposPrestamoss comparando con el campo nombre 
    def search_tipos_prestamos(self,finding ):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.descripcion.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.descripcion.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de una TiposPrestamos por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la TiposPrestamos
    # @params id: Id de la TiposPrestamos que será actualizado
    def update_tipos_prestamos(self, tiposPrestamos:TiposPrestamosSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la TiposPrestamos
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                TiposPrestamosExists = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.id == id).first()             

                #creamos el registro historico de TiposPrestamos
                self.create_historico_tipos_prestamos(TiposPrestamosExists ,"Actualización de la data de los Tipos de Prestamos")

                #registramnos los cambios en la tabla de TiposPrestamoss
                TiposPrestamosExists.sociedad_id=tiposPrestamos.sociedad_id,
                TiposPrestamosExists.descripcion=tiposPrestamos.descripcion,
                TiposPrestamosExists.cuenta=tiposPrestamos.cuenta,
                TiposPrestamosExists.CCAF=tiposPrestamos.CCAF,
                TiposPrestamosExists.caja_compensacion_id=tiposPrestamos.caja_compensacion_id,
                TiposPrestamosExists.updated=ahora,
                TiposPrestamosExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":TiposPrestamosExists.id,
                    "sociedad_id":TiposPrestamosExists.sociedad_id,
                    "descripcion":TiposPrestamosExists.descripcion,
                    "cuenta":TiposPrestamosExists.cuenta,
                    "CCAF":TiposPrestamosExists.CCAF,
                    "caja_compensacion_id":TiposPrestamosExists.caja_compensacion_id,
                    "created":TiposPrestamosExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":TiposPrestamosExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":TiposPrestamosExists.creator_user,
                    "updater_user":TiposPrestamosExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la TiposPrestamos","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las TiposPrestamoss
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_tipos_prestamos(self):
        consulta = self.db.query(TiposPrestamosModel)
        result=consulta.all()
        return (result)


    # metodo para consultar todas las TiposPrestamoss
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_tipos_prestamos_sociedad(self,idSociedad):
        consulta = self.db.query(TiposPrestamosModel).filter(TiposPrestamosModel.sociedad_id==idSociedad)
        result=consulta.all()
        return (result)


    # metodo para listar los datos historicos  de una TiposPrestamos
    # @params id: Id de la sociedad que se esta consultando
    def list_history_tipos_prestamos(self, id:int):

        # buscamos si exite la TiposPrestamos
        nRecord = self.db.query(HistoricoTiposPrestamosModel).filter(HistoricoTiposPrestamosModel.tipo_prestamo_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la TiposPrestamos
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoTiposPrestamosModel).filter(HistoricoTiposPrestamosModel.tipo_prestamo_id == id)
                listHistoryTiposPrestamos=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la TiposPrestamos ","data": listHistoryTiposPrestamos})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     