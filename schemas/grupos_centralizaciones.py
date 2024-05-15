'''
Esquema de datos que define a la tabla Grupos de Centralizacion
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class GrupoCentralizaciones(BaseModel):
    sociedad_id : int = Field (min=1, max=100)
    es_honorario : bool
    nombre : str = Field(min_length=3, max_length=200)
    monto_max_prestamo : float
    cuotas_max_prestamo : int
    porcentaje_tope_cuota_prestamo : float
    monto_max_anticipo : float
    porcentaje_maximo_anticipo : float
    calcular_porcentaje_segun : str = Field(min_length=0, max_length=10)
    factura_mas_pago : int = Field (ge=0, le=1)
    cuenta_factura_proveedor  : str = Field(min_length=0, max_length=20)
    cuenta_pago_factura  : str = Field(min_length=0, max_length=20)
    cuenta_remunera_deb   : str = Field(min_length=0, max_length=20)
    cuenta_AFP_deb   : str = Field(min_length=0, max_length=20)
    cuenta_salud_deb   : str = Field(min_length=0, max_length=20)
    cuenta_gratificacion_deb   : str = Field(min_length=0, max_length=20)
    cuenta_horas_ext_deb   : str = Field(min_length=0, max_length=20)
    cuenta_seg_AFC_deb   : str = Field(min_length=0, max_length=20)
    cuenta_mov_deb   : str = Field(min_length=0, max_length=20)
    cuenta_col_deb   : str = Field(min_length=0, max_length=20)
    cuenta_otra_asig_deb   : str = Field(min_length=0, max_length=20)
    cuenta_SIS_deb   : str = Field(min_length=0, max_length=20)
    cuenta_mut_deb   : str = Field(min_length=0, max_length=20)
    cuenta_impuesto_unico_deb   : str = Field(min_length=0, max_length=20)
    cuenta_asignacion_fami_deb   : str = Field(min_length=0, max_length=20)
    cuenta_Afc_empresa_cred   : str = Field(min_length=0, max_length=20)
    cuenta_asignacion_familiar_cred   : str = Field(min_length=0, max_length=20)
    cuenta_impuesto_unico_cred   : str = Field(min_length=0, max_length=20)
    cuenta_sueldo_pagar_cred   : str = Field(min_length=0, max_length=20)  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "es_honorario": True,
                    "nombre":"Demo",
                    "monto_max_prestamo" : 0,
                    "cuotas_max_prestamo" : 0,
                    "porcentaje_tope_cuota_prestamo" : 0,
                    "monto_max_anticipo" : 0,
                    "porcentaje_maximo_anticipo" : 0,
                    "calcular_porcentaje_segun" : "",
                    "factura_mas_pago" : 0,
                    "cuenta_factura_proveedor"  : "",
                    "cuenta_pago_factura"  : "",
                    "cuenta_remunera_deb"   : "",
                    "cuenta_AFP_deb"   : "",
                    "cuenta_salud_deb"   : "",
                    "cuenta_gratificacion_deb"   : "",
                    "cuenta_horas_ext_deb"   : "",
                    "cuenta_seg_AFC_deb"   : "",
                    "cuenta_mov_deb"   : "",
                    "cuenta_col_deb"   : "",
                    "cuenta_otra_asig_deb"   : "",
                    "cuenta_SIS_deb"   : "",
                    "cuenta_mut_deb"   : "",
                    "cuenta_impuesto_unico_deb"   : "",
                    "cuenta_asignacion_fami_deb"   : "",
                    "cuenta_Afc_empresa_cred"   :"",
                    "cuenta_asignacion_familiar_cred"   : "",
                    "cuenta_impuesto_unico_cred"   : "",
                    "cuenta_sueldo_pagar_cred"   : ""                      
                }
            ]
        }
    }    
