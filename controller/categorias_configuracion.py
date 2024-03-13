'''
Este archivo contiene las funciones básicas del CRUD de Categorias de Configuraciones
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="CategoriasConfiguracion"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)        
    nombre = Column(VARCHAR(200), nullable=False)
    activo = Column(BOOLEAN, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    nombre : str = Field(min_length=3, max_length=250)
    activo :  bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "nombre":"Configuracion Básica",
                    "direccion": "Direccion categoria_configuracion Demo",
                    "activo": True,
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
from models.categorias_configuracion import CategoriasConfiguracion as CategoriasConfiguracionModel
from models.historico_categorias_configuracion import HistoricoCategoriasConfiguracion as HistoricoCategoriasConfiguracionModel

#importamos el esquema de datos de Sociedades
from schemas.categorias_configuracion import CategoriasConfiguracion as CategoriasConfiguracionSchema


# esto representa los metodos implementados en la tabla
class CategoriasConfiguracionController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las categoria_configuracions
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_categoria_configuracion(self, categoriasConfiguracion: CategoriasConfiguracionModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricocategoriaConfiguracion= HistoricoCategoriasConfiguracionModel(
                categoria_id=categoriasConfiguracion.id,
                sociedad_id=categoriasConfiguracion.sociedad_id,
                nombre=categoriasConfiguracion.nombre,
                activo=categoriasConfiguracion.activo,
                created=categoriasConfiguracion.created,
                updated=categoriasConfiguracion.updated,
                creator_user=categoriasConfiguracion.creator_user,
                updater_user=categoriasConfiguracion.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricocategoriaConfiguracion)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos de la categoria_configuracion
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  categoria_configuracion  que se desea insertar       
    def create_categoria_configuracion(self, categoriaConfiguracion:CategoriasConfiguracionSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombrecategoria_configuracion=categoriaConfiguracion.nombre.upper().strip()

        # contamos si existe una categoria_configuracion con el mismo nombre
        nRecordNombre = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.nombre == nombrecategoria_configuracion).count()  


        if (nRecordNombre > 0):
            # buscamos la categoria_configuracion con el nombre y lo devolvemos
            categoria_configuracionExists=self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.nombre == nombrecategoria_configuracion).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una categoria_configuracion con ese nombre","data":categoria_configuracionExists})          
        else:    
            #creamos el nuevo registro de categoria_configuracions
            try:
                newcategoria_configuracion=CategoriasConfiguracionModel(
                    sociedad_id=categoriaConfiguracion.sociedad_id,
                    nombre=((categoriaConfiguracion.nombre).upper()).strip(),
                    activo=categoriaConfiguracion.activo,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newcategoria_configuracion)
                self.db.commit()

                #creamos el registro historico de categoria_configuracions
                self.create_historico_categoria_configuracion(newcategoria_configuracion,"Se creó una categoria de configuracion en el sistema")
  
                data={
                    "id":newcategoria_configuracion.id,
                    "sociedad_id":newcategoria_configuracion.sociedad_id,
                    "nombre": newcategoria_configuracion.nombre,
                    "activo":newcategoria_configuracion.activo,
                    "created": newcategoria_configuracion.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newcategoria_configuracion.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newcategoria_configuracion.creator_user,
                    "updater_user":newcategoria_configuracion.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una categoria_configuracion
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_categoria_configuracion(self,id:int):

        # buscamos si este existe esta categoria_configuracion
        nRecord = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta categoria_configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de esta categoria_configuracion
            try:
                categoria_configuracionExits = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.id == id).first()                  
                # devolvemos los datos de la categoria_configuracion
                return ({"result":"1","estado":"Se consiguieron los datos de la categoria_configuracion","data":categoria_configuracionExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})  
            
 
    #metodo para actualizar los datos de una categoria_configuracion por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la categoria_configuracion
    # @params id: Id de la categoria_configuracion que será actualizado
    def update_categoria_configuracion(self, categoria_configuracion:CategoriasConfiguracionSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este banco existe
        nRecord = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la categoria_configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                categoria_configuracionExists = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.id == id).first()             

                #creamos el registro historico de categoria_configuracion
                self.create_historico_categoria_configuracion(categoria_configuracionExists ,"Actualización de la data de la categoria_configuracion")

                #registramnos los cambios en la tabla de categoria_configuracions
                categoria_configuracionExists.sociedad_id=categoria_configuracion.sociedad_id,
                categoria_configuracionExists.nombre=((categoria_configuracion.nombre).upper()).strip(),
                categoria_configuracionExists.activo=categoria_configuracion.activo,
                categoria_configuracionExists.updated=ahora,
                categoria_configuracionExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":categoria_configuracionExists.id,
                    "sociedad_id":categoria_configuracionExists.sociedad_id,
                    "nombre":categoria_configuracionExists.nombre,
                    "activo":categoria_configuracionExists.activo,
                    "created":categoria_configuracionExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":categoria_configuracionExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":categoria_configuracionExists.creator_user,
                    "updater_user":categoria_configuracionExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la categoria_configuracion","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las categoria_configuracions
    def list_categorias_configuracion(self):
        result = self.db.query(CategoriasConfiguracionModel).order_by(CategoriasConfiguracionModel.id).all()
        return (result)


    # metodo para consultar todas las categoria_configuracions
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_categorias_configuracion_sociedad(self,idSociedad):
        result = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.sociedad_id==idSociedad).order_by(CategoriasConfiguracionModel.id).all()
        return (result)


    # metodo para listar los datos historicos  de una categoria_configuracion
    # @params id: Id de la sociedad que se esta consultando
    def list_history_categoria_configuracion(self, id:int):

        # buscamos si exite la categoria_configuracion
        nRecord = self.db.query(HistoricoCategoriasConfiguracionModel).filter(HistoricoCategoriasConfiguracionModel.categoria_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la categoria_configuracion
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                listHistorycategoria_configuracion = self.db.query(HistoricoCategoriasConfiguracionModel).filter(HistoricoCategoriasConfiguracionModel.categoria_id == id).all()

               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la categoria de configuracion ","data": listHistorycategoria_configuracion})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     