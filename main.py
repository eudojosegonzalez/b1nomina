#importamos la libreria para cargar los archivos de entorno
import dotenv


#importamos FASTAIP
from fastapi import FastAPI
from fastapi.responses import  RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


#Importamos los archivos de conforuracion de la base de datos
from config.database import engine, Base


#importamos el routers
from routers.user import user_router
from routers.contacto import user_contact_router
from routers.ubicacion import user_ubicacion_router
from routers.files_users import files_user_router
from routers.pic_users import pic_user_router
from routers.cv_users import cv_user_router
from routers.contrato_users import contrato_user_router
from routers.bancarios_user import bancarios_user_router
from routers.bancos import bancos_router
from routers.afp import afp_router
from routers.apv import apv_router
from routers.basic_parameter import basic_parameter_router
from routers.eventos import eventos_router
from routers.nomina import nomina_router
from routers.sociedades import sociedades_router
from routers.bancarios_sociedad import bancarios_sociedad_router
from routers.mutuales_sociedad import mutuales_sociedad_router
from routers.sedes import sedes_router
from routers.departamentos import departamentos_router
from routers.grupos_empleados import grupos_empleados_router
from routers.cargos import cargos_router
from routers.mutuales import mutuales_router
from routers.dashboard_admin import dashboard_admin_router
from routers.unidades_pacto import unidades_pacto_router
from routers.periodos import periodos_router
from routers.categorias_configuracion import categorias_configuracion_router
from routers.configuracion import configuracion_router
from routers.centros_costos import centros_costos_router
from routers.centralizaciones import centralizaciones_router
from routers.grupos_centralizaciones import grupos_centralizaciones_router
from routers.prevision_salud import prevision_salud_router
from routers.cuentas_contables import cuentas_contables_router
from routers.tipos_prestamos import tipos_prestamos_router
from routers.cajas_compensacion import cajas_compensacion_router
from routers.tramos_impuesto_unico import tramos_impuesto_unico_router
from routers.tramos_asignacion_familiar import tramos_asignacion_familiar_router
from routers.datos_laborales import datos_laborales_router
from routers.datos_pago import datos_pago_router
from routers.usuarios_afc import usuarios_afc_router
from routers.usuarios_afp import usuarios_afp_router
from routers.usuarios_prevision_salud import usuarios_prevision_salud_router
from routers.campos_adicionales import campos_adicionales_router

#importamos el manejador de errores
from middleware.error_handler import ErrorHandler

