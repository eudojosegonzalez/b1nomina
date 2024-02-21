'''
Este archivo contiene las funciones básicas del CRUD DashboardAdmin
Created 2024-01
'''
'''
    **********************************************************************
    * Estructura del Modelo                                              *
    **********************************************************************


  
'''   

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_,and_


import  datetime


# importamos el modelo de la base de datos
from models.user import Usuario as UsuarioModel



# esto representa los metodos implementados en la tabla
class DashboardAdminController():
    # metodo constructor que requerira una instancia a la Base de Datos
    def __init__(self,db) -> None:
        self.db = db

    
    #metodo para insertar  los datos del banco 
    # @userCreatorId: Id del usuario que está creando el registro
    # @params banco: esquema de los datos banco que se desea insertar       
    def count_users(self):
        try:
            nRecordUsers = self.db.query(UsuarioModel).filter(UsuarioModel.activo == 1).count()  
            return ({"result":"1","estado":"creado","nRecordUsers":nRecordUsers})
        except ValueError as e:
            return( {"result":"-3","error": str(e)})

    