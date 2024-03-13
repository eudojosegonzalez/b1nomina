'''
Este archivo contiene las funciones básicas del CRUD de sociedades en el sistema
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
	id	bigint(20) AI PK
	rut	varchar(100)
	nombre	varchar(200)
	direccion	text
	region_id	bigint(20)
	comuna_id	bigint(20)
	ciudad	varchar(250)
	icono	varchar(250)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    rut : str = Field(min_length=3, max_length=100),
    nombre : str = Field(min_length=3, max_length=250),
    direccion : str = Field(min_length=3, max_length=500),
    region_id : int = Field(ge=1, le=1000),
    comuna_id : int = Field(ge=1, le=1000),
    ciudad : str = Field(min_length=3, max_length=250),
    icono : str = Field(min_length=3, max_length=250),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "rut": "RutDemo",
                    "nombre":"Demo",
                    "direccion": "Direccion Demo",
                    "region_id": 1,
                    "comuna_id": 1,
                    "ciudad":"Demo ciudad",
                    'icono':''
                }
            ]
        }
    } 
'''   
import random

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime


# importamos el modelo de la base de datos
from models.sociedades import Sociedad as SociedadModel
from models.historico_sociedades import HistoricoSociedad as HistoricoSociedadModel
from models.sede import Sede as SedeModel
from models.user import Usuario as UsuarioModel
from models.departamentos import Departamentos as DepartamentosModel
from models.grupos_empleados import GruposEmpleado as GruposEmpleadoModel
from models.categorias_configuracion import CategoriasConfiguracion as CategoriasConfiguracionModel


#importamos el esquema de datos de Sociedades
from schemas.sociedades import Sociedades as SocidadeSchema



