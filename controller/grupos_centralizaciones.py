'''
Este archivo contiene las funciones básicas del CRUD de Grupos de Centralizaciones
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
    __tablename__="GruposEmpleado"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    es_honorario = Column(INTEGER, nullable=False)
    nombre = Column(VARCHAR(200), nullable=False)
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,



    **********************************************************************
    * Estructura del Schema                                              *
    **********************************************************************
    es_honorario = bool,
    nombre : str = Field(min_length=3, max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "es_honorario": True,
                    "nombre":"Demo"
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
from models.grupos_centralizaciones import GrupoCentralizaciones  as GrupoCentralizacionesModel
from models.historico_grupos_centralizaciones import HistoricoGrupoCentralizaciones as HistoricoGrupoCentralizacionesModel


#importamos el esquema de datos de Grupo de Centralizaciones
from schemas.grupos_centralizaciones import GrupoCentralizaciones as GrupoCentralizacionesSchema



# esto representa los metodos implementados en la tabla
class GrupoCentralizacionesController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    # funcion para crear el registro de historico las Grupo de Centralizaciones
    #@param grupoCentralizaciones: Modelo del registro de Grupo de Centralizaciones
    #@param observavacion: Observación sobre el historico
    def create_historico_grupo_centralizaciones (self, grupoCentralizacion: GrupoCentralizacionesModel, observacion:str):
        # determinamos la fecha/hora actual
        ahora = datetime.datetime.now()

        try:
            #creamos la instancia la nuevo registro del historico
            newHistoricogrupoCentralizaciones= HistoricoGrupoCentralizacionesModel(

                grupo_centralizacion_id=grupoCentralizacion.id,
                sociedad_id=grupoCentralizacion.sociedad_id,
                es_honorario=grupoCentralizacion.es_honorario,
                nombre=grupoCentralizacion.nombre,
                monto_max_prestamo=grupoCentralizacion.monto_max_prestamo,
                cuotas_max_prestamo =grupoCentralizacion.cuotas_max_prestamo,
                porcentaje_tope_cuota_prestamo=grupoCentralizacion.porcentaje_tope_cuota_prestamo,
                monto_max_anticipo=grupoCentralizacion.monto_max_anticipo,
                porcentaje_maximo_anticipo=grupoCentralizacion.porcentaje_maximo_anticipo,
                calcular_porcentaje_segun=grupoCentralizacion.calcular_porcentaje_segun,
                factura_mas_pago =grupoCentralizacion.factura_mas_pago,
                cuenta_factura_proveedor=grupoCentralizacion.cuenta_factura_proveedor,
                cuenta_pago_factura=grupoCentralizacion.cuenta_pago_factura,
                cuenta_remunera_deb=grupoCentralizacion.cuenta_remunera_deb,
                cuenta_AFP_deb=grupoCentralizacion.cuenta_AFP_deb,
                cuenta_salud_deb=grupoCentralizacion.cuenta_salud_deb,
                cuenta_gratificacion_deb =grupoCentralizacion.cuenta_gratificacion_deb,
                cuenta_horas_ext_deb=grupoCentralizacion.cuenta_horas_ext_deb,
                cuenta_seg_AFC_deb=grupoCentralizacion.cuenta_seg_AFC_deb,
                cuenta_mov_deb=grupoCentralizacion.cuenta_mov_deb,
                cuenta_col_deb=grupoCentralizacion.cuenta_col_deb,
                cuenta_otra_asig_deb=grupoCentralizacion.cuenta_otra_asig_deb,
                cuenta_SIS_deb=grupoCentralizacion.cuenta_SIS_deb,
                cuenta_mut_deb=grupoCentralizacion.cuenta_mut_deb,
                cuenta_impuesto_unico_deb=grupoCentralizacion.cuenta_impuesto_unico_deb,
                cuenta_asignacion_fami_deb=grupoCentralizacion.cuenta_asignacion_fami_deb,
                cuenta_Afc_empresa_cred=grupoCentralizacion.cuenta_Afc_empresa_cred,
                cuenta_asignacion_familiar_cred=grupoCentralizacion.cuenta_asignacion_familiar_cred,
                cuenta_impuesto_unico_cred=grupoCentralizacion.cuenta_impuesto_unico_cred,
                cuenta_sueldo_pagar_cred=grupoCentralizacion.cuenta_sueldo_pagar_cred,                  
                created=grupoCentralizacion.created,
                updated=grupoCentralizacion.updated,
                creator_user=grupoCentralizacion.creator_user,
                updater_user=grupoCentralizacion.updater_user,
                fecha_registro = ahora,
                observaciones = observacion
            )

            # confirmamos el registro en el historico
            self.db.add(newHistoricogrupoCentralizaciones)
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})        
    
    
    #metodo para insertar  los datos del Grupo de Centralización
    # @userCreatorId: Id del usuario que está creando el registro
    # @params socieda: esquema de los datos de  grupoCentralizaciones que se desea insertar       
    def create_grupo_centralizaciones(self, grupoCentralizacion:GrupoCentralizacionesSchema, userCreatorId:int ):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()

        nombreGrupoCentralizacion=grupoCentralizacion.nombre.upper().strip()


        # contamos si existe una grupoCentralizaciones con el mismo nombre
        nRecordNombre = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.nombre == nombreGrupoCentralizacion).count()  

        if (nRecordNombre > 0):
            # buscamos la grupoCentralizaciones con el nombre y lo devolvemos
            grupoCEntralizacionExists=self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.nombre == nombreGrupoCentralizacion).first() 

            # devolvemos la grupoCentralizaciones que ya existe
            return ({"result":"-1","estado":"Existe un Grupo de Centralizacion con ese nombre","data":grupoCEntralizacionExists})
        else:    
            #creamos el nuevo registro de banco
            
            try:
                newgrupoCentralizacion=GrupoCentralizacionesModel(
                    sociedad_id=grupoCentralizacion.sociedad_id,
                    es_honorario=grupoCentralizacion.es_honorario,
                    nombre=((grupoCentralizacion.nombre).upper()).strip(),
                    monto_max_prestamo=grupoCentralizacion.monto_max_prestamo,
                    cuotas_max_prestamo =grupoCentralizacion.cuotas_max_prestamo,
                    porcentaje_tope_cuota_prestamo=grupoCentralizacion.porcentaje_tope_cuota_prestamo,
                    monto_max_anticipo=grupoCentralizacion.monto_max_anticipo,
                    porcentaje_maximo_anticipo=grupoCentralizacion.porcentaje_maximo_anticipo,
                    calcular_porcentaje_segun=grupoCentralizacion.calcular_porcentaje_segun,
                    factura_mas_pago =grupoCentralizacion.factura_mas_pago,
                    cuenta_factura_proveedor=grupoCentralizacion.cuenta_factura_proveedor,
                    cuenta_pago_factura=grupoCentralizacion.cuenta_pago_factura,
                    cuenta_remunera_deb=grupoCentralizacion.cuenta_remunera_deb,
                    cuenta_AFP_deb=grupoCentralizacion.cuenta_AFP_deb,
                    cuenta_salud_deb=grupoCentralizacion.cuenta_salud_deb,
                    cuenta_gratificacion_deb =grupoCentralizacion.cuenta_gratificacion_deb,
                    cuenta_horas_ext_deb=grupoCentralizacion.cuenta_horas_ext_deb,
                    cuenta_seg_AFC_deb=grupoCentralizacion.cuenta_seg_AFC_deb,
                    cuenta_mov_deb=grupoCentralizacion.cuenta_mov_deb,
                    cuenta_col_deb=grupoCentralizacion.cuenta_col_deb,
                    cuenta_otra_asig_deb=grupoCentralizacion.cuenta_otra_asig_deb,
                    cuenta_SIS_deb=grupoCentralizacion.cuenta_SIS_deb,
                    cuenta_mut_deb=grupoCentralizacion.cuenta_mut_deb,
                    cuenta_impuesto_unico_deb=grupoCentralizacion.cuenta_impuesto_unico_deb,
                    cuenta_asignacion_fami_deb=grupoCentralizacion.cuenta_asignacion_fami_deb,
                    cuenta_Afc_empresa_cred=grupoCentralizacion.cuenta_Afc_empresa_cred,
                    cuenta_asignacion_familiar_cred=grupoCentralizacion.cuenta_asignacion_familiar_cred,
                    cuenta_impuesto_unico_cred=grupoCentralizacion.cuenta_impuesto_unico_cred,
                    cuenta_sueldo_pagar_cred=grupoCentralizacion.cuenta_sueldo_pagar_cred,                     
                    created=ahora,
                    updated=ahora,
                    creator_user = userCreatorId,
                    updater_user=userCreatorId
                )

                #confirmamos el cambio en la Base de Datos
                self.db.add(newgrupoCentralizacion)
                self.db.commit()

                #creamos el registro historico de sede
                self.create_historico_grupo_centralizaciones(newgrupoCentralizacion,"Se creó un Grupo de Centralización en el sistema")
  
                data={
                    "id":newgrupoCentralizacion.id,
                    "sociedad_id":newgrupoCentralizacion.sociedad_id,
                    "es_honorario":newgrupoCentralizacion.es_honorario,
                    "nombre": newgrupoCentralizacion.nombre,
                    "monto_max_prestamo":newgrupoCentralizacion.monto_max_prestamo,
                    "cuotas_max_prestamo ":newgrupoCentralizacion.cuotas_max_prestamo,
                    "porcentaje_tope_cuota_prestamo":newgrupoCentralizacion.porcentaje_tope_cuota_prestamo,
                    "monto_max_anticipo":newgrupoCentralizacion.monto_max_anticipo,
                    "porcentaje_maximo_anticipo":newgrupoCentralizacion.porcentaje_maximo_anticipo,
                    "calcular_porcentaje_segun":newgrupoCentralizacion.calcular_porcentaje_segun,
                    "factura_mas_pago ":newgrupoCentralizacion.factura_mas_pago,
                    "cuenta_factura_proveedor":newgrupoCentralizacion.cuenta_factura_proveedor,
                    "cuenta_pago_factura":newgrupoCentralizacion.cuenta_pago_factura,
                    "cuenta_remunera_deb":newgrupoCentralizacion.cuenta_remunera_deb,
                    "cuenta_AFP_deb":newgrupoCentralizacion.cuenta_AFP_deb,
                    "cuenta_salud_deb":newgrupoCentralizacion.cuenta_salud_deb,
                    "cuenta_gratificacion_deb ":newgrupoCentralizacion.cuenta_gratificacion_deb,
                    "cuenta_horas_ext_deb":newgrupoCentralizacion.cuenta_horas_ext_deb,
                    "cuenta_seg_AFC_deb":newgrupoCentralizacion.cuenta_seg_AFC_deb,
                    "cuenta_mov_deb":newgrupoCentralizacion.cuenta_mov_deb,
                    "cuenta_col_deb":newgrupoCentralizacion.cuenta_col_deb,
                    "cuenta_otra_asig_deb":newgrupoCentralizacion.cuenta_otra_asig_deb,
                    "cuenta_SIS_deb":newgrupoCentralizacion.cuenta_SIS_deb,
                    "cuenta_mut_deb":newgrupoCentralizacion.cuenta_mut_deb,
                    "cuenta_impuesto_unico_deb":newgrupoCentralizacion.cuenta_impuesto_unico_deb,
                    "cuenta_asignacion_fami_deb":newgrupoCentralizacion.cuenta_asignacion_fami_deb,
                    "cuenta_Afc_empresa_cred":newgrupoCentralizacion.cuenta_Afc_empresa_cred,
                    "cuenta_asignacion_familiar_cred":newgrupoCentralizacion.cuenta_asignacion_familiar_cred,
                    "cuenta_impuesto_unico_cred":newgrupoCentralizacion.cuenta_impuesto_unico_cred,
                    "cuenta_sueldo_pagar_cred":newgrupoCentralizacion.cuenta_sueldo_pagar_cred,                      
                    "created": newgrupoCentralizacion.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":newgrupoCentralizacion.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":newgrupoCentralizacion.creator_user,
                    "updater_user":newgrupoCentralizacion.updater_user
                }

                return ({"result":"1","estado":"creado","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})
    

    #metodo para consultar los datos de una grupoCentralizaciones por Id
    # @userUpdaterId: Id del usuario que está actualizando el registro
    def get_grupo_centralizaciones(self,id:int):

        # buscamos si esta grupoCentralizaciones existe
        nRecord = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.id == id).count()
        
        if (nRecord == 0):
            # no existen datos de esta grupo Empleado
            return ({"result":"-2","estado":"No record found"})
        else:
            # se extraen los datos de la grupo Empleado
            try:
                grupoCentralizacionExits = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.id == id).first()                  
                # devolvemos los datos bancarios
                return ({"result":"1","estado":"Se consiguieron los datos de la Grupo de Centralizacion","data":grupoCentralizacionExits})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)}) 
            

    #metodo para efectuar búsquedas en los Grupos de  Centralizaciones
    # @params cadena: cadena que se buscara en la tabla Grupo de Centralizaciones comparando con el campo nombre 
    def search_grupo_centralizacion(self,finding ):

        findingT="%"+finding+"%"

        try:
            # buscamos si hay resgistros coincidentes
            nRecord=self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.nombre.like(findingT)).count()  

            # hay registros
            if (nRecord >0):
                # ejecutamos la consulta
                consulta = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.nombre.like(findingT))
                result=consulta.all()
                
                # devolvemos los resultados
                return ({"result":"1","estado":"Se encontraron registros coincidentes con los criterios de búsqueda","data":result})
            else:
                # los filtros no arrojaron resultados
                 return ({"result":"-1","estado":"No record found"})            

        except ValueError as e:
                # ocurrio un error y devolvemos el estado
                return( {"result":"-3","error": str(e)})       
            
 
    #metodo para actualizar los datos de una grupo Empleado por Id
    # @params userUpdaterId: Id del usuario que está actualizando el registro
    # @params grupoCentralizaciones: esquema de los datos del Grupo de Centralización 
    # @params id: Id del Grupo de Centralización que será actualizado
    def update_grupo_centralizaciones(self, grupoCentralizacion:GrupoCentralizacionesSchema, userUpdaterId:int, id:int):
        #obtenemos la fecha/hora del servidor
        ahora=datetime.datetime.now()
        
        # buscamos si este grupoCentralizaciones existe
        nRecord = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.id == id).count()
        
        if (nRecord == 0):
            # no se consiguieron los datos del Grupo de Centralización
            return ({"result":"-2","estado":"No record found"})
        else:
            try:
                #extraemos los datos para guardar el histórico
                grupoCentralizacionesExists = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.id == id).first()             

                #creamos el registro historicos de grupo de centralizacion
                self.create_historico_grupo_centralizaciones(grupoCentralizacionesExists ,"Actualización de la data del Grupo de Centralizacion")

                #registramnos los cambios en la tabla de grupo CEntralizaciones
                grupoCentralizacionesExists.sociedad_id=grupoCentralizacion.sociedad_id,
                grupoCentralizacionesExists.es_honorario=grupoCentralizacion.es_honorario,
                grupoCentralizacionesExists.nombre=((grupoCentralizacion.nombre).upper()).strip(),
                grupoCentralizacionesExists.monto_max_prestamo=grupoCentralizacion.monto_max_prestamo,
                grupoCentralizacionesExists.cuotas_max_prestamo =grupoCentralizacion.cuotas_max_prestamo,
                grupoCentralizacionesExists.porcentaje_tope_cuota_prestamo=grupoCentralizacion.porcentaje_tope_cuota_prestamo,
                grupoCentralizacionesExists.monto_max_anticipo=grupoCentralizacion.monto_max_anticipo,
                grupoCentralizacionesExists.porcentaje_maximo_anticipo=grupoCentralizacion.porcentaje_maximo_anticipo,
                grupoCentralizacionesExists.calcular_porcentaje_segun=grupoCentralizacion.calcular_porcentaje_segun,
                grupoCentralizacionesExists.factura_mas_pago =grupoCentralizacion.factura_mas_pago,
                grupoCentralizacionesExists.cuenta_factura_proveedor=grupoCentralizacion.cuenta_factura_proveedor,
                grupoCentralizacionesExists.cuenta_pago_factura=grupoCentralizacion.cuenta_pago_factura,
                grupoCentralizacionesExists.cuenta_remunera_deb=grupoCentralizacion.cuenta_remunera_deb,
                grupoCentralizacionesExists.cuenta_AFP_deb=grupoCentralizacion.cuenta_AFP_deb,
                grupoCentralizacionesExists.cuenta_salud_deb=grupoCentralizacion.cuenta_salud_deb,
                grupoCentralizacionesExists.cuenta_gratificacion_deb =grupoCentralizacion.cuenta_gratificacion_deb,
                grupoCentralizacionesExists.cuenta_horas_ext_deb=grupoCentralizacion.cuenta_horas_ext_deb,
                grupoCentralizacionesExists.cuenta_seg_AFC_deb=grupoCentralizacion.cuenta_seg_AFC_deb,
                grupoCentralizacionesExists.cuenta_mov_deb=grupoCentralizacion.cuenta_mov_deb,
                grupoCentralizacionesExists.cuenta_col_deb=grupoCentralizacion.cuenta_col_deb,
                grupoCentralizacionesExists.cuenta_otra_asig_deb=grupoCentralizacion.cuenta_otra_asig_deb,
                grupoCentralizacionesExists.cuenta_SIS_deb=grupoCentralizacion.cuenta_SIS_deb,
                grupoCentralizacionesExists.cuenta_mut_deb=grupoCentralizacion.cuenta_mut_deb,
                grupoCentralizacionesExists.cuenta_impuesto_unico_deb=grupoCentralizacion.cuenta_impuesto_unico_deb,
                grupoCentralizacionesExists.cuenta_asignacion_fami_deb=grupoCentralizacion.cuenta_asignacion_fami_deb,
                grupoCentralizacionesExists.cuenta_Afc_empresa_cred=grupoCentralizacion.cuenta_Afc_empresa_cred,
                grupoCentralizacionesExists.cuenta_asignacion_familiar_cred=grupoCentralizacion.cuenta_asignacion_familiar_cred,
                grupoCentralizacionesExists.cuenta_impuesto_unico_cred=grupoCentralizacion.cuenta_impuesto_unico_cred,
                grupoCentralizacionesExists.cuenta_sueldo_pagar_cred=grupoCentralizacion.cuenta_sueldo_pagar_cred,                 
                grupoCentralizacionesExists.updated=ahora,
                grupoCentralizacionesExists.updater_user=userUpdaterId               

                #confirmamos los cambios
                self.db.commit()

                data={
                    "id":grupoCentralizacionesExists.id,
                    "sociedad_id":grupoCentralizacionesExists.sociedad_id,
                    "es_honorario":grupoCentralizacionesExists.es_honorario,
                    "nombre": grupoCentralizacionesExists.nombre,
                    "monto_max_prestamo":grupoCentralizacionesExists.monto_max_prestamo,
                    "cuotas_max_prestamo ":grupoCentralizacionesExists.cuotas_max_prestamo,
                    "porcentaje_tope_cuota_prestamo":grupoCentralizacionesExists.porcentaje_tope_cuota_prestamo,
                    "monto_max_anticipo":grupoCentralizacionesExists.monto_max_anticipo,
                    "porcentaje_maximo_anticipo":grupoCentralizacionesExists.porcentaje_maximo_anticipo,
                    "calcular_porcentaje_segun":grupoCentralizacionesExists.calcular_porcentaje_segun,
                    "factura_mas_pago ":grupoCentralizacionesExists.factura_mas_pago,
                    "cuenta_factura_proveedor":grupoCentralizacionesExists.cuenta_factura_proveedor,
                    "cuenta_pago_factura":grupoCentralizacionesExists.cuenta_pago_factura,
                    "cuenta_remunera_deb":grupoCentralizacionesExists.cuenta_remunera_deb,
                    "cuenta_AFP_deb":grupoCentralizacionesExists.cuenta_AFP_deb,
                    "cuenta_salud_deb":grupoCentralizacionesExists.cuenta_salud_deb,
                    "cuenta_gratificacion_deb ":grupoCentralizacionesExists.cuenta_gratificacion_deb,
                    "cuenta_horas_ext_deb":grupoCentralizacionesExists.cuenta_horas_ext_deb,
                    "cuenta_seg_AFC_deb":grupoCentralizacionesExists.cuenta_seg_AFC_deb,
                    "cuenta_mov_deb":grupoCentralizacionesExists.cuenta_mov_deb,
                    "cuenta_col_deb":grupoCentralizacionesExists.cuenta_col_deb,
                    "cuenta_otra_asig_deb":grupoCentralizacionesExists.cuenta_otra_asig_deb,
                    "cuenta_SIS_deb":grupoCentralizacionesExists.cuenta_SIS_deb,
                    "cuenta_mut_deb":grupoCentralizacionesExists.cuenta_mut_deb,
                    "cuenta_impuesto_unico_deb":grupoCentralizacionesExists.cuenta_impuesto_unico_deb,
                    "cuenta_asignacion_fami_deb":grupoCentralizacionesExists.cuenta_asignacion_fami_deb,
                    "cuenta_Afc_empresa_cred":grupoCentralizacionesExists.cuenta_Afc_empresa_cred,
                    "cuenta_asignacion_familiar_cred":grupoCentralizacionesExists.cuenta_asignacion_familiar_cred,
                    "cuenta_impuesto_unico_cred":grupoCentralizacionesExists.cuenta_impuesto_unico_cred,
                    "cuenta_sueldo_pagar_cred":grupoCentralizacionesExists.cuenta_sueldo_pagar_cred,                      
                    "created": grupoCentralizacionesExists.created.strftime("%Y-%m-%d %H:%M:%S"),  
                    "updated":grupoCentralizacionesExists.updated.strftime("%Y-%m-%d %H:%M:%S"),  
                    "creator_user":grupoCentralizacionesExists.creator_user,
                    "updater_user":grupoCentralizacionesExists.updater_user
                }
                # se actualizó el registro devolvemos el registro actualizado
                return ({"result":"1","estado":"Se actualizó el dato de de Grupo de Centralización","data":data})
            except ValueError as e:
                return( {"result":"-3","error": str(e)})                    


    # metodo para listar los datos historicos  de un Grupo Centralizaciones
    # @params id: Id del Grupo de Centralización que se esta consultando
    def list_history_grupo_centralizaciones(self,  id:int):

        # buscamos si exite el banco
        nRecord = self.db.query(HistoricoGrupoCentralizacionesModel).filter(HistoricoGrupoCentralizacionesModel.grupo_centralizacion_id == id).count()
        
        if (nRecord == 0):
            # el no se consiguieron datos historicos del Grupo de Centralización
            return ({"result":"-2","estado":"No record found"})
        else:
            # existen los datos historicos del Grupo de Centralización
            try:
                # ejecutamos la consulta
                consulta = self.db.query(HistoricoGrupoCentralizacionesModel).filter(HistoricoGrupoCentralizacionesModel.grupo_centralizacion_id == id)
                listHistoryGrupoCentralizaciones=consulta.all()
               
                # se actualizó el registro devolvemos el registro encontrado
                return ({"result":"1","estado":"Se consiguieron los datos historicos del Grupo de Centralización ","data": listHistoryGrupoCentralizaciones})
            except ValueError as e:
                # ocurrió un error devolvemos el error
                return( {"result":"-1","error": str(e)})     
            
    
    # metodo para consultar todas los grupos de centralizacion una sociedad
    # @params page: pagina de los datos que se mostrará
    # @params records: cantidad de registros por página
    def list_sociedad_grupos(self,idSociedad):
        consulta = self.db.query(GrupoCentralizacionesModel).filter(GrupoCentralizacionesModel.sociedad_id==idSociedad)
        result=consulta.all()
        return (result)  
  