#descripcion de los endpoints
tags_metadata = [
    {
        "name": "Auth",
        "description": "Operaciones de validación de usuario y generación de tokens",
    },
    {
        "name": "DashboardAdmin",
        "description": "Dashboard inicial del Administrador",
    },    
    {
        "name": "Usuarios",
        "description": "Operaciones relacionadas con los datos personales de los usuarios",
    },
    {
        "name": "Contacto",
        "description": "Operaciones relacionadas con los datos de contacto de los usuarios",
    },    
    {
        "name": "Localizacion",
        "description": "Operaciones relacionadas con los datos de localizacion de los usuarios",
    },     
    {
        "name": "Archivos de Usuarios",
        "description": "Operaciones relacionadas con los Archivos de los Usuarios",
    },    
    {
        "name": "Fotos de Usuarios",
        "description": "Operaciones relacionadas con las fotos de los Usuarios",
    },     
    {
        "name": "Bancarios Usuarios",
        "description": "Operaciones relacionadas con los Datos de Pago de los Usuarios",
    },   
    {
        "name": "Datos Laborales",
        "description": "Operaciones relacionadas con los Datos Laborales de los Usuarios",
    },    
    {
        "name": "Datos Pago",
        "description": "Operaciones relacionadas con los Datos de Pago de los Usuarios",
    },      
    {
        "name": "AFC Usuarios",
        "description": "Operaciones relacionadas con los Datos AFC de los Usuarios",
    },  
    {
        "name": "AFP Usuarios",
        "description": "Operaciones relacionadas con los Datos AFP de los Usuarios",
    }, 
    {
        "name": "Prevision Salud Usuarios",
        "description": "Operaciones relacionadas con los Datos Prevision Salud de los Usuarios",
    },                    
    {
        "name": "Instituciones AFP",
        "description": "Operaciones relacionadas con las instituciones AFP",
    },    
    {
        "name": "Instituciones APV",
        "description": "Operaciones relacionadas con las instituciones APV",
    }, 
    {
        "name": "Categorias Configuracion",
        "description": "Operaciones relacionadas con las Categorias de Configuración del Sistema",
    },     
    {
        "name": "Configuracion",
        "description": "Operaciones relacionadas con la Configuración del Sistema",
    },  
    {
        "name": "Centralizaciones",
        "description": "Operaciones relacionadas con las Centralizaciones del Sistema",
    },
    {
        "name": "Centros de Costo",
        "description": "Operaciones relacionadas con los Centros de Costo del Sistema",
    },            
    {
        "name": "Periodos",
        "description": "Operaciones relacionadas con los Periodos",
    },            
    {
        "name": "Bancos",
        "description": "Operaciones relacionadas con las instituciones Bancarias",
    },
    {
        "name": "Mutuales",
        "description": "Operaciones relacionadas con las instituciones Mutuales",
    },    
    {
        "name": "Parametros Basicos",
        "description": "Operaciones relacionadas con los Parámetros Básicos del Sistema",
    }, 
    {
        "name": "Eventos",
        "description": "Operaciones relacionadas con los Eventos de Nómina",
    },     
    {
        "name": "Nomina",
        "description": "Operaciones relacionadas con la Nómina",
    },    
    {
        "name": "UnidadesPacto",
        "description": "Operaciones relacionadas con las Unidades de Pacto",
    },   
    {
        "name": "Sociedades",
        "description": "Operaciones relacionadas con las Sociedades del sistema",
    }, 
    {
        "name": "Grupos Centralizaciones",
        "description": "Operaciones relacionadas con los Grupos de Centralizaciones del sistema",
    },          
    {
        "name": "Bancarios Sociedad",
        "description": "Operaciones relacionadas con los Datos Bancarios de las Sociedades del sistema",
    },      
    {
        "name": "Mutuales Sociedad",
        "description": "Operaciones relacionadas con los Datos Mutuales de las Sociedades del sistema",
    },        
    {
        "name": "Sedes",
        "description": "Operaciones relacionadas con las Sedes de las Sociedades",
    },     
    {
        "name": "Departamentos",
        "description": "Operaciones relacionadas con los Departamentos de las Sociedades",
    },     
    {
        "name": "Grupos Empleados",
        "description": "Operaciones relacionadas con los Grupos de Empleados",
    },      
    {
        "name": "Cargos",
        "description": "Operaciones relacionadas con los Cargos de las Sociedades",
    },  
    {
        "name": "Prevision Salud",
        "description": "Operaciones relacionadas con las Instituciones de Prevision Salud",
    },  
    {
        "name": "Cuentas Contables",
        "description": "Operaciones relacionadas con las Cuentas Contables",
    },    
    {
        "name": "Tipos Prestamos",
        "description": "Operaciones relacionadas con los Tipos Prestamos",
    },           
    {
        "name": "Cajas Compensacion",
        "description": "Operaciones relacionadas con las Cajas de Compensación",
    },     
    {
        "name": "Tramos Impuesto Unico",
        "description": "Operaciones relacionadas con los Tramos de Impuesto Único",
    },   
    {
        "name": "Tramos Asignacion Familiar",
        "description": "Operaciones relacionadas con los Tramos de Asignacion Familiar",
    },  
    {
        "name": "Campos Adicionales",
        "description": "Operaciones relacionadas con los Campos Adicionales",
    },     
]

#cargamos las variables de entorno
dotenv.load_dotenv()

#Cargamos la documentacion de las rutas
app = FastAPI(openapi_tags=tags_metadata,debug=True)
app.title='Core B1 Nomina by Kyros'
app.version='V1.0'


# manejador de errores
app.add_middleware(ErrorHandler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"],
	max_age=3600,
)

#inclusión de los endpoints
app.include_router(user_router)
app.include_router(user_contact_router)
app.include_router(user_ubicacion_router)
app.include_router(files_user_router)
app.include_router(pic_user_router)
app.include_router(cv_user_router)
app.include_router(contrato_user_router)
app.include_router(bancarios_user_router)
app.include_router(datos_laborales_router)
app.include_router(datos_pago_router)
app.include_router(usuarios_afc_router)
app.include_router(usuarios_afp_router)
app.include_router(usuarios_prevision_salud_router)
app.include_router(categorias_configuracion_router)
app.include_router(configuracion_router)
app.include_router(centralizaciones_router)
app.include_router(grupos_centralizaciones_router)
app.include_router(centros_costos_router)
app.include_router(periodos_router)
app.include_router(afp_router)
app.include_router(bancos_router)
app.include_router(basic_parameter_router)
app.include_router(eventos_router)
app.include_router(nomina_router)
app.include_router(sociedades_router)
app.include_router(bancarios_sociedad_router)
app.include_router(mutuales_sociedad_router)
app.include_router(sedes_router)
app.include_router(departamentos_router)
app.include_router(grupos_empleados_router)
app.include_router(cargos_router)
app.include_router(mutuales_router)
app.include_router(dashboard_admin_router)
app.include_router(unidades_pacto_router)
app.include_router(apv_router)
app.include_router(prevision_salud_router)
app.include_router(cuentas_contables_router)
app.include_router(tipos_prestamos_router)
app.include_router(cajas_compensacion_router)
app.include_router(tramos_impuesto_unico_router)
app.include_router(tramos_asignacion_familiar_router)
app.include_router(campos_adicionales_router)




# esto crea la base de datos si no existe al empezar la app
Base.metadata.create_all(bind=engine)


@app.get('/',tags=['Home'])
def home():
    # redireccionamos a la documentación de la API
    return RedirectResponse("/docs")


