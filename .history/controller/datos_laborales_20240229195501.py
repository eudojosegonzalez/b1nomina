'''
Este archivo contiene las funciones básicas del CRUD de Datos Laborales en el sistema
Created 2024-02
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="DatosLaborales"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    sede_id = Column (BIGINT, ForeignKey("datosLaborales.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    departamento_id = Column (BIGINT, ForeignKey("Departamentos.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    grupo_id = Column (BIGINT, ForeignKey("GruposEmpleado.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    cargo_id = Column (BIGINT, ForeignKey("Cargo.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    user_id = Column (BIGINT, ForeignKey("Usuario.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)            
    tipo_contrato = Column(INTEGER, nullable=False)
    termino_contrato = Column(INTEGER, nullable=False)
    fecha_inicio =Column(DATE, nullable=False)    
    fecha_fin =Column(DATE, nullable=True)    
    periodo_salario = Column(INTEGER, nullable=False)    
    modalidad = Column(INTEGER, nullable=False)   
    dias_descanso=Column(VARCHAR(50), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    sociedad_id : int = Field(ge=1, le=1000)
    sede_id : int = Field(ge=1, le=1000)
    departamento_id : int = Field(ge=1, le=1000)  
    grupo_id : int = Field(ge=0, le=1000)      
    cargo_id : int = Field(ge=1, le=1000)    
    user_id : int = Field(ge=1, le=10000)    
    tipo_contrato : int = Field(ge=1, le=2)    
    termino_contrato : int = Field(ge=1, le=2) 
    fecha_inicio : date = None
    fecha_fin : date = None
    periodo_salario: int
    modalidad: int    
    dias_descanso: str = Field (min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "sede_id": 1,                    
                    "departamento_id": 1,                    
                    "grupo_id":0,
                    "cargo_id":1,
                    "user_id":1,
                    "tipo_contrato":1,
                    "termino_contrato":1,
                    "fecha_inicio":'2024-01-01',
                     "fecha_fin":'',
                    "periodo_salario":30,
                    "modalidad":0,
                    "dias_descanso":"1"
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
from models.datos_laborales import DatosLaborales as DatosLaboralesModel
from models.historico_datos_laborales import HistoricoDatosLaborales as HistoricoDatosLaboralesModel

#importamos el esquema de datos de Datos Laborales
from schemas.datos_laborales import DatosLaborales as DatosLaboralesSchema



# esto representa los metodos implementados en la tabla
class DatosLaboralesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico los Datos Laborales
    #@param datosLaborales: Modelo del registro de Datos Laborales
    #@param observavacion: Observación sobre el historico
    def create_historico_datos_laborales(self, datosLaborales: DatosLaboralesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricoSociedad= HistoricoDatosLaboralesModel(
                datos_laborales_id=datosLaborales.id,
                sociedad_id=datosLaborales.sociedad_id,
                sede_id=datosLaborales.sede_id,
                departamento_id=datosLaborales.departamento_id,
                grupo_id=datosLaborales.grupo_id,
                cargo_id=datosLaborales.cargo_id,
                user_id=datosLaborales.user_id,
                tipo_contrato=datosLaborales.tipo_contrato,
                termino_contrato=datosLaborales.termino_contrato,
                fecha_inicio=datosLaborales.fecha_inicio,
                fecha_fin=datosLaborales.fecha_fin,
                periodo_salario=datosLaborales.periodo_salario,
                modalidad=datosLaborales.modalidad,
                dias_descanso=datosLaborales.dias_descanso,
                salario_base=datosLaborales.salario_base,
                created=datosLaborales.created,
                updated=datosLaborales.updated,
                creator_user=datosLaborales.creator_user,
                updater_user=datosLaborales.updater_user,
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
    
    
    #metodo para insertar  los datos laborales
    # @userCreatorId: Id del usuario que está creando el registro
    # @params datosLaborales: esquema de los datos laborales  que se desea insertar       
    def create_datos_laborales(self, datosLaborales:DatosLaboralesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        # verificamos que el usuario no tenga datos laborales previos
        nRecordDatosLaborales=  self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == datosLaborales.user_id).count()

        if (nRecordDatosLaborales>0):
            datoLaboralExists = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == datosLaborales.user_id).first()
            return ({"result":"-1","estado":"Este usuario ya tiene datos laborales no puede volver a crearlo","Dato Laboral": datoLaboralExists})     
                
        else:
            #creamos el nuevo registro de Datos Laborales
            try:
                newDatosLaborales=DatosLaboralesModel(
                    sociedad_id=datosLaborales.sociedad_id,
                    sede_id=datosLaborales.sede_id,
                    departamento_id=datosLaborales.departamento_id,                
                    grupo_id=datosLaborales.grupo_id,                
                    cargo_id=datosLaborales.cargo_id,                
                    user_id=datosLaborales.user_id,
                    tipo_contrato=datosLaborales.tipo_contrato,                
                    termino_contrato=datosLaborales.termino_contrato,                
                    fecha_inicio=datosLaborales.fecha_inicio,
                    fecha_fin=datosLaborales.fecha_fin,
                    periodo_salario=datosLaborales.periodo_salario,
                    modalidad=datosLaborales.modalidad,
                    dias_descanso=datosLaborales.dias_descanso,
                    salario_base=datosLaborales.salario_base,
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newDatosLaborales)
                self.db.commit()

                #creamos el registro historico de los datos laborales
                self.create_historico_datos_laborales(newDatosLaborales,"Se creó un Dato Laboral en el sistema")

                data={
                    "id":newDatosLaborales.id,
                    "sociedad_id":newDatosLaborales.sociedad_id,
                    "sede_id":newDatosLaborales.sede_id,
                    "departamento_id":newDatosLaborales.departamento_id,
                    "grupo_id":newDatosLaborales.departamento_id,
                    "cargo_id":newDatosLaborales.cargo_id,
                    "user_id":newDatosLaborales.user_id,
                    "tipo_contrato":newDatosLaborales.tipo_contrato,
                    "termino_contrato":newDatosLaborales.termino_contrato,
                    "fecha_inicio":newDatosLaborales.fecha_inicio,
                    "fecha_fin":newDatosLaborales.fecha_fin,
                    "periodo_salario":newDatosLaborales.periodo_salario,
                    "modalidad":newDatosLaborales.modalidad,
                    "dias_descanso":newDatosLaborales.dias_descanso,
                    "salario_base":newDatosLaborales.salario_base,
                    "created": newDatosLaborales.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newDatosLaborales.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newDatosLaborales.creator_user,
                    "updater_user":newDatosLaborales.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    # metodo para consultar los datos Laborales por ID
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_datos_laborales(self,id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos laborales
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales
            try:
                sedeExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == id).first()                  
                # devolvemos los datos de la sede
                return ({"result":"1","estado":"Se consiguieron los Datos Laborales","data":sedeExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para consultar los datos Laborales por user_id
    def get_datos_laborales_userid(self,userId:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este usuario
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.user_id == userId).first()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los Datos Laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     
            
    # metodo para consultar todas los Datos Laborales
    def list_datos_laborales(self):
        consulta = self.db.query(DatosLaboralesModel)
        result=consulta.all()
        return (result)


    # metodo para consultar todas los Datos Laborales
    def list_datos_laborales_sociedad(self,Id ):
        consulta = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.sociedad_id==Id)
        result=consulta.all()
        return (result)
 
            
                        
    #metodo para consultar los datos Laborales por sede_id
    def list_datos_laborales_sede(self,Id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.sede_id == Id).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este usuario
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este usuario
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.sede_id == Id).all()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los dtos laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})                      
            

            
    #metodo para consultar los datos Laborales por deprtamento_id
    def list_datos_laborales_departamento(self,Id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.departamento_id == Id).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este departamento
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este departamento
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.departamento_id == Id).all()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los dtos laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            
            
    #metodo para consultar los datos Laborales por grupo_id
    def list_datos_laborales_grupo(self,Id:int):

        # buscamos si este existe esta sede
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.grupo_id == Id).count()
        
        if (nRecord == 0):
            # no existen datos laborales de este grupo
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos laborales de este grupo
            try:
                DatosLaboralesExits = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.grupo_id == Id).all()                  
                # devolvemos los datos laborales
                return ({"result":"1","estado":"Se consiguieron los dtos laborales","data":DatosLaboralesExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
                                             
            
 
    #metodo para actualizar los datos laborales por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params datosLaborale: esquema de los datos laborales que se estan actualizando
    # @params id: Id de los datos laborales que será actualizado
    def update_datos_laborales(self, datosLaborales:DatosLaboralesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este dato laboral existe
        nRecord = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos laborales
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                datosLaboralesExists = self.db.query(DatosLaboralesModel).filter(DatosLaboralesModel.id == id).first()             

                #creamos el registro historico de datos laborales
                self.create_historico_datos_laborales(datosLaboralesExists ,"Actualización de la data de la sede")

                #registramnos los cambios en la tabla de datos laborales
                datosLaboralesExists.sociedad_id=datosLaborales.sociedad_id,
                datosLaboralesExists.sede_id=datosLaborales.sede_id,
                datosLaboralesExists.departamento_id=datosLaborales.departamento_id,
                datosLaboralesExists.grupo_id=datosLaborales.grupo_id,
                datosLaboralesExists.cargo_id=datosLaborales.cargo_id,
                datosLaboralesExists.user_id=datosLaborales.user_id,                
                datosLaboralesExists.tipo_contrato=datosLaborales.tipo_contrato, 
                datosLaboralesExists.termino_contrato=datosLaborales.termino_contrato, 
                datosLaboralesExists.fecha_inicio=datosLaborales.fecha_inicio,                 
                datosLaboralesExists.fecha_fin=datosLaborales.fecha_fin, 
                datosLaboralesExists.periodo_salario=datosLaborales.periodo_salario, 
                datosLaboralesExists.modalidad=datosLaborales.modalidad, 
                datosLaboralesExists.dias_descanso=datosLaborales.dias_descanso, 
                datosLaboralesExists.salario_base=datosLaborales.salario_base,
                datosLaboralesExists.updated=ahora,
                datosLaboralesExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":datosLaboralesExists.id,
                    "sociedad_id":datosLaboralesExists.sociedad_id,
                    "sede_id":datosLaboralesExists.sede_id,
                    "departamento_id":datosLaboralesExists.departamento_id,
                    "grupo_id":datosLaboralesExists.grupo_id,                    
                    "cargo_id":datosLaboralesExists.cargo_id,                    
                    "user_id":datosLaboralesExists.user_id,                    
                    "tipo_contrato":datosLaboralesExists.tipo_contrato,
                    "termino_contrato":datosLaboralesExists.termino_contrato,
                    "fecha_inicio":datosLaboralesExists.fecha_inicio,
                    "fecha_fin":datosLaboralesExists.fecha_fin,
                    "periodo_salario":datosLaboralesExists.periodo_salario,
                    "modalidad":datosLaboralesExists.modalidad,
                    "dias_descanso":datosLaboralesExists.dias_descanso,    
                    "salario_base":datosLaboralesExists.salario_base,                
                    "created":datosLaboralesExists.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated":datosLaboralesExists.updated.strftime("%Y-%m-%d %H:%M:%S"),
                    "creator_user":datosLaboralesExists.creator_user,
                    "updater_user":datosLaboralesExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de la sede","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para listar los datos historicos  de una sede
    # @params id: Id de la sociedad que se esta consultando
    def list_history_datos_laborales(self,  id:int):

        # buscamos si exite la sede
        nRecord = self.db.query(HistoricoDatosLaboralesModel).filter(HistoricoDatosLaboralesModel.datos_laborales_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos de la sede
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del banco
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoDatosLaboralesModel).filter(HistoricoDatosLaboralesModel.datos_laborales_id == id)
                listHistoryDatosLaborales=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos de la sede ","data": listHistoryDatosLaborales})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     