# esto representa los metodos implementados en la tabla
class sociedadesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las sociedades
    #@param sociedad: Modelo del registro de Sociedades
    #@param observavacion: Observación sobre el historico
    def create_historico_sociedad (self, sociedad: SociedadModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoSociedadModel(
                rut=sociedad.rut,
                sociedad_id=sociedad.id,
                nombre=sociedad.nombre,
                direccion=sociedad.direccion,
                region_id=sociedad.region_id,
                comuna_id=sociedad.comuna_id,
                ciudad=sociedad.ciudad,
                icono=sociedad.icono,
                created=sociedad.created,
                updated=sociedad.updated,
                creator_user=sociedad.creator_user,
                updater_user=sociedad.updater_user,
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
    
    
    #metodo para insertar  los datos de la sociedad
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  sociedad que se desea insertar       
    def create_sociedad(self, sociedad:SocidadeSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreSociedad=sociedad.nombre.upper().strip()
        rutSociedad=sociedad.rut.upper().strip()


        # contamos si existe una sociedad con el mismo nombre
        nRecordNombre = self.db.query(SociedadModel).filter(SociedadModel.nombre == nombreSociedad).count()  

        # contamos si existe una sociedad con el mismo rut
        nRecordRut = self.db.query(SociedadModel).filter(SociedadModel.rut == rutSociedad).count()         


        if (nRecordNombre > 0):
            # buscamos la sociedad con el nombre y lo devolvemos
            sociedadExists=self.db.query(SociedadModel).filter(SociedadModel.nombre == nombreSociedad).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sociedad con ese nombre","data":sociedadExists})
        elif (nRecordRut > 0):
            # buscamos la sociedad con el nombre y lo devolvemos
            sociedadExists=self.db.query(SociedadModel).filter(SociedadModel.rut == rutSociedad).first() 

            # devolvemos la sociedad que ya existe
            return ({"result":"-1","estado":"Existe una sociedad con ese rut","data":sociedadExists})            
        else:    
            #creamos el nuevo registro de banco
            try:
                newSociedad=SociedadModel(
                    nombre=((sociedad.nombre).upper()).strip(),
                    rut=((sociedad.rut).upper()).strip(),
                    region_id=sociedad.region_id,
                    comuna_id=sociedad.comuna_id,
                    direccion=((sociedad.direccion).upper()).strip(),
                    ciudad=((sociedad.ciudad).upper()).strip(),
                    icono=sociedad.icono,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newSociedad)
                self.db.commit()

                #creamos el registro historico de sede
                self.create_historico_sociedad(newSociedad,"Se creó una sociedad en el sistema")
  
                data={
                    "id":newSociedad.id,
                    "rut":newSociedad.rut,
                    "nombre": newSociedad.nombre,
                    "region_id":newSociedad.region_id,
                    "comuna_id":newSociedad.comuna_id,
                    "ciudad":newSociedad.ciudad,
                    "direccion":newSociedad.direccion,
                    "icono":newSociedad.icono,
                    "created": newSociedad.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newSociedad.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newSociedad.creator_user,
                    "updater_user":newSociedad.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una sociedad por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_sociedad(self,id:int):

        # buscamos si esta sociedad existe
        nRecord = self.db.query(SociedadModel).filter(SociedadModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta sociedad
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de la sociedad
            try:
                sociedadExits = self.db.query(SociedadModel).filter(SociedadModel.id == id).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de la sociedad","data":sociedadExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en las sociedades
    # @params cadena: cadena que se buscara en la tabla sociedades comparando con el campo nombre 
    def search_sociedades(self,finding ,page, records):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(SociedadModel).filter(SociedadModel.nombre.like(findingT) | SociedadModel.rut.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(SociedadModel).filter(SociedadModel.nombre.like(findingT) | SociedadModel.rut.like(findingT))
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
            
 
    #metodo para actualizar los datos de una sociedad por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params sociedad: esquema de los datos de la sociedad 
    # @params id: Id de la sociedad que será actualizado
    def update_sociedad(self, sociedad:SocidadeSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este sociedad existe
        nRecord = self.db.query(SociedadModel).filter(SociedadModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos de la sociedad
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                sociedadExists = self.db.query(SociedadModel).filter(SociedadModel.id == id).first()             

                #creamos el registro historicos ociedades 
                self.create_historico_sociedad(sociedadExists ,"Actualización de la data de la sociedad")

                #registramnos los cambios en la tabla de sociedades
                sociedadExists.nombre=((sociedad.nombre).upper()).strip(),
                sociedadExists.rut=((sociedad.rut).upper()).strip(),
                sociedadExists.region_id=sociedad.region_id,
                sociedadExists.comuna_id=sociedad.comuna_id,
                sociedadExists.direccion=((sociedad.direccion).upper()).strip(),
                sociedadExists.ciudad=((sociedad.ciudad).upper()).strip(),
                sociedadExists.icono=sociedad.icono,
                sociedadExists.updated=ahora,
                sociedadExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":sociedadExists.id,
                    "rut":sociedadExists.rut,
                    "nombre":sociedadExists.nombre,
                    "region_id":sociedadExists.region_id,
                    "comuna_id":sociedadExists.comuna_id,
                    "direccion":sociedadExists.direccion,
                    "ciudad":sociedadExists.ciudad,
                    "icono":sociedadExists.icono,
                    "created":sociedadExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":sociedadExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":sociedadExists.creator_user,
                    "updater_user":sociedadExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de de la sociedad","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para consultar todas las sociedades
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedades(self, page, records):
        consulta = self.db.query(SociedadModel)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)
    
    # metodo para consultar todas las sedes por sociedades
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_sedes(self, page, records,idSociedad):
        consulta = self.db.query(SedeModel).filter(SedeModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)
    
    # metodo para consultar todas los grupos de unaa sociedad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_grupos_empleados(self, idSociedad):
        consulta = self.db.query(GruposEmpleadoModel).filter(GruposEmpleadoModel.sociedad_id==idSociedad)
        result=consulta.all()
        return (result)    
    
    # metodo para consultar todas las categorias de configiracion de una sociedad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_categorias_configuracion(self, idSociedad):
        result = self.db.query(CategoriasConfiguracionModel).filter(CategoriasConfiguracionModel.sociedad_id==idSociedad).order_by(CategoriasConfiguracionModel.id).all
        return (result)   

    # metodo para consultar todas los departamentos por Id de socidad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_departamentos(self, page, records,idSociedad):
        consulta = self.db.query(DepartamentosModel).filter(DepartamentosModel.sociedad_id==idSociedad)
        consulta = consulta.limit(records)
        consulta = consulta.offset(records * (page - 1))
        result=consulta.all()
        return (result)    


    # metodo para consultar todas los empleados por Id de socidad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_empleados(self, idSociedad):
        if (idSociedad == 1):
            consulta = self.db.query(UsuarioModel).filter(UsuarioModel.id < 150)
        elif (idSociedad == 2):
            consulta = self.db.query(UsuarioModel).filter(UsuarioModel.id >= 150)    
        else:
            consulta = self.db.query(UsuarioModel).filter(UsuarioModel.id >= 1500) 


        result=consulta.all()
        '''
        id = Column(BIGINT, primary_key=True, autoincrement=True)
        rut = Column(VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
        rut_provisorio  = Column(VARCHAR(100), nullable=True) #VARCHAR(100) NULL,
        nombres = Column (VARCHAR(100), nullable=False) #VARCHAR(100) NOT NULL,
        apellido_paterno  = Column (VARCHAR(100), nullable=False) #paterno VARCHAR(100) NOT NULL,
        apellido_materno = Column (VARCHAR(100),nullable=True )  #VARCHAR(100) NULL,
        fecha_nacimiento = Column(DATE, nullable=False) #DATE NOT NULL,
        sexo_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,
        estado_civil_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL,    
        nacionalidad_id = Column(BIGINT, nullable=False) #BIGINT NOT NULL, 
        username = Column(VARCHAR(250), nullable=False) #varchar(250) NOT NULL,    
        password = Column(VARCHAR(250), nullable=False) #NOT NULL,  
        activo = Column(Boolean, nullable=False) #boolean NOT NULL comment 'campo para activar o no al usuario 0 Inactivo 1 Activo',           
        created = Column (DateTime, nullable=False) #datetime NOT NULL,    
        updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
        creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
        updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,         
        '''
        data = [{
                "id": row.id,
                "nombres": row.nombres,
                "apellido_paterno": row.apellido_paterno,
                "apellido_materno": row.apellido_materno,
                "activo": row.activo,
                "cargo": "Cargo",
                "sueldo":str( random.randint(4500,  10000)),                
                "rut": row.rut
            } for row in result]

        return (data)   

    # metodo para listar los datos historicos  de una sociedad
    # @params id: Id de la sociedad que se esta consultando
    def list_history_sociedades(self, page:int, records: int, id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricoSociedadModel).filter(HistoricoSociedadModel.sociedad_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sociedad
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos de la sociedad
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoSociedadModel).filter(HistoricoSociedadModel.sociedad_id == id)
                consulta = consulta.limit(records)
                consulta = consulta.offset(records * (page - 1))
                listHistorySociedad=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la sociedad ","data": listHistorySociedad})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     


    # esta funcion permite contar los empleados, contratados e inactivos
    def get_employee_summary(self, idSociedad):
        nRecordUserActivos=300

        nRecordUserInactivos=0

        nRecordUserContratados=0

        data={
            "empleados" : str(nRecordUserActivos),
            "contratacion" : str(nRecordUserContratados), 
            "inactivos" : str(nRecordUserInactivos)
        }

        return ({"result":"1","estado":"Datos encontrados","data":data})  