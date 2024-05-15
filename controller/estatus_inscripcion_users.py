'''
Este archivo contiene las funciones básicas del CRUD de Estatus Inscripcion Usuario
Created 2024-04
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************
 
'''   
import os
import re
import uuid


from fastapi import File, UploadFile,  Request
from fastapi.staticfiles import StaticFiles


# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate



from sqlalchemy import or_,and_
import  datetime


#Importamos los modeloas necesarios
from models.estatus_inscripcion import EstatusInscripcion as EstatusInscripcionModel
from models.historico_estatus_inscripcion import HistoricoEstatusInscripcion as HistoricoEstatusInscripcionModel

from schemas.estatus_inscripcion import EstatusInscripcion as EstatusInscripcionSchema
from schemas.estatus_inscripcion_laborales import EstatusInscripcionLaboral as EstatusInscripcionLaboralSchema
from schemas.estatus_inscripcion_pago import EstatusInscripcionPago as EstatusInscripcionPagoSchema

# esto representa los metodos implementados en la tabla
class EstatusInscripcionUserController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db


    #rutina para convertir un registro en un elemento tipo diccionario
    # @params estatusInscripcionUsuarios: Modelo de datos 
    def get_data (estatusInscripcionExists:EstatusInscripcionModel):
        data={
            "id":estatusInscripcionExists.id,
            "user_id":estatusInscripcionExists.user_id,
            "rut":estatusInscripcionExists.rut,
            "nombre":estatusInscripcionExists.nombre,
            "apellido":estatusInscripcionExists.apellido,   
            "nacionalidad":estatusInscripcionExists.nacionalidad,
            "sexo":estatusInscripcionExists.sexo,   
            "fecha_nac":estatusInscripcionExists.fecha_nac,
            "estado_civil":estatusInscripcionExists.estado_civil,   
            "region":estatusInscripcionExists.region,   
            "comuna":estatusInscripcionExists.comuna,
            "direccion":estatusInscripcionExists.direccion,   
            "telefono":estatusInscripcionExists.telefono,
            "email":estatusInscripcionExists.email,
            "tipo_contrato":estatusInscripcionExists.tipo_contrato,   
            "termino":estatusInscripcionExists.termino,
            "fecha_contratacion":estatusInscripcionExists.fecha_contratacion,   
            "salario_base":estatusInscripcionExists.salario_base,
            "unidad_sueldo":estatusInscripcionExists.unidad_sueldo,   
            "monto_sueldo":estatusInscripcionExists.monto_sueldo,
            "sociedad":estatusInscripcionExists.sociedad,   
            "sede":estatusInscripcionExists.sede,   
            "departamento":estatusInscripcionExists.departamento,   
            "cargo":estatusInscripcionExists.cargo,
            "grupo":estatusInscripcionExists.grupo,   
            "modalidad":estatusInscripcionExists.modalidad,
            "dias_descanso":estatusInscripcionExists.dias_descanso,
            "nivel_estudio":estatusInscripcionExists.nivel_estudio,
            "medio":estatusInscripcionExists.medio,   
            "banco":estatusInscripcionExists.banco,
            "tipo_cuenta":estatusInscripcionExists.tipo_cuenta,   
            "numero":estatusInscripcionExists.numero,
            "foto":estatusInscripcionExists.foto, 
            "cv":estatusInscripcionExists.cv,
            "contrato":estatusInscripcionExists.contrato,
            "created":estatusInscripcionExists.created,
            "updated": estatusInscripcionExists.updated,
            "creator_user":estatusInscripcionExists.creator_user,
            "updater_user":estatusInscripcionExists.updater_user                    
        }
        return (data)

    # funcion para crear el registro de historico de los archivos del usuario
    # @param estatusInscripcionUsuarios: Modelo del registro de Estatos de Inscrpcion
    # @param observavacion: Observación sobre el historico
    def create_historico_estatus_inscripcion (self, estatusInscripcionUsuarios: EstatusInscripcionModel, observacion:str):
        # determinamos la fecha/hora actual
        paso=1
        ahora = datetime.datetime.now()

        try:
            paso=2
            #creamos la instancia la nuevo registro del historico
            newHistoricoEstatusInscripcion= HistoricoEstatusInscripcionModel(
                estatus_inscripcion_id=estatusInscripcionUsuarios.id,                  
                user_id=estatusInscripcionUsuarios.user_id,     
                rut=estatusInscripcionUsuarios.rut,
                nombre=estatusInscripcionUsuarios.nombre,
                apellido=estatusInscripcionUsuarios.apellido,
                nacionalidad=estatusInscripcionUsuarios.nacionalidad,
                sexo=estatusInscripcionUsuarios.sexo,
                fecha_nac=estatusInscripcionUsuarios.fecha_nac,
                estado_civil=estatusInscripcionUsuarios.estado_civil,

                region=estatusInscripcionUsuarios.region,
                comuna=estatusInscripcionUsuarios.comuna,
                direccion=estatusInscripcionUsuarios.direccion,
                
                telefono=estatusInscripcionUsuarios.telefono,
                email=estatusInscripcionUsuarios.email,  
                
                tipo_contrato=estatusInscripcionUsuarios.tipo_contrato,
                termino=estatusInscripcionUsuarios.termino,   
                fecha_contratacion=estatusInscripcionUsuarios.fecha_contratacion,   
                salario_base=estatusInscripcionUsuarios.salario_base,   
                unidad_sueldo=estatusInscripcionUsuarios.unidad_sueldo,  
                monto_sueldo=estatusInscripcionUsuarios.monto_sueldo,    
                sociedad=estatusInscripcionUsuarios.sociedad,       
                sede=estatusInscripcionUsuarios.sede,   
                departamento=estatusInscripcionUsuarios.departamento,    
                cargo=estatusInscripcionUsuarios.cargo,    
                grupo=estatusInscripcionUsuarios.grupo,  
                modalidad=estatusInscripcionUsuarios.modalidad,  
                dias_descanso=estatusInscripcionUsuarios.dias_descanso,
                nivel_estudio=estatusInscripcionUsuarios.nivel_estudio, 
                
                medio=estatusInscripcionUsuarios.medio,  
                banco=estatusInscripcionUsuarios.banco,  
                tipo_cuenta=estatusInscripcionUsuarios.tipo_cuenta,   
                numero=estatusInscripcionUsuarios.numero,                          
                
                foto=estatusInscripcionUsuarios.foto,   
                cv=estatusInscripcionUsuarios.cv,     
                contrato=estatusInscripcionUsuarios.contrato,                   

                created=estatusInscripcionUsuarios.created,
                updated=estatusInscripcionUsuarios.updated,
                creator_user = estatusInscripcionUsuarios.creator_user,
                updater_user=estatusInscripcionUsuarios.updater_user,
                fecha_registro=ahora,
                observaciones=observacion
            )

            # confirmamos el registro en el historico
            paso=3
            self.db.add(newHistoricoEstatusInscripcion)
            paso=4
            self.db.commit()        

            result=True
            return (result)
        except ValueError as e:
            return( {"result":False,"error": str(e)})  


    # funcion para crear el registro de estatus de inscripcion del usuario
    # @param estatusInscripcion: esquiema de datos que representa el modelo de estatus de inscripcion
    # @param creatorUserId:usuario que efectua la operación
    def create_estatus_inscripcion(self,estatusInscripcion: EstatusInscripcionSchema, creatorUserId):
        paso=1
        ahora=datetime.datetime.now()
        
        paso=2
        userId=estatusInscripcion.user_id

        # verificamos que el registro no exista
        paso=3
        nRecord= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
        
        if (nRecord > 0):
            paso=4
            #existe no puede vorlver a crearlo
            data=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()
            
            return ({"result":"-2","estado":"Ya existe el registro de estatus de inscripcion","data":data})   
        else:
            try:
                paso=5
                newEstatusInscripcion=EstatusInscripcionModel(
                    user_id=estatusInscripcion.user_id,
                    rut=1,
                    nombre=estatusInscripcion.nombre,
                    apellido=estatusInscripcion.apellido,
                    nacionalidad=estatusInscripcion.nacionalidad,
                    sexo=estatusInscripcion.sexo,
                    fecha_nac=estatusInscripcion.fecha_nac,
                    estado_civil=estatusInscripcion.estado_civil,

                    region=estatusInscripcion.region,
                    comuna=estatusInscripcion.comuna,
                    direccion=estatusInscripcion.direccion,
                    
                    telefono=estatusInscripcion.telefono,
                    email=estatusInscripcion.email,  
                    
                    tipo_contrato=estatusInscripcion.tipo_contrato,
                    termino=estatusInscripcion.termino,   
                    fecha_contratacion=estatusInscripcion.fecha_contratacion,   
                    salario_base=estatusInscripcion.salario_base,   
                    unidad_sueldo=estatusInscripcion.unidad_sueldo,  
                    monto_sueldo=estatusInscripcion.monto_sueldo,    
                    sociedad=estatusInscripcion.sociedad,       
                    sede=estatusInscripcion.sede,   
                    departamento=estatusInscripcion.departamento,    
                    cargo=estatusInscripcion.cargo,    
                    grupo=estatusInscripcion.grupo,  
                    modalidad=estatusInscripcion.modalidad,  
                    dias_descanso=estatusInscripcion.dias_descanso,
                    nivel_estudio=estatusInscripcion.nivel_estudio, 
                    
                    medio=estatusInscripcion.medio,  
                    banco=estatusInscripcion.banco,  
                    tipo_cuenta=estatusInscripcion.tipo_cuenta,   
                    numero=estatusInscripcion.numero,                          
                    
                    foto=estatusInscripcion.foto,   
                    cv=estatusInscripcion.cv,     
                    contrato=estatusInscripcion.contrato,                   
                    
                    created = ahora,    
                    updated = ahora,
                    creator_user= creatorUserId,    
                    updater_user = creatorUserId
                )
                
                # confirmamos los pasos
                paso=6
                self.db.add(newEstatusInscripcion)
                paso=7
                self.db.commit()
                
                paso=8
                #creamos el registro historico de estatus
                result2=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,newEstatusInscripcion,"Creacion de estatus de inscripcion de un usuario")
                       
                # devolvemos los datos   
                paso=9
                data=EstatusInscripcionUserController.get_data(newEstatusInscripcion) 

                return ({"result":"1","estado":"estatus de inscripción creado","data":data})
            
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})
            
            
    # metodo para consultar un archivo por Id
    # @params userId: id del usuario que se desa consultar
    def get_estatus_inscripcion(self, userId):

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()

        if (nRecordFileUser>0):
            # Obtener la dirección del servidor.
            result= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

            data=EstatusInscripcionUserController.get_data(result) 

            if (result):
                return ({"result":"1","estado":"Archivo encontrado","data":data })                            
            else:
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })   
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })    

 
    # metodo para actualizar el estatus inscripcion 
    # @params userId: id del usuario que se desa actualizar
    # @estatusInscripcion: esquema de datos del estatus de inscripcion
    def update_estatus_inscripcion(self, userId, estatusInscripcion: EstatusInscripcionSchema, creatorUserId):
        ahora=datetime.datetime.now()

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()

        if (nRecordFileUser>0):
            # Obtener el registro
            try:
                paso=1
                estatusInscripcionExists= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                # actualizamos 
                paso=2
                estatusInscripcionExists.nombre=estatusInscripcion.nombre,
                estatusInscripcionExists.apellido=estatusInscripcion.apellido,
                estatusInscripcionExists.nacionalidad=estatusInscripcion.nacionalidad,
                estatusInscripcionExists.sexo=estatusInscripcion.sexo,
                estatusInscripcionExists.fecha_nac=estatusInscripcion.fecha_nac,
                estatusInscripcionExists.estado_civil=estatusInscripcion.estado_civil,

                estatusInscripcionExists.region=estatusInscripcion.region,
                estatusInscripcionExists.comuna=estatusInscripcion.comuna,
                estatusInscripcionExists.direccion=estatusInscripcion.direccion,

                estatusInscripcionExists.telefono=estatusInscripcion.telefono,
                estatusInscripcionExists.email=estatusInscripcion.email,  

                estatusInscripcionExists.tipo_contrato=estatusInscripcion.tipo_contrato,
                estatusInscripcionExists.termino=estatusInscripcion.termino,   
                estatusInscripcionExists.fecha_contratacion=estatusInscripcion.fecha_contratacion,   
                estatusInscripcionExists.salario_base=estatusInscripcion.salario_base,   
                estatusInscripcionExists.unidad_sueldo=estatusInscripcion.unidad_sueldo,  
                estatusInscripcionExists.monto_sueldo=estatusInscripcion.monto_sueldo,    
                estatusInscripcionExists.sociedad=estatusInscripcion.sociedad,       
                estatusInscripcionExists.sede=estatusInscripcion.sede,   
                estatusInscripcionExists.departamento=estatusInscripcion.departamento,    
                estatusInscripcionExists.cargo=estatusInscripcion.cargo,    
                estatusInscripcionExists.grupo=estatusInscripcion.grupo,  
                estatusInscripcionExists.modalidad=estatusInscripcion.modalidad,  
                estatusInscripcionExists.dias_descanso=estatusInscripcion.dias_descanso,
                estatusInscripcionExists.nivel_estudio=estatusInscripcion.nivel_estudio, 

                estatusInscripcionExists.medio=estatusInscripcion.medio,  
                estatusInscripcionExists.banco=estatusInscripcion.banco,  
                estatusInscripcionExists.tipo_cuenta=estatusInscripcion.tipo_cuenta,   
                estatusInscripcionExists.numero=estatusInscripcion.numero,estatusInscripcionExists,        

                estatusInscripcionExists.foto=estatusInscripcion.foto,   
                estatusInscripcionExists.cv=estatusInscripcion.cv,     
                estatusInscripcionExists.contrato=estatusInscripcion.contrato

                estatusInscripcionExists.updated = ahora,
                estatusInscripcionExists.updater_user = creatorUserId 
                
                paso=3
                # confirmamos los cambios
                self.db.commit()           
                
                # devolvemos el nuevo estado
                paso=4
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists) 

                
                return ({"result":"1","estado":"Estatus de inscripcion actualizado","data":data }) 
            
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})                
  
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })  
        

    # metodo que permite actualizar el estatus de inscripcion de datos laborales
    # @params estatusLaborales: esquema de datos del estatus de inscripcion  de datos laborales 
    def update_estatus_inscripcion_laborales (self,estatusLaborales:EstatusInscripcionLaboralSchema, creatorUserId):
        ahora=datetime.datetime.now()
        
        paso=1
        userId=estatusLaborales.user_id
        
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()
                
                #creamos el registro historico
                EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualizacion de los datos laborales del estatus de inscripcion")
                
                # actualizamos el estado de la inscripcion
                estatusInscripcionExists.tipo_contrato=estatusLaborales.tipo_contrato
                estatusInscripcionExists.termino=estatusLaborales.termino
                estatusInscripcionExists.fecha_contratacion=estatusLaborales.fecha_contratacion
                estatusInscripcionExists.salario_base=estatusLaborales.salario_base
                estatusInscripcionExists.unidad_sueldo=estatusLaborales.unidad_sueldo
                estatusInscripcionExists.monto_sueldo=estatusLaborales.monto_sueldo
                estatusInscripcionExists.sede=estatusLaborales.sede
                estatusInscripcionExists.departamento=estatusLaborales.departamento
                estatusInscripcionExists.cargo=estatusLaborales.cargo
                estatusInscripcionExists.grupo=estatusLaborales.grupo
                estatusInscripcionExists.modalidad=estatusLaborales.modalidad
                estatusInscripcionExists.dias_descanso=estatusLaborales.dias_descanso
                estatusInscripcionExists.nivel_estudio=estatusLaborales.nivel_estudio
                estatusInscripcionExists.updater_user=creatorUserId,
                estatusInscripcionExists.updated=ahora
                
                #confirmamos los cambios
                paso=4
                self.db.commit()
                
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"}) 


    # metodo que permite actualizr el estatus de inscripcion de datos de pago
    # @params estatusPago: esquema de datos del estatus de inscripcion  de datos de pago    
    def update_estatus_inscripcion_pago (self,estatusPago:EstatusInscripcionPagoSchema, creatorUserId):
        ahora=datetime.datetime.now()
        
        paso=1
        userId=estatusPago.user_id
        
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                
                
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()
                
                result=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualizacion del estatus de pago en las preinscripciones")
                
                # actualizamos el estado de la inscripcion
                estatusInscripcionExists.medio=estatusPago.medio
                estatusInscripcionExists.banco=estatusPago.banco
                estatusInscripcionExists.tipo_cuenta=estatusPago.tipo_cuenta
                estatusInscripcionExists.numero=estatusPago.numero
                
                #confirmamos los cambios
                paso=4
                self.db.commit()
                
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"}) 
    

    # metodo que permite actualizr el estatus de inscripcion de datos de pago
    # @params estatusPago: esquema de datos del estatus de inscripcion  de datos de pago    
    def update_estatus_sociedad (self,userId, creatorUserId,estado):
        ahora=datetime.datetime.now()
        
        paso=1
        
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                #creamos el historico
                paso=4
                result1=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del estado de sociedad del estatus de inscripcion")

                
                # actualizamos el estado de la inscripcion
                paso=5
                estatusInscripcionExists.sociedad=estado
                estatusInscripcionExists.updated=ahora
                estatusInscripcionExists.updater_user=creatorUserId
 
                
                #confirmamos los cambios
                paso=6
                self.db.commit()
                
                paso=7
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"}) 

        
    # metodo que permite actualizr el estatus de inscripcion de datos de pago
    # @params estatusPago: esquema de datos del estatus de inscripcion  de datos de pago    
    def update_estatus_departamento (self,userId, creatorUserId,estado):
        ahora=datetime.datetime.now()
        
        paso=1
        
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                #creamos el historico
                paso=4
                result1=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del estado del Departamento del estatus de inscripcion")

                
                # actualizamos el estado de la inscripcion
                paso=5
                estatusInscripcionExists.departamento=estado
                estatusInscripcionExists.updated=ahora
                estatusInscripcionExists.updater_user=creatorUserId
 
                
                #confirmamos los cambios
                paso=6
                self.db.commit()
                
                paso=7
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"}) 
        
    # metodo que permite actualizr el estatus de inscripcion de datos sede
    # @params estatusPago: esquema de datos del estatus de inscripcion  de sede    
    def update_estatus_sede (self,userId, creatorUserId,estado):
        ahora=datetime.datetime.now()
        
        paso=1
        
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                #creamos el historico
                paso=4
                result1=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del estado del Sede del estatus de inscripcion")

                
                # actualizamos el estado de la inscripcion
                paso=5
                estatusInscripcionExists.sede=estado
                estatusInscripcionExists.updated=ahora
                estatusInscripcionExists.updater_user=creatorUserId
 
                
                #confirmamos los cambios
                paso=6
                self.db.commit()
                
                paso=7
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})    
        
        
    # metodo que permite actualizr el estatus de inscripcion de datos de grupo
    # @params estatusPago: esquema de datos del estatus de inscripcion  de datos grupo    
    def update_estatus_grupo (self,userId, creatorUserId,estado):
        ahora=datetime.datetime.now()
        
        paso=1
        
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                #creamos el historico
                paso=4
                result1=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del estado del Grupo del estatus de inscripcion")

                
                # actualizamos el estado de la inscripcion
                paso=5
                estatusInscripcionExists.grupo=estado
                estatusInscripcionExists.updated=ahora
                estatusInscripcionExists.updater_user=creatorUserId
 
                
                #confirmamos los cambios
                paso=6
                self.db.commit()
                
                paso=7
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})                 
        

    # metodo para actualizar el estatus del CV a SUBIDO (1) No SUBIDO (0)
    # @params userId: id del usuario que se desa actualizar
    def update_estatus_cv(self, userId, creatorUserId,estado):
        ahora=datetime.datetime.now()

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()

        if (nRecordFileUser>0):
            # Obtener el registro
            try:
                paso=1
                estatusInscripcionExists= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                # creamos el historico
                result=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del CV en el estatus de inscripcion")

                # actualizamos 
                paso=2
                estatusInscripcionExists.cv=estado,     
                estatusInscripcionExists.updated = ahora,
                estatusInscripcionExists.updater_user = creatorUserId 
                
                paso=3
                # confirmamos los cambios
                self.db.commit()           
                
                # devolvemos el nuevo estado
                paso=4
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)
 
                
                return ({"result":"1","estado":"Estatus de CV en inscripcion actualizado","data":data }) 
            
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})                
  
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })          
       
    
    # metodo para actualizar el estatus del contrato a SUBIDO
    # @params userId: id del usuario que se desa actualizar
    def update_estatus_contrato(self, userId, creatorUserId,estado):
        ahora=datetime.datetime.now()

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()

        if (nRecordFileUser>0):
            # Obtener el registro
            try:
                paso=1
                estatusInscripcionExists= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                # creamos el historico
                result=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del CV en el estatus de inscripcion")

                # actualizamos 
                paso=2
                estatusInscripcionExists.contrato=estado,     
                estatusInscripcionExists.updated = ahora,
                estatusInscripcionExists.updater_user = creatorUserId 
                
                paso=3
                # confirmamos los cambios
                self.db.commit()           
                
                # devolvemos el nuevo estado
                paso=4
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)
                
                return ({"result":"1","estado":"Estatus de CV en inscripcion actualizado","data":data }) 
            
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})                
  
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })       
    

    # metodo para actualizar el estatus de la foto a SUBIDO
    # @params userId: id del usuario que se desa actualizar
    def update_estatus_foto(self, userId, creatorUserId, estado):
        ahora=datetime.datetime.now()

        # verificamos si existe el registro
        nRecordFileUser= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()

        if (nRecordFileUser>0):
            # Obtener el registro
            try:
                paso=1
                estatusInscripcionExists= self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                # creamos el historico
                result=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del CV en el estatus de inscripcion")

                # actualizamos 
                paso=2
                estatusInscripcionExists.foto=estado,     
                estatusInscripcionExists.updated = ahora,
                estatusInscripcionExists.updater_user = creatorUserId 
                
                paso=3
                # confirmamos los cambios
                self.db.commit()           
                
                # devolvemos el nuevo estado
                paso=4
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                
                return ({"result":"1","estado":"Estatus de CV en inscripcion actualizado","data":data }) 
            
            except ValueError as e:
                return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})                
  
        else:
            return ({"result":"-1","estado":"Usuario no encontrado","userId":userId })      


    # metodo para actualizar el estatus de los datos de contacto 
    # @params userId: id del usuario que se desa actualizar
    def update_estatus_contacto(self,userId,creatorUserId, estado):
        ahora=datetime.datetime.now()
        
        paso=1
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                #creamos el historico
                paso=4
                result1=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del estado del Grupo del estatus de inscripcion")

                
                # actualizamos el estado de la inscripcion
                paso=5
                estatusInscripcionExists.email=estado
                estatusInscripcionExists.telefono=estado
                estatusInscripcionExists.updated=ahora
                estatusInscripcionExists.updater_user=creatorUserId
 
                
                #confirmamos los cambios
                paso=6
                self.db.commit()
                
                paso=7
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"})             
    
    
    # metodo para actualizar el estatus de los datos de ubicacion
    # @params userId: id del usuario que se desa actualizar
    def update_estatus_ubicacion(self,userId,creatorUserId, estado):
        ahora=datetime.datetime.now()
        
        paso=1
        try:
            #verificamos si existe el registro de lo contrario emitimos el error
            paso=2
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                #buscamos el registro
                paso=3
                estatusInscripcionExists=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()

                #creamos el historico
                paso=4
                result1=EstatusInscripcionUserController.create_historico_estatus_inscripcion(self,estatusInscripcionExists,"Actualización del estado del Grupo del estatus de inscripcion")

                
                # actualizamos el estado de la inscripcion
                paso=5
                estatusInscripcionExists.region=estado
                estatusInscripcionExists.comuna=estado
                estatusInscripcionExists.direccion=estado
                estatusInscripcionExists.updated=ahora
                estatusInscripcionExists.updater_user=creatorUserId
 
                
                #confirmamos los cambios
                paso=6
                self.db.commit()
                
                paso=7
                data=EstatusInscripcionUserController.get_data(estatusInscripcionExists)

                return ({"result":"1","estado":"Estatus de Inscripcion actualizado","data":data }) 
            else:
                # no existe emitimos error
                return ({"result":"-1","estado":"Usuario no encontrado","userId":userId }) 
        
        except ValueError as e:
            return( {"result":"-1","cadenaError": f"Error {str(e)} paso {paso}"}) 

    # metodo que permite determinar el avance de  inscripcion del usuario
    # @params userId: id del usuario que se está consultando
    def avance_inscripcion (self, userId):
        paso=1
        try:
            nRecord=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).count()
            
            if (nRecord>0):
                # existe buscamos el registro
                result=self.db.query(EstatusInscripcionModel).filter(EstatusInscripcionModel.user_id==userId).first()
                
                # el total del los campos es 
                '''
                1 rut	int(11)
                2 nombre	int(11)
                3 apellido	int(11)
                4 nacionalidad	int(11)
                5 sexo	int(11)
                6 fecha_nac	int(11)
                7 estado_civil	int(11)
                8 region	int(11)
                9 comuna	int(11)
                10 direccion	int(11)
                11 telefono	int(11)
                12 email	int(11)
                13 tipo_contrato	int(11)
                14 termino	int(11)
                15 fecha_contratacion	int(11)
                16 salario_base	int(11)
                17 unidad_sueldo	int(11)
                18 monto_sueldo	int(11)
                19 sociedad	int(11)
                20 sede	int(11)
                21 departamento	int(11)
                22 cargo	int(11)
                23 grupo	int(11)
                24 modalidad	int(11)
                25 dias_descanso	int(11)
                26 nivel_estudio	int(11)
                27 medio	int(11)
                28 banco	int(11)
                29 tipo_cuenta	int(11)
                30 numero	int(11)
                foto	int(11)
                cv	int(11)
                contrato	int(11)                
                '''
                suma=0
                suma=suma+result.rut
                suma=suma+result.nombre  
                suma=suma+result.apellido
                suma=suma+result.nacionalidad   
                suma=suma+result.sexo
                suma=suma+result.fecha_nac  
                suma=suma+result.estado_civil
                suma=suma+result.region  
                suma=suma+result.comuna
                suma=suma+result.direccion  
                suma=suma+result.telefono
                suma=suma+result.email   
                suma=suma+result.tipo_contrato
                suma=suma+result.termino  
                suma=suma+result.fecha_contratacion
                suma=suma+result.salario_base 
                suma=suma+result.unidad_sueldo
                suma=suma+result.monto_sueldo  
                suma=suma+result.sociedad
                suma=suma+result.sede  
                suma=suma+result.departamento
                suma=suma+result.cargo  
                suma=suma+result.grupo
                suma=suma+result.modalidad   
                suma=suma+result.dias_descanso  
                suma=suma+result.nivel_estudio
                suma=suma+result.medio
                suma=suma+result.banco
                suma=suma+result.tipo_cuenta  
                suma=suma+result.numero
                
                avance=(suma*100)/30
                                                                                                
                return( {"result":"1","avance": avance}) 
            
            else:
                # no existe emitimos mensaje de error
                return( {"result":"-1","estado":f"Registro no encontrado"}) 
                
        except ValueError as e:
                return( {"result":"-3","cadenaError": f"Error {str(e)} paso {paso}"})   